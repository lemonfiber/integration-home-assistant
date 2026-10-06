# Copyright (c) 2026 NightWorksIO
"""What goes on the wire and what comes back, read the same way by both clients.

Nothing here performs I/O. A client turns a `Call` into a request over its own
transport and hands back an `Answer`; everything a request carries and
everything an answer means is decided here, once.
"""

import datetime
import json
import types
import urllib.parse
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Final, Literal, TypeIs, cast

from lemonfiber._generated import (
    REFUSAL_CODES,
    CapabilityState,
    Envelope,
    JobEnvelope,
    Problem,
    RefusalCode,
    is_refusal_code,
)
from lemonfiber.capabilities import CapabilitySet, is_state
from lemonfiber.credential import Credential
from lemonfiber.envelope import expect, parse_envelope
from lemonfiber.jobs import Ended, Finished, JobStanding, Running
from lemonfiber.problems import (
    BusyError,
    DeclinedError,
    FailedError,
    LemonfiberError,
    MisaskedError,
    MissingError,
    NoSuchJobError,
    NotAdmittedError,
    PasswordRefusedError,
    RefusedError,
    StillRunningError,
    TooManyAttemptsError,
    UnreachableError,
    UnreadableResponseError,
)
from lemonfiber.reads import ACTIONS, BUNDLE, CAPABILITIES, JOBS, LOGS, SESSION, Read

type Scalar = str | int | bool
"""One value a query parameter carries."""

type Query = Mapping[str, Scalar | Sequence[Scalar] | None]
"""A read's parameters. A list is the parameter once per value; `None` or an empty list sends nothing."""

type Json = bool | int | float | str | Sequence[Json] | Mapping[str, Json] | None
"""A value an action's arguments may carry."""

NOTHING_SAFE: Final = ""
"""The characters a path segment leaves unquoted beyond the unreserved ones: none."""
JSON_TYPE: Final = "application/json"
ANY_TYPE: Final = "*/*"
SUCCESS: Final = range(200, 300)
"""The statuses a success is answered with."""
NO_SUCH_NAME: Final = 404
"""The status a job name this run never issued is answered with, in prose."""
STILL_GOING: Final = 202
"""The status work still in flight is answered with."""
TURNED_AWAY: Final = frozenset({401, 403})
"""The statuses a request is turned away with for who is asking or where from."""
THE_CREDENTIAL: Final = "NOT_ADMITTED"
"""The registry name of the refusal that is the credential itself, looked up rather than its code written here."""
MEANT_BY: Final[Mapping[int, type[RefusedError]]] = {
    400: MisaskedError,
    404: MissingError,
    409: BusyError,
}
"""What a status says the request got wrong; any other status is the machine's."""
TOO_MANY: Final = 429
NOT_THE_PASSWORD: Final = 401
STRUCTURE: Final = ("{", "[", "<")
"""What opens a document rather than a sentence."""
DEFAULT_TIMEOUT: Final = 30.0
"""How many seconds a call waits for its answer, unless the client is told otherwise."""
DEFAULT_EVERY: Final = 1.0
"""How many seconds apart work being followed is asked about."""
CERTIFICATE_REFUSED: Final = "The stack's certificate is not the one pinned for it, or no trust store vouches for it, so nothing was sent."
NOT_ANSWERING: Final = "lemonfiber is not answering at that address. It may have been stopped."
NOT_ADMITTED: Final = (
    "lemonfiber does not admit the credential this client holds. Use the token it printed, sign in again, "
    "or use a key the operator minted."
)


@dataclass(frozen=True, slots=True)
class Call:
    """One request, as every transport sends it.

    Its headers carry the credential and its body may carry a password, so
    neither is shown when the call is printed.
    """

    method: str
    path: str
    headers: Mapping[str, str] = field(default_factory=dict[str, str], repr=False)
    body: bytes | None = field(default=None, repr=False)


@dataclass(frozen=True, slots=True)
class Answer:
    """One answer, as every transport hands it back: header names lower-cased."""

    status: int
    headers: Mapping[str, str]
    body: bytes


@dataclass(frozen=True, slots=True)
class Bundle:
    """A file lemonfiber handed over, kept as the bytes that arrived."""

    name: str
    content: bytes
    content_type: str | None


@dataclass(frozen=True, slots=True)
class Admitted:
    """A session opened: the credential it is carried by, when it stops being one, and whose it is.

    `member` is the household member the session is for; absent is the operator.
    """

    credential: Credential
    until: datetime.datetime
    member: str | None


def segment(name: str) -> str:
    """Write a name as one path segment, so a separator in it reaches lemonfiber as written."""
    return urllib.parse.quote(name, safe=NOTHING_SAFE)


