# Copyright (c) 2026 NightWorksIO
"""The synchronous client, on urllib3.

A pinned address is reached through a connection pool holding the pin as
`assert_fingerprint`: urllib3 compares the certificate's SHA-256 digest with it
once the handshake completes and before a byte of the request is written, and
refuses the connection where they differ. The pool is built in `transport` from the
address alone, so no argument reaches the transport's options.
"""

import time
from typing import TYPE_CHECKING, Self, overload

import urllib3
import urllib3.exceptions

from lemonfiber._protocol import operation
from lemonfiber._protocol.calls import (
    DEFAULT_TIMEOUT,
    REFERENCE,
    TITLE,
    Call,
    received,
    with_credential,
)
from lemonfiber._protocol.following import DEFAULT_EVERY, job_name, next_wait
from lemonfiber._protocol.refusals import CERTIFICATE_REFUSED, LAPSED, opening_refusal
from lemonfiber._protocol.retry import Attempts
from lemonfiber.jobs import Ended, Finished, Running
from lemonfiber.problems import CertificateRefusedError, ClaimLapsedError
from lemonfiber.reads import ASKABLE_ID_POSTER, HELD_ID_BACKDROP, HELD_ID_POSTER, REQUESTS_REFERENCE_POSTER
from lemonfiber.stream import FIRST_WAIT, OPENED, RECONNECTS_ALLOWED, SILENCE_ALLOWED, Break, Following

if TYPE_CHECKING:
    from collections.abc import Generator, Iterator, Mapping, Sequence
    from types import TracebackType

    from lemonfiber._generated import (
        ActionName,
        ActionRequest,
        DeviceChallengeEnvelope,
        DeviceKeyEnvelope,
        DeviceKeysEnvelope,
        Envelope,
        JobEnvelope,
        KeyClaimEnvelope,
        KeysEnvelope,
        LogEnvelope,
        MintedKey,
        MintedKeyEnvelope,
        PushEndpointEnvelope,
        PushEndpointsEnvelope,
    )
    from lemonfiber._protocol.calls import Json, Query
    from lemonfiber._sync.transport import Way
    from lemonfiber.address import Address
    from lemonfiber.capabilities import CapabilitySet
    from lemonfiber.credential import Credential, Session
    from lemonfiber.device_keys import Registering
    from lemonfiber.files import BundleFile, Picture
    from lemonfiber.jobs import JobStanding
    from lemonfiber.keys import KeyLink, Minting
    from lemonfiber.push_endpoints import PushEndpointRegistering
    from lemonfiber.reads import Read
    from lemonfiber.stream import Arrival, Live, Stale

