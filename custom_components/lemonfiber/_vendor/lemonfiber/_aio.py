# Copyright (c) 2026 NightWorksIO
"""The asynchronous client, on aiohttp.

A pinned address is reached with an `aiohttp.Fingerprint` on every request:
aiohttp compares the certificate's SHA-256 digest with it once the handshake
completes and before a byte of the request is written, and refuses the
connection where they differ (`ARCH-R99`). It is given per request rather than
to a connector, so it holds on a session the caller supplied, whatever that
session's connector was built with; an unpinned https address is given a
verifying context per request for the same reason.
"""

import asyncio
import ssl
from typing import TYPE_CHECKING, Final, Self

import aiohttp

from lemonfiber import _wire
from lemonfiber.jobs import Ended, Finished, Running
from lemonfiber.problems import (
    CertificateRefusedError,
    ConfigurationError,
    LemonfiberError,
    UnreachableError,
)
from lemonfiber.stream import FIRST_WAIT, OPENED, RECONNECTS_ALLOWED, SILENCE_ALLOWED, Break, Following

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator, AsyncIterator, Callable, Mapping
    from types import TracebackType

    from lemonfiber._generated import Envelope, JobEnvelope
    from lemonfiber.address import Address, Route
    from lemonfiber.capabilities import CapabilitySet
    from lemonfiber.credential import Credential
    from lemonfiber.jobs import JobStanding
    from lemonfiber.reads import Read
    from lemonfiber.stream import Arrival, Live, Stale


type TlsSetting = aiohttp.Fingerprint | ssl.SSLContext | bool

NOT_PROXIED: Final = "The session given would send through a proxy, and a credential goes to the stack alone, so nothing was sent."
"""Why a request a caller's session would send through a proxy is refused."""


async def unproxied(
    request: aiohttp.ClientRequest,
    handler: aiohttp.ClientHandlerType,
) -> aiohttp.ClientResponse:
    """Send a request straight to the stack, refusing one the session would send through a proxy.

    A session the caller gave may carry a proxy of its own, or read one from the
    environment; either would hand the credential to the proxy, in the clear over
    http. This runs once aiohttp has chosen the proxy and before anything is
    sent, and as the request's only middleware it also keeps the session's own
    middlewares from ever seeing the credential.
    """
    if request.proxy is not None:
        raise ConfigurationError(NOT_PROXIED)
    return await handler(request)


STRAIGHT: Final = (unproxied,)
"""The middlewares every request is sent through: this one, in place of any the session holds."""


def tls_for(address: Address) -> TlsSetting:
    """Return what every request to an address is checked with: its pin, a verifying context, or nothing."""
    if address.pin is not None:
        return aiohttp.Fingerprint(address.pin.digest)
    if address.scheme == "https":
        return ssl.create_default_context()
    return True


def checked(session: aiohttp.ClientSession) -> aiohttp.ClientSession:
    """Return a caller's session, refusing one whose connector would not check a pin."""
    if not isinstance(session.connector, aiohttp.TCPConnector):
        msg = "A session given to the client connects over TCP, so the certificate pin can be checked."
        raise ConfigurationError(msg)
    return session


async def attempt(
    session: aiohttp.ClientSession,
    route: Route,
    tls: TlsSetting,
    call: _wire.Call,
    limit: aiohttp.ClientTimeout,
) -> _wire.Answer | None:
    """Send one call over one route, or return nothing where no connection could be made there.

    A route that reaches a named stack by an address it resolved to names the
    stack in the TLS handshake, and the certificate is checked against that name.
    A failure is raised once aiohttp's error is let go, since that error holds
    the request's headers, credential included, and would ride along as the
    failure's cause.
    """
    try:
        async with session.request(
            call.method,
            route.url(call.path),
            data=call.body,
            headers={**call.headers, **route.headers()},
            ssl=tls,
            server_hostname=route.named,
            middlewares=STRAIGHT,
            allow_redirects=False,
            raise_for_status=False,
            timeout=limit,
        ) as response:
            body = await response.read()
    except aiohttp.ServerFingerprintMismatch, aiohttp.ClientSSLError:
        failure: LemonfiberError = CertificateRefusedError(_wire.CERTIFICATE_REFUSED)
    except aiohttp.ClientConnectorError:
        return None
    except aiohttp.ClientError, TimeoutError:
        failure = UnreachableError(_wire.NOT_ANSWERING)
    else:
        headers = {name.lower(): value for name, value in response.headers.items()}
        return _wire.Answer(response.status, headers, body)
    raise failure