def search(query: Query | None) -> str:
    """Return a query string, or nothing where there is nothing to ask for. The credential is never in it."""
    pairs: list[tuple[str, str]] = []
    for key, value in (query or {}).items():
        pairs.extend((key, written(one)) for one in listed(value))
    return f"?{urllib.parse.urlencode(pairs)}" if pairs else ""


def listed(value: Scalar | Sequence[Scalar] | None) -> list[Scalar]:
    """Return a query value as the values it sends: none for nothing, one for a scalar, each of a list."""
    if value is None:
        return []
    if isinstance(value, str | int):
        return [value]
    return list(value)


def written(value: Scalar) -> str:
    """Write one query value as lemonfiber reads it."""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def with_credential(call: Call, credential: Credential) -> Call:
    """Return the call carrying the credential in its header."""
    return Call(call.method, call.path, {**call.headers, **credential.header()}, call.body)


def read_call(read: Read, query: Query | None) -> Call:
    """Ask for what a command prints under `--json`."""
    return Call("GET", read.path + search(query), {"Accept": JSON_TYPE})


def capabilities_call() -> Call:
    """Ask what the stack can do, for the credential the call carries."""
    return Call("GET", CAPABILITIES, {"Accept": JSON_TYPE})


def logs_call(query: Query | None) -> Call:
    """Ask for what the services have been saying."""
    return Call("GET", LOGS + search(query), {"Accept": JSON_TYPE})


def bundle_call(name: str) -> Call:
    """Ask for one support bundle, by the name it was written under."""
    return Call("GET", f"{BUNDLE}/{segment(name)}", {"Accept": ANY_TYPE})


def action_call(name: str, arguments: Mapping[str, Json] | None) -> Call:
    """Tell lemonfiber to do something the command line could also do."""
    body = json.dumps(dict(arguments or {})).encode()
    return Call("POST", f"{ACTIONS}/{segment(name)}", {"Accept": JSON_TYPE, "Content-Type": JSON_TYPE}, body)


def job_call(job: str, method: Literal["GET", "DELETE"]) -> Call:
    """Ask where work stands with `GET`, or let its name go with `DELETE`."""
    return Call(method, f"{JOBS}/{segment(job)}", {"Accept": JSON_TYPE})


def session_call(password: str, name: str | None) -> Call:
    """Offer a password, and a household member's name where it is one, for a session."""
    offer = {"password": password} if name is None else {"name": name, "password": password}
    return Call("POST", SESSION, {"Accept": JSON_TYPE, "Content-Type": JSON_TYPE}, json.dumps(offer).encode())


REFUSED_OUTRIGHT: Final = frozenset({400, 401, 403, 404})
"""Statuses opening the stream is refused with that another attempt would only repeat."""


def opening_refusal(answer: Answer) -> LemonfiberError | None:
    """Return the refusal an answer to opening the stream is, or None where another attempt may succeed."""
    if answer.status in REFUSED_OUTRIGHT:
        return refusal_of(answer)
    return None


def succeeded(answer: Answer) -> bool:
    """Tell whether an answer is a success."""
    return answer.status in SUCCESS


def envelope_of(answer: Answer) -> Envelope:
    """Read an answer as one envelope, or raise the refusal it is."""
    if not succeeded(answer):
        raise refusal_of(answer)
    return parse_envelope(answer.body)


def envelopes_of(answer: Answer) -> list[Envelope]:
    """Read an answer of one envelope a line, or raise the refusal it is."""
    if not succeeded(answer):
        raise refusal_of(answer)
    return [parse_envelope(line) for line in answer.body.splitlines() if line.strip()]


def bundle_of(name: str, answer: Answer) -> Bundle:
    """Keep a handed-over file as it arrived, or raise the refusal it is."""
    if not succeeded(answer):
        raise refusal_of(answer)
    return Bundle(name, answer.body, answer.headers.get("content-type"))


def standing_of(job: str, answer: Answer) -> JobStanding:
    """Read where work stands from the status and the kind together."""
    if answer.status == NO_SUCH_NAME and problem_in(answer.body) is None:
        raise NoSuchJobError(job)
    envelope = envelope_of(answer)
    if envelope["kind"] != "job":
        return Finished(job, envelope)
    started = expect(envelope, "job")
    return Running(job, started) if answer.status == STILL_GOING else Ended(job, started)


def capabilities_of(answer: Answer) -> CapabilitySet:
    """Read the stack's capabilities as they stood when the answer arrived, or raise the refusal it is.

    A capability name this client does not know is kept, never refused (`ARCH-R81`); a state the
    contract does not list is not a document lemonfiber writes.
    """
    arrived = datetime.datetime.now(datetime.UTC)
    data = cast("object", expect(envelope_of(answer), "capabilities")["data"])
    held = cast("dict[str, object]", data).get("capabilities") if isinstance(data, dict) else None
    if not isinstance(held, dict):
        msg = f"the capabilities are {held!r}, and they are an object keyed by path"
        raise UnreadableResponseError(msg)
    states: dict[str, CapabilityState] = {}
    for path, state in cast("dict[object, object]", held).items():
        if not isinstance(path, str) or not is_state(state):
            msg = f"{path!r} is {state!r}, which is not a state a capability can be in"
            raise UnreadableResponseError(msg)
        states[path] = state
    return CapabilitySet(types.MappingProxyType(states), arrived)


