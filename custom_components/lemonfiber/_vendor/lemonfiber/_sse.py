# Copyright (c) 2026 NightWorksIO
"""The `text/event-stream` wire format, read a chunk at a time."""

import codecs
from dataclasses import dataclass, field
from typing import Final

from lemonfiber.problems import UnreadableResponseError

LARGEST: Final = 16 * 1024 * 1024
"""The most characters one event's data, or one line of it, may hold."""

NONE_LEFT: Final = -1
"""What a search for a line ending finds where the text holds no more of them."""

NOT_LOOKED: Final = -2
"""Where a line ending is before it has been looked for."""


@dataclass(frozen=True, slots=True)
class Event:
    """One event as the stream carried it: its id, its name and its data."""

    id: str | None
    name: str
    data: str


@dataclass(slots=True)
class _Pending:
    id: str | None = None
    name: str = "message"
    data: list[str] = field(default_factory=list[str])
    size: int = 0
    """The characters the data holds once joined, and one more."""


class Parser:
    """Gathers chunks and hands back each event as it completes.

    A chunk may end inside a line and a line inside a UTF-8 sequence, so bytes
    are held until they decode, text until a line ends, and an event until a
    blank line ends it. A comment line is the heartbeat and carries nothing.
    An unfinished line is held as the pieces it arrived in and joined once it
    ends, so a long line is not copied again with every chunk.

    Nothing held grows past `largest` characters: a line that has not ended,
    or the data of an event that has not completed, beyond that is refused as
    `UnreadableResponseError` rather than held, and each character is looked
    at a bounded number of times, however the stream is cut into chunks.
    """

    def __init__(self, *, largest: int = LARGEST) -> None:
        """Start with nothing gathered, holding no line or event beyond `largest` characters."""
        self._largest = largest
        self._decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")
        self._unfinished: list[str] = []
        self._unfinished_size = 0
        self._pending = _Pending()

    def push(self, chunk: bytes) -> list[Event]:
        """Return the events this chunk completes, in order."""
        decoded = self._decoder.decode(chunk)
        waiting = bool(self._unfinished) and self._unfinished[-1].endswith("\r")
        if waiting or "\n" in decoded or "\r" in decoded:
            done = self._lines("".join([*self._unfinished, decoded]))
        else:
            self._unfinished.append(decoded)
            self._unfinished_size += len(decoded)
            done = []
        if self._unfinished_size > self._largest:
            what = f"the stream carried a line longer than the {self._largest} characters an event may be"
            raise UnreadableResponseError(what)
        return done

    def _lines(self, text: str) -> list[Event]:
        """Read every line a text completes, keeping the line it has not finished."""
        done: list[Event] = []
        lines = Lines(text)
        start = 0
        while (end := lines.end_after(start)) is not None:
            event = self._line(text[start : end[0]])
            if event is not None:
                done.append(event)
            start = end[1]
        rest = text[start:]
        self._unfinished = [rest] if rest else []
        self._unfinished_size = len(rest)
        return done

    def _line(self, line: str) -> Event | None:
        if not line:
            return self._complete()
        if line.startswith(":"):
            return None
        name, _, value = line.partition(":")
        value = value.removeprefix(" ")
        if name == "id":
            self._pending.id = value
        elif name == "event":
            self._pending.name = value
        elif name == "data":
            self._pending.data.append(value)
            self._pending.size += len(value) + 1
            if self._pending.size > self._largest + 1:
                what = (
                    f"the stream carried an event larger than the {self._largest} characters an event may be"
                )
                raise UnreadableResponseError(what)
        return None

    def _complete(self) -> Event | None:
        pending, self._pending = self._pending, _Pending()
        if not pending.data:
            return None
        return Event(pending.id, pending.name, "\n".join(pending.data))


class Lines:
    """Finds where each line of a text ends, looking at each character once.

    The next line feed and the next carriage return are each found once and
    kept until the reading passes them, so a text of many lines is not searched
    again from every line's start.
    """

    def __init__(self, text: str) -> None:
        """Hold the text, with neither ending yet looked for."""
        self._text = text
        self._feed = NOT_LOOKED
        self._return = NOT_LOOKED

    def end_after(self, start: int) -> tuple[int, int] | None:
        """Return where the first line at or after `start` ends and where the next begins, if it has ended."""
        self._feed = feed = self._next(self._feed, "\n", start)
        self._return = back = self._next(self._return, "\r", start)
        if back == NONE_LEFT or NONE_LEFT < feed < back:
            return None if feed == NONE_LEFT else (feed, feed + 1)
        if back + 1 == len(self._text):
            return None
        return back, back + 2 if self._text[back + 1] == "\n" else back + 1

    def _next(self, found: int, ending: str, start: int) -> int:
        """Return the next `ending` at or after `start`, searching again only where the one found is behind it."""
        if found == NOT_LOOKED or NONE_LEFT < found < start:
            return self._text.find(ending, start)
        return found