async def exchange(
    session: aiohttp.ClientSession,
    address: Address,
    tls: TlsSetting,
    call: _wire.Call,
    limit: aiohttp.ClientTimeout,
) -> _wire.Answer:
    """Send one call over the first route a connection can be made on, following no redirect.

    A route is passed over only where no connection could be made, so nothing
    was sent; once a connection is made, its outcome is the call's.
    """
    for route in address.routes:
        answer = await attempt(session, route, tls, call, limit)
        if answer is not None:
            return answer
    raise UnreachableError(_wire.NOT_ANSWERING)


class AsyncClient:
    """Talks to one stack, asynchronously, with one credential.

    Give it the `aiohttp.ClientSession` the application already holds, as Home
    Assistant gives an integration its own; a client given none opens one and
    closes it in `aclose`. A session it was given is never closed by it.
    """

    def __init__(
        self,
        address: Address,
        credential: Credential,
        *,
        session: aiohttp.ClientSession | None = None,
        timeout: float = _wire.DEFAULT_TIMEOUT,
    ) -> None:
        """Hold an address, a credential and the session to send through; nothing is sent until a call is made."""
        self._address = address
        self._credential = credential
        self._given = None if session is None else checked(session)
        self._owned: aiohttp.ClientSession | None = None
        self._tls = tls_for(address)
        self._limit = aiohttp.ClientTimeout(total=timeout)

    @property
    def address(self) -> Address:
        """Return where this client sends, and the pin it holds that address to."""
        return self._address

    def _session(self) -> aiohttp.ClientSession:
        if self._given is not None:
            return self._given
        if self._owned is None:
            self._owned = aiohttp.ClientSession()
        return self._owned

    async def _answer(self, call: _wire.Call) -> _wire.Answer:
        sent = _wire.with_credential(call, self._credential)
        return await exchange(self._session(), self._address, self._tls, sent, self._limit)

    async def read(self, read: Read, query: _wire.Query | None = None) -> Envelope:
        """Ask for what a command prints under `--json`."""
        return _wire.envelope_of(await self._answer(_wire.read_call(read, query)))

    async def capabilities(self) -> CapabilitySet:
        """Ask what the stack can do, for the credential this client holds, as it stands now."""
        return _wire.capabilities_of(await self._answer(_wire.capabilities_call()))

    async def logs(self, query: _wire.Query | None = None) -> list[Envelope]:
        """Ask for what the services have been saying, a `log` envelope a line."""
        return _wire.envelopes_of(await self._answer(_wire.logs_call(query)))

    async def bundle(self, name: str) -> _wire.Bundle:
        """Fetch one support bundle this run wrote, by name, as the bytes it is."""
        return _wire.bundle_of(name, await self._answer(_wire.bundle_call(name)))

    async def act(self, action: str, arguments: Mapping[str, _wire.Json] | None = None) -> Envelope:
        """Tell lemonfiber to do something the command line could also do. Sent once, never retried."""
        return _wire.envelope_of(await self._answer(_wire.action_call(action, arguments)))

    async def job(self, job: str) -> JobStanding:
        """Ask where the work a name stands for got to."""
        return _wire.standing_of(job, await self._answer(_wire.job_call(job, "GET")))

    async def release(self, job: str) -> JobStanding:
        """Let a name go, ending the work it stands for, and say where it now stands."""
        return _wire.standing_of(job, await self._answer(_wire.job_call(job, "DELETE")))

    async def follow(
        self,
        job: str | JobEnvelope,
        *,
        every: float = _wire.DEFAULT_EVERY,
        within: float | None = None,
    ) -> Finished | Ended:
        """Ask where work stands every `every` seconds until it is no longer going.

        Raises `StillRunningError` once `within` seconds have passed with it still going.
        """
        name = _wire.job_name(job)
        loop = asyncio.get_running_loop()
        started = loop.time()
        standing = await self.job(name)
        while isinstance(standing, Running):
            await asyncio.sleep(_wire.next_wait(name, started, loop.time(), every, within))
            standing = await self.job(name)
        return standing

    def events(
        self,
        *,
        silence: float = SILENCE_ALLOWED,
        reconnects: int = RECONNECTS_ALLOWED,
        first_wait: float = FIRST_WAIT,
    ) -> AsyncStream:
        """Follow the live stream: what arrives, what has gone stale across a gap, and each gap itself.

        Silence longer than `silence` seconds is a broken stream. A broken stream
        is reopened from the last event it carried, waiting `first_wait` seconds
        and twice as long after each failure, and `StreamLostError` is raised once
        `reconnects` attempts in a row have failed.
        """
        following = Following(self._credential, silence=silence, reconnects=reconnects, first_wait=first_wait)
        connect = aiohttp.ClientTimeout(total=None, sock_connect=self._limit.total)
        return AsyncStream(self._session, self._address, self._tls, following, connect)

    async def aclose(self) -> None:
        """Close the session this client opened, if it opened one."""
        if self._owned is not None:
            await self._owned.close()
            self._owned = None

    async def __aenter__(self) -> Self:
        """Return the client, to be closed when the block ends."""
        return self

    async def __aexit__(
        self,
        kind: type[BaseException] | None,
        error: BaseException | None,
        trace: TracebackType | None,
    ) -> None:
        """Close the client."""
        await self.aclose()


