# Copyright (c) 2026 NightWorksIO
"""A stand-in stack: a real TLS server on loopback, with a certificate a pin names, answering as a test tells it.

It runs on the test's own event loop, beside Home Assistant, and records every
request that arrives. Reads are answered from replies a test queues; the event
stream is fed one event at a time, so a test decides when the stack speaks, when
it goes quiet and when it lets go.
"""

import asyncio
import hashlib
import json
import socket
import ssl
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Final, Self

import trustme
from aiohttp import web

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping
    from types import TracebackType

API_VERSION: Final = 1
LET_GO: Final = "Error on transport creation for incoming connection"
"""What the event loop says when a client lets a connection go while the stand-in is still accepting it."""
LOOPBACK: Final = "127.0.0.1"
HEARTBEAT: Final = b": heartbeat\n\n"


def envelope(kind: str, data: object, version: int = API_VERSION) -> dict[str, object]:
    """Return an envelope as lemonfiber writes one."""
    return {"api_version": version, "kind": kind, "data": data}


def problem(code: str, summary: str) -> dict[str, object]:
    """Return an `error` envelope carrying one problem."""
    return envelope(
        "error",
        {
            "code": code,
            "severity": "error",
            "state": "open",
            "summary": summary,
            "meaning": "",
            "remedies": [],
        },
    )


def event(kind: str, data: object, event_id: str | None = None, version: int = API_VERSION) -> bytes:
    """Return one server-sent event carrying an envelope, as lemonfiber writes one."""
    lines = [] if event_id is None else [f"id: {event_id}"]
    lines += [f"event: {kind}", f"data: {json.dumps(envelope(kind, data, version))}", "", ""]
    return "\n".join(lines).encode()


@dataclass(frozen=True)
class Reply:
    """One answer to a read: a status and a body."""

    status: int = 200
    body: object = None

    def response(self) -> web.Response:
        """Return the answer as aiohttp sends it."""
        if isinstance(self.body, str):
            return web.Response(status=self.status, text=self.body)
        return web.Response(
            status=self.status,
            body=json.dumps(self.body).encode(),
            content_type="application/json",
        )


END: Final = b""
"""Fed to a stream, it ends the stream as the server closing it."""


@dataclass
class Feed:
    """An opening of the event stream, written to as a test feeds it."""

    queue: asyncio.Queue[bytes] = field(default_factory=asyncio.Queue[bytes])

    def say(self, *chunks: bytes) -> None:
        """Send these chunks on the stream, in order."""
        for chunk in chunks:
            self.queue.put_nowait(chunk)

    def end(self) -> None:
        """Close the stream from the server's side."""
        self.queue.put_nowait(END)


class Stack:
    """A loopback TLS server answering each path with the replies it was given, in order, the last from then on."""

    def __init__(self) -> None:
        """Make a certificate of the stand-in's own, and the pin that names it."""
        self.arrived: list[tuple[str, str, Mapping[str, str]]] = []
        self.feeds: list[Feed] = []
        self._replies: dict[str, list[Reply | Feed]] = {}
        authority = trustme.CA()
        issued = authority.issue_cert(LOOPBACK, "localhost")
        self._context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        with issued.private_key_and_cert_chain_pem.tempfile() as path:
            self._context.load_cert_chain(path)
        der = ssl.PEM_cert_to_DER_cert(issued.cert_chain_pems[0].bytes().decode())
        self.pin = hashlib.sha256(der).hexdigest()
        self.port = 0
        self._runner: web.AppRunner | None = None
        self._handler: Callable[[asyncio.AbstractEventLoop, dict[str, Any]], object] | None = None

    @property
    def url(self) -> str:
        """Return the address the stand-in serves at."""
        return f"https://{LOOPBACK}:{self.port}"

    def reply(self, path: str, *replies: Reply | Feed) -> None:
        """Answer a path with these replies in turn, the last one from then on."""
        self._replies[path] = list(replies)

    def stream(self, *feeds: Feed | Reply) -> None:
        """Open the event stream as each feed in turn, the last one for every later opening; a reply refuses it."""
        self.reply("/api/events", *feeds)

    def asked(self, path: str) -> int:
        """Return how many times a path was asked for."""
        return sum(1 for _, arrived, _ in self.arrived if arrived == path)

    async def _handle(self, request: web.Request) -> web.StreamResponse:
        self.arrived.append((request.method, request.path, dict(request.headers)))
        queued = self._replies.get(request.path)
        if not queued:
            return web.Response(status=599, text="the stand-in was not told how to answer this")
        reply = queued.pop(0) if len(queued) > 1 else queued[0]
        if isinstance(reply, Feed):
            return await self._follow(request, reply)
        return reply.response()

    async def _follow(self, request: web.Request, feed: Feed) -> web.StreamResponse:
        self.feeds.append(feed)
        response = web.StreamResponse(headers={"Content-Type": "text/event-stream"})
        await response.prepare(request)
        while (chunk := await feed.queue.get()) != END:
            await response.write(chunk)
        return response

    def _accepting(self, loop: asyncio.AbstractEventLoop, context: dict[str, Any]) -> None:
        """Pass on every failure the event loop reports but a client letting go of a connection being accepted.

        A test that ends while a request is still connecting cancels it, and the
        connection is cut on the stand-in's side mid-handshake: that is how the
        integration lets go, not a failure of the test.
        """
        if str(context.get("message", "")).startswith(LET_GO) and isinstance(
            context.get("exception"),
            ConnectionError | ssl.SSLError,
        ):
            return
        if self._handler is None:
            loop.default_exception_handler(context)
        else:
            self._handler(loop, context)

    async def __aenter__(self) -> Self:
        """Start serving."""
        loop = asyncio.get_running_loop()
        self._handler = loop.get_exception_handler()
        loop.set_exception_handler(self._accepting)
        application = web.Application()
        application.router.add_route("*", "/{tail:.*}", self._handle)
        self._runner = web.AppRunner(application, access_log=None, shutdown_timeout=0.1)
        await self._runner.setup()
        site = web.TCPSite(self._runner, LOOPBACK, 0, ssl_context=self._context)
        await site.start()
        self.port = int(self._runner.addresses[0][1])
        return self

    async def __aexit__(
        self,
        kind: type[BaseException] | None,
        error: BaseException | None,
        trace: TracebackType | None,
    ) -> None:
        """Stop serving, ending every stream still open."""
        for feed in self.feeds:
            feed.end()
        if self._runner is not None:
            await self._runner.cleanup()
        asyncio.get_running_loop().set_exception_handler(self._handler)


def unused_port() -> int:
    """Return a loopback port nothing listens on."""
    with socket.socket() as probe:
        probe.bind((LOOPBACK, 0))
        return int(probe.getsockname()[1])