def admitted_of(answer: Answer) -> Admitted:
    """Read the door's answer as a session, or raise why there is none."""
    if answer.status == NOT_THE_PASSWORD:
        raise PasswordRefusedError(
            sentence_in(answer.body) or "That is not the password, or none is configured.",
            status=answer.status,
            code=code_in(answer.body),
            problem=problem_in(answer.body),
        )
    data = expect(envelope_of(answer), "admission")["data"]
    return Admitted(Credential(data["token"]), instant(data["until"]), data.get("member"))


def job_name(job: str | JobEnvelope) -> str:
    """Return the name work goes by, given the name or the envelope that answered with it."""
    return job if isinstance(job, str) else job["data"]["job"]


def next_wait(job: str, started: float, now: float, every: float, within: float | None) -> float:
    """Return how long to wait before asking about work again, or raise once `within` has passed."""
    if within is None:
        return every
    waited = now - started
    if waited >= within:
        raise StillRunningError(job, waited)
    return min(every, within - waited)


def instant(written: str) -> datetime.datetime:
    """Read an instant as this product writes one, in UTC."""
    try:
        read = datetime.datetime.fromisoformat(written)
    except ValueError as unreadable:
        msg = f"{written!r} is not an instant"
        raise UnreadableResponseError(msg) from unreadable
    if read.tzinfo is None:
        return read.replace(tzinfo=datetime.UTC)
    if read.utcoffset() != datetime.timedelta(0):
        msg = f"{written!r} names an offset other than UTC"
        raise UnreadableResponseError(msg)
    return read.astimezone(datetime.UTC)


def problem_in(body: bytes) -> Problem | None:
    """Return the problem an `error` envelope carries, or None where the body is not one."""
    text = body.decode(errors="replace").strip()
    if not text.startswith(STRUCTURE):
        return None
    try:
        envelope = parse_envelope(text)
    except LemonfiberError:
        return None
    if envelope["kind"] != "error":
        return None
    data: object = expect(envelope, "error")["data"]
    return data if is_problem(data) else None


def is_problem(data: object) -> TypeIs[Problem]:
    """Tell whether an `error` envelope's data is an object, as a problem is."""
    return isinstance(data, dict)


def sentence_in(body: bytes) -> str | None:
    """Return the one sentence a refusal holds: an `error` envelope's summary, or prose."""
    text = body.decode(errors="replace").strip()
    if not text:
        return None
    if not text.startswith(STRUCTURE):
        return text
    problem = problem_in(body)
    summary: object = problem.get("summary") if problem is not None else None
    if not isinstance(summary, str) or not summary.strip():
        return None
    return summary.strip()


def code_in(body: bytes) -> RefusalCode | None:
    """Return the refusal's code where the contract lists it; any other code reads as none."""
    problem = problem_in(body)
    code: object = problem.get("code") if problem is not None else None
    return code if isinstance(code, str) and is_refusal_code(code) else None


def retry_after(answer: Answer) -> int | None:
    """Return the seconds a `Retry-After` header names, or None where it names none this can read."""
    said = answer.headers.get("retry-after")
    if said is None or not said.strip().isdecimal():
        return None
    return int(said)


def refusal_of(answer: Answer) -> LemonfiberError:
    """Return the problem an answer that is not a success is.

    A request turned away at 401 or 403 is read from its code: the credential's
    own code, no code, or a code the contract does not list is `NotAdmittedError`;
    any other listed code is `DeclinedError`, carrying lemonfiber's sentence. Any
    other status with no sentence this client can read did not come from
    lemonfiber, and is `UnreachableError`.
    """
    sentence = sentence_in(answer.body)
    code = code_in(answer.body)
    problem = problem_in(answer.body)
    if answer.status in TURNED_AWAY:
        if code is None or REFUSAL_CODES[code].name == THE_CREDENTIAL or sentence is None:
            return NotAdmittedError(NOT_ADMITTED, status=answer.status, code=code, problem=problem)
        return DeclinedError(sentence, status=answer.status, code=code, problem=problem)
    if answer.status == TOO_MANY:
        said = sentence or "Too many wrong answers lately; wait before trying again."
        return TooManyAttemptsError(
            said,
            status=answer.status,
            retry_after=retry_after(answer),
            code=code,
            problem=problem,
        )
    if sentence is None:
        return UnreachableError(f"Something other than lemonfiber answered, with status {answer.status}.")
    meant = MEANT_BY.get(answer.status, FailedError)
    return meant(sentence, status=answer.status, code=code, problem=problem)