class AsyncStream:
    """The live stream, followed asynchronously. `async for` it for each `Arrival`; `aclose` it to let go."""

    def __init__(
        self,
        session: Callable[[], aiohttp.ClientSession],
        address: Address,
        tls: TlsSetting,
        following: Following,
        connect: aiohttp.ClientTimeout,
    ) -> None:
        """Hold what opening and reading the stream needs; nothing is sent until it is iterated."""
        self._session = session
        self._address = address
        self._tls = tls
        self._following = following
        self._connect = connect
        self._arrivals = self._follow()

    def __aiter__(self) -> AsyncIterator[Arrival]:
        """Return the stream itself."""
        return self

    async def __anext__(self) -> Arrival:
        """Return the next arrival, waiting for it."""
        return await anext(self._arrivals)

    def held(self) -> dict[str, Live | Stale]:
        """Return the last value of each kind the stream carried, and whether it is still current."""
        return self._following.held()

    async def _follow(self) -> AsyncGenerator[Arrival]:
        while True:
            async for arrival in self._opening():
                yield arrival
            await asyncio.sleep(self._following.retry())

    async def _opening(self) -> AsyncGenerator[Arrival]:
        call = self._following.call()
        for route in self._address.routes:
            opened = await self._open(route, call)
            if opened is not None:
                break
        else:
            return
        async with opened as response:
            self._following.opened()
            why = Break.ENDED
            while chunk := await self._chunk(response):
                if isinstance(chunk, Break):
                    why = chunk
                    break
                for arrival in self._following.heard(chunk):
                    yield arrival
        for arrival in self._following.broke(why):
            yield arrival

    async def _open(self, route: Route, call: _wire.Call) -> aiohttp.ClientResponse | None:
        """Open the stream over one route: the response once it is open, or nothing where it did not open.

        A refusal the stack answered with, or a certificate it does not hold to,
        is raised; anything else leaves the next route, or the next attempt, to try.
        """
        try:
            response = await self._session().request(
                call.method,
                route.url(call.path),
                headers={**call.headers, **route.headers()},
                ssl=self._tls,
                server_hostname=route.named,
                middlewares=STRAIGHT,
                allow_redirects=False,
                raise_for_status=False,
                timeout=self._connect,
            )
            if response.status == OPENED:
                return response
            headers = {name.lower(): value for name, value in response.headers.items()}
            answer = _wire.Answer(response.status, headers, await response.read())
        except aiohttp.ServerFingerprintMismatch, aiohttp.ClientSSLError:
            failure = CertificateRefusedError(_wire.CERTIFICATE_REFUSED)
        except aiohttp.ClientError, TimeoutError:
            return None
        else:
            refusal = _wire.opening_refusal(answer)
            if refusal is not None:
                raise refusal
            return None
        raise failure

    async def _chunk(self, response: aiohttp.ClientResponse) -> bytes | Break:
        try:
            async with asyncio.timeout(self._following.silence):
                return await response.content.readany()
        except TimeoutError:
            return Break.SILENT
        except aiohttp.ClientError, OSError:
            return Break.DROPPED

    async def aclose(self) -> None:
        """Stop following and let the connection go."""
        await self._arrivals.aclose()

    async def __aenter__(self) -> Self:
        """Return the stream, to be closed when the block ends."""
        return self

    async def __aexit__(
        self,
        kind: type[BaseException] | None,
        error: BaseException | None,
        trace: TracebackType | None,
    ) -> None:
        """Close the stream."""
        await self.aclose()


async def admit_async(
    address: Address,
    password: str,
    *,
    name: str | None = None,
    session: aiohttp.ClientSession | None = None,
) -> _wire.Admitted:
    """Offer a password, once, and come away with a session or with why there is none.

    A household member gives their `name`; the operator gives none. The session's
    credential is what an `AsyncClient` is then built with. The offer waits as
    long as a client's call does by default; `asyncio.timeout` around it waits less.
    """
    call = _wire.session_call(password, name)
    tls = tls_for(address)
    limit = aiohttp.ClientTimeout(total=_wire.DEFAULT_TIMEOUT)
    if session is not None:
        return _wire.admitted_of(await exchange(checked(session), address, tls, call, limit))
    async with aiohttp.ClientSession() as opened:
        return _wire.admitted_of(await exchange(opened, address, tls, call, limit))
