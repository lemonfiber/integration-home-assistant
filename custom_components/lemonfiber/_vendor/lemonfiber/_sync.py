# Copyright (c) 2026 NightWorksIO
"""The synchronous client, on urllib3.

A pinned address is reached through a connection pool holding the pin as
`assert_fingerprint`: urllib3 compares the certificate's SHA-256 digest with it
once the handshake completes and before a byte of the request is written, and
refuses the connection where they differ (`ARCH-R99`). The pool is built here
from the address alone, so no argument reaches the transport's options.
"""

import time
from typing import TYPE_CHECKING, Final, Self

import urllib3
import urllib3.exceptions

from lemonfiber import _wire
from lemonfiber.jobs import Ended, Finished, Running
from lemonfiber.problems import CertificateRefusedError, LemonfiberError, UnreachableError
from lemonfiber.stream import FIRST_WAIT, OPENED, RECONNECTS_ALLOWED, SILENCE_ALLOWED, Break, Following

if TYPE_CHECKING:
    from collections.abc import Generator, Iterator, Mapping, Sequence
    from types import TracebackType

    from lemonfiber._generated import Envelope, JobEnvelope
    from lemonfiber.address import Address, Route
    from lemonfiber.capabilities import CapabilitySet
    from lemonfiber.credential import Credential
    from lemonfiber.jobs import JobStanding
    from lemonfiber.reads import Read
    from lemonfiber.stream import Arrival, Live, Stale

CHUNK: Final = 65536
"""The most bytes one read of the stream asks for."""


VERIFYING: Final = "CERT_REQUIRED"
"""A certificate a trust store vouches for, as an unpinned https address is held to."""

NOT_VERIFYING: Final = "CERT_NONE"
"""No trust store asked, as a pinned address is held to its pin alone, whatever the store would say."""


type Way = tuple[Route, urllib3.HTTPConnectionPool]
"""One route to a stack, and the pool its connections are kept in."""


def pool_for(address: Address, route: Route, timeout: float) -> urllib3.HTTPConnectionPool:
    """Return the pool a route is reached through, holding the address's pin where it has one.

    A route that reaches a named stack by an address it resolved to checks the
    certificate against that name, and names it in the TLS handshake.
    """
    limit = urllib3.Timeout(total=timeout)
    if address.scheme == "http":
        return urllib3.HTTPConnectionPool(route.host, address.port, timeout=limit)
    if address.pin is None:
        return urllib3.HTTPSConnectionPool(
            route.host,
            address.port,
            timeout=limit,
            cert_reqs=VERIFYING,
            assert_hostname=route.named,
            server_hostname=route.named,
        )
    return urllib3.HTTPSConnectionPool(
        route.host,
        address.port,
        timeout=limit,
        cert_reqs=NOT_VERIFYING,
        assert_fingerprint=address.pin.hex,
    )


def ways_to(address: Address, timeout: float) -> list[Way]:
    """Return every route to a stack, each with its pool, in the order they are tried."""
    return [(route, pool_for(address, route, timeout)) for route in address.routes]


def attempt(way: Way, prefix: str, call: _wire.Call) -> _wire.Answer | None:
    """Send one call over one route, or return nothing where no connection could be made there.

    A failure is raised once urllib3's error is let go, so nothing of the
    request, its credential included, rides along as the failure's cause.
    """
    route, pool = way
    try:
        response = pool.urlopen(
            call.method,
            prefix + call.path,
            body=call.body,
            headers={**call.headers, **route.headers()},
            retries=False,
        )
    except urllib3.exceptions.SSLError:
        failure: LemonfiberError = CertificateRefusedError(_wire.CERTIFICATE_REFUSED)
    except urllib3.exceptions.NewConnectionError:
        return None
    except urllib3.exceptions.HTTPError:
        failure = UnreachableError(_wire.NOT_ANSWERING)
    else:
        headers = {name.lower(): value for name, value in response.headers.items()}
        return _wire.Answer(response.status, headers, response.data)
    raise failure