from lemonfiber._sync.transport import CHUNK, asked, close_all, exchange, ways_to


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
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        """Hold an address and a credential; nothing is sent until a call is made."""
        self._address = address
        self._credential = credential
        self._timeout = timeout
        self._ways = ways_to(address)

    @property
    def address(self) -> Address:
        """Return where this client sends, and the pin it holds that address to."""
        return self._address

    def _run[T](self, operated: operation.Operation[T]) -> T:
        call = with_credential(operated.call, self._credential)
        attempts = Attempts(operated.again, self._timeout, time.monotonic())
        return operated.read(asked(self._ways, self._address.prefix, call, attempts))

    def read(self, read: Read, query: Query | None = None) -> Envelope:
        """Ask for what a command prints under `--json`."""
        return self._run(operation.reading(read, query))

    def capabilities(self) -> CapabilitySet:
        """Ask what the stack can do, for the credential this client holds, as it stands now."""
        return self._run(operation.capabilities())

    def logs(
        self,
        *,
        services: Sequence[str] = (),
        forms: Sequence[str] = (),
        tail: int | None = None,
    ) -> list[LogEnvelope]:
        """Ask for what the services have been saying, a `log` envelope a line.

        `services` and `forms` narrow to those named; `tail` is how many of the
        latest lines to answer with. Each left out is left to lemonfiber, as the
        command leaves a flag it was not given.
        """
        return self._run(operation.logs(services, forms, tail))

    def bundle(self, name: str) -> BundleFile:
        """Fetch one support bundle this run wrote, by name, as the bytes it is."""
        return self._run(operation.bundle(name))

    def poster(self, title: str, query: Query | None = None) -> Picture:
        """Fetch a title's poster, by the id its shelf lists it under, as the raster image it is.

        `query` takes `member` and `defaults`, as the title read does. A title outside
        the member's limits is `PLAY-2`, and one with no poster is `PLAY-9`.
        """
        return self._run(operation.picture(HELD_ID_POSTER, TITLE, title, query))

    def backdrop(self, title: str, query: Query | None = None) -> Picture:
        """Fetch a title's backdrop, as `poster` fetches its poster."""
        return self._run(operation.picture(HELD_ID_BACKDROP, TITLE, title, query))

    def askable_poster(self, title: str, query: Query | None = None) -> Picture:
        """Fetch the poster of a title a member may ask for, by the id their search lists it under.

        `query` takes `member`, `kind` and, for music or books, `unit`. A title the member may not
        ask for is `WISH-3`, and one with no poster is `WISH-13`.
        """
        return self._run(operation.picture(ASKABLE_ID_POSTER, TITLE, title, query))

    def request_poster(self, reference: str, query: Query | None = None) -> Picture:
        """Fetch the cover of an ask for music or books the core keeps, by the reference the household list names it by.

        `query` takes `member`. A reference no kept ask goes by, or another member's, is `WISH-3`,
        and an ask with no cover is `WISH-13`.
        """
        return self._run(operation.picture(REQUESTS_REFERENCE_POSTER, REFERENCE, reference, query))

    @overload
    def act(self, action: ActionRequest) -> Envelope: ...
    @overload
    def act(self, action: ActionName, arguments: Mapping[str, Json] | None = None) -> Envelope: ...
    def act(
        self,
        action: ActionRequest | ActionName,
        arguments: Mapping[str, Json] | None = None,
    ) -> Envelope:
        """Tell lemonfiber to do something the command line could also do. Sent once, never retried.

        `action` is a request, its arguments typed as the contract types that action's, or an action the
        contract lists by name with `arguments` beside it.
        """
        return self._run(operation.action(action, arguments))

    def keys(self) -> KeysEnvelope:
        """Ask for the integration keys this credential may see, without their secrets."""
        return self._run(operation.keys())

    def mint(self, minting: Minting) -> MintedKeyEnvelope:
        """Mint one integration key, its secret in this answer and in no other. Sent once, never retried."""
        return self._run(operation.mint(minting))

    def mint_claim(self, minting: Minting) -> KeyClaimEnvelope:
        """Mint one integration key as a claim, answered with the key link that collects it and no secret."""
        return self._run(operation.mint_claim(minting))

    def revoke(self, name: str) -> KeysEnvelope:
        """Revoke one integration key by its name, answered with the keys as they now stand."""
        return self._run(operation.revoke(name))

    def register_device_key(self, registering: Registering) -> DeviceKeyEnvelope:
        """Register a phone's key pair as a device key. Sent once, never retried."""
        return self._run(operation.register_device_key(registering))

    def device_keys(self) -> DeviceKeysEnvelope:
        """Ask for the operator's device keys, revoked ones included."""
        return self._run(operation.device_keys())

    def device_key_challenge(self, name: str) -> DeviceChallengeEnvelope:
        """Ask a challenge for one device key, good for one mint within a minute. Sent once."""
        return self._run(operation.device_key_challenge(name))

    def revoke_device_key(self, name: str) -> DeviceKeysEnvelope:
        """Revoke one device key by its name; the keys it proved stay. Sent once, never retried."""
        return self._run(operation.revoke_device_key(name))

    def register_push_endpoint(self, registering: PushEndpointRegistering) -> PushEndpointEnvelope:
        """Register a phone's push endpoint, answered with the endpoint as registered. Sent once."""
        return self._run(operation.register_push_endpoint(registering))

    def push_endpoints(self) -> PushEndpointsEnvelope:
        """Return every push endpoint this credential keeps: all for the operator, a member's own for a member."""
        return self._run(operation.push_endpoints())

    def remove_push_endpoint(self, name: str) -> PushEndpointsEnvelope:
        """Remove one push endpoint by its name, answered with the endpoints as they now stand. Sent once."""
        return self._run(operation.remove_push_endpoint(name))

    def job(self, job: str) -> JobStanding:
        """Ask where the work a name stands for got to."""
        return self._run(operation.job(job))

    def release(self, job: str) -> JobStanding:
        """Let a name go, ending the work it stands for, and say where it now stands."""
        return self._run(operation.release(job))

    def forget(self, job: str) -> JobStanding:
        """Let a name go, leaving the work it stands for running, and say where that work stood. Sent once."""
        return self._run(operation.forget(job))

    def follow(
        self,
        job: str | JobEnvelope,
        *,
        every: float = DEFAULT_EVERY,
        within: float | None = None,
    ) -> Finished | Ended:
        """Ask where work stands every `every` seconds until it is no longer going.

        Raises `StillRunningError` once `within` seconds have passed with it still going.
        """
        name = job_name(job)
        started = time.monotonic()
        standing = self.job(name)
        while isinstance(standing, Running):
            time.sleep(next_wait(name, started, time.monotonic(), every, within))
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
        return SyncStream(self._ways, self._address.prefix, following, self._timeout)

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
        connect: float = DEFAULT_TIMEOUT,
    ) -> None:
        """Hold what opening and reading the stream needs; nothing is sent until it is iterated."""
        self._ways = ways
        self._prefix = prefix
        self._following = following
        self._connect = connect
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
                self._following.opened()
                try:
                    why = yield from self._read(response)
                except BaseException:
                    response.close()
                    raise
                response.drain_conn()
                response.release_conn()
                yield from self._following.broke(why)
            time.sleep(self._following.retry())

    def _open(self) -> urllib3.BaseHTTPResponse | None:
        call = self._following.call()
        for way in self._ways:
            response = self._attempt(way, call)
            if response is not None:
                return self._judged(response)
        return None

    def _attempt(self, way: Way, call: Call) -> urllib3.BaseHTTPResponse | None:
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
                timeout=urllib3.Timeout(connect=self._connect, read=self._following.silence),
            )
        except urllib3.exceptions.SSLError:
            failure = CertificateRefusedError(CERTIFICATE_REFUSED)
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
        answer = received(response.status, response.headers, response.read())
        response.release_conn()
        refusal = opening_refusal(answer)
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
    timeout: float = DEFAULT_TIMEOUT,
) -> Session:
    """Offer a password, once, and come away with a session or with why there is none.

    A household member gives their `name`; the operator gives none. The session's
    credential is what a `SyncClient` is then built with.
    """
    offered = operation.admission(password, name)
    ways = ways_to(address)
    try:
        return offered.read(exchange(ways, address.prefix, offered.call, timeout))
    finally:
        close_all(ways)


def collect(link: KeyLink, *, timeout: float = DEFAULT_TIMEOUT) -> MintedKey:
    """Collect the key a key link's claim was minted for, once, over the TLS the link's fingerprint verifies.

    The claim is sent alone, with no credential. A claim already lapsed is
    refused before anything is sent; one the stack turns away is a
    `ClaimRefusedError`. The answer carries the key's secret, and nothing here
    keeps it.
    """
    if link.lapsed():
        raise ClaimLapsedError(LAPSED)
    collecting = operation.collection(link.claim)
    ways = ways_to(link.address)
    try:
        return collecting.read(exchange(ways, link.address.prefix, collecting.call, timeout))
    finally:
        close_all(ways)
