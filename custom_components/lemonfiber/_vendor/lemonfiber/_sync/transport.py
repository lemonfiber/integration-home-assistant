# Copyright (c) 2026 NightWorksIO
"""Sending one call to a stack over urllib3: each route in turn, its pin or verifying context, no proxy, no redirect."""

import time
from typing import TYPE_CHECKING, Final

import urllib3
import urllib3.exceptions

from lemonfiber._protocol.calls import Answer, Call, declared_over, received
from lemonfiber._protocol.refusals import CERTIFICATE_REFUSED, NOT_ANSWERING
from lemonfiber.problems import CertificateRefusedError, LemonfiberError, UnreachableError

if TYPE_CHECKING:
    from collections.abc import Sequence

    from lemonfiber._protocol.retry import Attempts
    from lemonfiber.address import Address, Route


CHUNK: Final = 65536
"""The most bytes one read of the stream asks for, so a chunk the server declares larger is not held whole."""


VERIFYING: Final = "CERT_REQUIRED"
"""A certificate a trust store vouches for, as an unpinned https address is held to."""

NOT_VERIFYING: Final = "CERT_NONE"
"""No trust store asked, as a pinned address is held to its pin alone, whatever the store would say."""


type Way = tuple[Route, urllib3.HTTPConnectionPool]
"""One route to a stack, and the pool its connections are kept in."""


def pool_for(address: Address, route: Route) -> urllib3.HTTPConnectionPool:
    """Return the pool a route is reached through, holding the address's pin where it has one.

    A route that reaches a named stack by an address it resolved to checks the
    certificate against that name, and names it in the TLS handshake. How long
    a request waits is given with each request, so the pool holds no timeout.
    """
    if address.scheme == "http":
        return urllib3.HTTPConnectionPool(route.host, address.port)
    if address.pin is None:
        return urllib3.HTTPSConnectionPool(
            route.host,
            address.port,
            cert_reqs=VERIFYING,
            assert_hostname=route.named,
            server_hostname=route.named,
        )
    return urllib3.HTTPSConnectionPool(
        route.host,
        address.port,
        cert_reqs=NOT_VERIFYING,
        assert_fingerprint=address.pin.hex,
    )


def ways_to(address: Address) -> list[Way]:
    """Return every route to a stack, each with its pool, in the order they are tried."""
    return [(route, pool_for(address, route)) for route in address.routes]


def attempt(way: Way, prefix: str, call: Call, limit: float) -> Answer | None:
    """Send one call over one route, waiting at most `limit` seconds, or return nothing where no connection could be made there.

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
            timeout=urllib3.Timeout(total=limit),
            preload_content=False,
        )
        body = response.data if call.most is None else capped(response, call.most)
    except urllib3.exceptions.SSLError:
        failure: LemonfiberError = CertificateRefusedError(CERTIFICATE_REFUSED)
    except urllib3.exceptions.NewConnectionError:
        return None
    except urllib3.exceptions.HTTPError:
        failure = UnreachableError(NOT_ANSWERING)
    else:
        return received(response.status, response.headers, body)
    raise failure


def capped(response: urllib3.BaseHTTPResponse, most: int) -> bytes:
    """Return at most one byte past `most` of an answer, and none of one that declares more.

    A connection read to its end goes back to the pool; one left part-read is closed.
    """
    if declared_over(response.headers, most):
        response.close()
        return b""
    kept = response.read(most + 1)
    if len(kept) > most:
        response.close()
    else:
        response.release_conn()
    return kept


def exchange(ways: Sequence[Way], prefix: str, call: Call, limit: float) -> Answer:
    """Send one call over the first route a connection can be made on, following no redirect.

    A route is passed over only where no connection could be made, so nothing
    was sent; once a connection is made, its outcome is the call's.
    """
    for way in ways:
        answer = attempt(way, prefix, call, limit)
        if answer is not None:
            return answer
    raise UnreachableError(NOT_ANSWERING)


def asked(ways: Sequence[Way], prefix: str, call: Call, attempts: Attempts) -> Answer:
    """Send a call, and send a read again after a passing failure, as `attempts` allows.

    The last attempt's outcome is the call's: its answer, or the failure that
    nothing answered.
    """
    while True:
        outcome: Answer | UnreachableError
        try:
            outcome = exchange(ways, prefix, call, attempts.left(time.monotonic()))
        except UnreachableError as unanswered:
            outcome = unanswered
        pause = attempts.pause(outcome if isinstance(outcome, Answer) else None, time.monotonic())
        if pause is None:
            break
        time.sleep(pause)
    if isinstance(outcome, UnreachableError):
        raise outcome
    return outcome


def close_all(ways: Sequence[Way]) -> None:
    """Close every pool a client holds."""
    for _, pool in ways:
        pool.close()