def exchange(ways: Sequence[Way], prefix: str, call: _wire.Call) -> _wire.Answer:
    """Send one call over the first route a connection can be made on, following no redirect.

    A route is passed over only where no connection could be made, so nothing
    was sent; once a connection is made, its outcome is the call's.
    """
    for way in ways:
        answer = attempt(way, prefix, call)
        if answer is not None:
            return answer
    raise UnreachableError(_wire.NOT_ANSWERING)


def close_all(ways: Sequence[Way]) -> None:
    """Close every pool a client holds."""
    for _, pool in ways:
        pool.close()


class SyncClient:
    """Talks to one stack, synchronously, with one credential.

    Every answer is read through the envelope, so a version this package does
    not speak is refused rather than half understood; every refusal is a typed
    `LemonfiberError`.
    """

    def __init__(
        self,
        address: Address,
        credential: Credential,
        *,
        timeout: float = _wire.DEFAULT_TIMEOUT,
    ) -> None:
        """Hold an address and a credential; nothing is sent until a call is made."""
        self._address = address
        self._credential = credential
        self._ways = ways_to(address, timeout)

    @property
    def address(self) -> Address:
        """Return where this client sends, and the pin it holds that address to."""
        return self._address

    def _answer(self, call: _wire.Call) -> _wire.Answer:
        return exchange(self._ways, self._address.prefix, _wire.with_credential(call, self._credential))

    def read(self, read: Read, query: _wire.Query | None = None) -> Envelope:
        """Ask for what a command prints under `--json`."""
        return _wire.envelope_of(self._answer(_wire.read_call(read, query)))

    def capabilities(self) -> CapabilitySet:
        """Ask what the stack can do, for the credential this client holds, as it stands now."""
        return _wire.capabilities_of(self._answer(_wire.capabilities_call()))

    def logs(self, query: _wire.Query | None = None) -> list[Envelope]:
        """Ask for what the services have been saying, a `log` envelope a line."""
        return _wire.envelopes_of(self._answer(_wire.logs_call(query)))

    def bundle(self, name: str) -> _wire.Bundle:
        """Fetch one support bundle this run wrote, by name, as the bytes it is."""
        return _wire.bundle_of(name, self._answer(_wire.bundle_call(name)))

    def act(self, action: str, arguments: Mapping[str, _wire.Json] | None = None) -> Envelope:
        """Tell lemonfiber to do something the command line could also do. Sent once, never retried."""
        return _wire.envelope_of(self._answer(_wire.action_call(action, arguments)))

    def job(self, job: str) -> JobStanding:
        """Ask where the work a name stands for got to."""
        return _wire.standing_of(job, self._answer(_wire.job_call(job, "GET")))

    def release(self, job: str) -> JobStanding:
        """Let a name go, ending the work it stands for, and say where it now stands."""
        return _wire.standing_of(job, self._answer(_wire.job_call(job, "DELETE")))

    def follow(
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
        started = time.monotonic()
        standing = self.job(name)
        while isinstance(standing, Running):
            time.sleep(_wire.next_wait(name, started, time.monotonic(), every, within))
            standing = self.job(name)
        return standing

    def events(
        self,
        *,
        silence: float = SILENCE_ALLOWED,
        reconnects: int = RECONNECTS_ALLOWED,
        first_wait: float = FIRST_WAIT,
    ) -> SyncStream:
        """Follow the live stream: what arrives, what has gone stale across a gap, and each gap itself.

        Silence longer than `silence` seconds is a broken stream. A broken stream
        is reopened from the last event it carried, waiting `first_wait` seconds
        and twice as long after each failure, and `StreamLostError` is raised once
        `reconnects` attempts in a row have failed.
        """
        following = Following(self._credential, silence=silence, reconnects=reconnects, first_wait=first_wait)
        return SyncStream(self._ways, self._address.prefix, following)

    def close(self) -> None:
        """Close every connection this client holds."""
        close_all(self._ways)

    def __enter__(self) -> Self:
        """Return the client, to be closed when the block ends."""
        return self

    def __exit__(
        self,
        kind: type[BaseException] | None,
        error: BaseException | None,
        trace: TracebackType | None,
    ) -> None:
        """Close the client."""
        self.close()


class SyncStream:
    """The live stream, followed synchronously. Iterate it for each `Arrival`; close it to let go."""

    def __init__(
        self,
        ways: Sequence[Way],
        prefix: str,
        following: Following,
    ) -> None:
        """Hold what opening and reading the stream needs; nothing is sent until it is iterated."""
        self._ways = ways
        self._prefix = prefix
        self._following = following
        self._response: urllib3.BaseHTTPResponse | None = None
        self._arrivals = self._follow()

    def __iter__(self) -> Iterator[Arrival]:
        """Return the stream itself."""
        return self

    def __next__(self) -> Arrival:
        """Return the next arrival, waiting for it."""
        return next(self._arrivals)

    def held(self) -> dict[str, Live | Stale]:
        """Return the last value of each kind the stream carried, and whether it is still current."""
        return self._following.held()

    def _follow(self) -> Generator[Arrival]:
        while True:
            response = self._open()
            if response is not None:
                self._response = response
                self._following.opened()
                why = yield from self._read(response)
                response.drain_conn()
                response.release_conn()
                self._response = None
                yield from self._following.broke(why)
            time.sleep(self._following.retry())

    def _open(self) -> urllib3.BaseHTTPResponse | None:
        call = self._following.call()
        for way in self._ways:
            response = self._attempt(way, call)
            if response is not None:
                return self._judged(response)
        return None

    def _attempt(self, way: Way, call: _wire.Call) -> urllib3.BaseHTTPResponse | None:
        """Ask for the stream over one route: the response, or nothing where none came back.

        A certificate the stack does not hold to is raised; anything else leaves
        the next route, or the next attempt, to try.
        """
        route, pool = way
        try:
            response = pool.urlopen(
                call.method,
                self._prefix + call.path,
                headers={**call.headers, **route.headers()},
                retries=False,
                preload_content=False,
                timeout=urllib3.Timeout(connect=pool.timeout.connect_timeout, read=self._following.silence),
            )
        except urllib3.exceptions.SSLError:
            failure = CertificateRefusedError(_wire.CERTIFICATE_REFUSED)
        except urllib3.exceptions.HTTPError:
            return None
        else:
            return response
        raise failure

    @staticmethod
    def _judged(response: urllib3.BaseHTTPResponse) -> urllib3.BaseHTTPResponse | None:
        """Return a response that opened the stream, raising the refusal where the stack answered with one."""
        if response.status == OPENED:
            return response
        headers = {name.lower(): value for name, value in response.headers.items()}
        answer = _wire.Answer(response.status, headers, response.read())
        response.release_conn()
        refusal = _wire.opening_refusal(answer)
        if refusal is not None:
            raise refusal
        return None

    def _read(self, response: urllib3.BaseHTTPResponse) -> Generator[Arrival, None, Break]:
        while True:
            try:
                chunk = response.read1(CHUNK)
            except urllib3.exceptions.ReadTimeoutError:
                return Break.SILENT
            except urllib3.exceptions.HTTPError, OSError:
                return Break.DROPPED
            if not chunk:
                return Break.ENDED
            yield from self._following.heard(chunk)

    def close(self) -> None:
        """Stop following and let the connection go."""
        self._arrivals.close()
        if self._response is not None:
            self._response.close()
            self._response = None

    def __enter__(self) -> Self:
        """Return the stream, to be closed when the block ends."""
        return self

    def __exit__(
        self,
        kind: type[BaseException] | None,
        error: BaseException | None,
        trace: TracebackType | None,
    ) -> None:
        """Close the stream."""
        self.close()


def admit(
    address: Address,
    password: str,
    *,
    name: str | None = None,
    timeout: float = _wire.DEFAULT_TIMEOUT,
) -> _wire.Admitted:
    """Offer a password, once, and come away with a session or with why there is none.

    A household member gives their `name`; the operator gives none. The session's
    credential is what a `SyncClient` is then built with.
    """
    ways = ways_to(address, timeout)
    try:
        return _wire.admitted_of(exchange(ways, address.prefix, _wire.session_call(password, name)))
    finally:
        close_all(ways)
