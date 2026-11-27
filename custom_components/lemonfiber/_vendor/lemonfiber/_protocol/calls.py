# Copyright (c) 2026 NightWorksIO
"""What a request carries, and the answer a transport hands back."""

import base64
import json
import urllib.parse
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from http import HTTPMethod, HTTPStatus
from typing import TYPE_CHECKING, Final

from lemonfiber._generated import READS, ActionRequest
from lemonfiber.files import PICTURE_MOST, PICTURE_TYPES
from lemonfiber.problems import MisaskedError
from lemonfiber.reads import (
    ACTIONS,
    BUNDLE,
    CAPABILITIES,
    DEVICE_KEYS,
    JOBS,
    KEY_CLAIMS,
    KEYS,
    LOGS,
    PUSH_ENDPOINTS,
    SESSION,
)

if TYPE_CHECKING:
    from lemonfiber.credential import Credential
    from lemonfiber.device_keys import Registering
    from lemonfiber.keys import Minting
    from lemonfiber.push_endpoints import PushEndpointRegistering
    from lemonfiber.reads import Read

type Scalar = str | int | bool
"""One value a query parameter carries."""

type Query = Mapping[str, Scalar | Sequence[Scalar] | None]
"""A read's parameters. A list is the parameter once per value; `None` or an empty list sends nothing."""

type Json = bool | int | float | str | Sequence[Json] | Mapping[str, Json] | None
"""A value an action's arguments may carry."""

NOTHING_SAFE: Final = ""
"""The characters a path segment leaves unquoted beyond the unreserved ones: none."""

JSON_TYPE: Final = "application/json"
"""What every request but the one for a file asks to be answered in, and what a body is sent as."""

UNKEPT_SEGMENTS: Final = frozenset({"", ".", ".."})
"""Values a URL does not keep as a segment: the folder itself, the path's own folder, the one above it."""

TITLE: Final = "id"
"""The segment a title's picture is read under: the id the title is listed by."""

REFERENCE: Final = "reference"
"""The segment a kept ask's cover is read under: the reference the household list names it by."""

ANY_TYPE: Final = "*/*"
"""What a request for a file takes, whatever it is served as."""

DEFAULT_TIMEOUT: Final = 30.0
"""How many seconds a call waits for its answer, unless the client is told otherwise."""


@dataclass(frozen=True, slots=True)
class Call:
    """One request, as every transport sends it.

    Its headers carry the credential and its body may carry a password, so
    neither is shown when the call is printed.
    """

    method: HTTPMethod
    path: str
    headers: Mapping[str, str] = field(default_factory=dict[str, str], repr=False)
    body: bytes | None = field(default=None, repr=False)
    most: int | None = None
    """The most bytes the answer may be: a transport reads one byte past it and no further, and nothing of an
    answer that declares more. `None` reads the whole answer."""


@dataclass(frozen=True, slots=True)
class Answer:
    """One answer, as every transport hands it back: header names lower-cased."""

    status: int
    headers: Mapping[str, str]
    body: bytes


def received(status: int, headers: Mapping[str, str], body: bytes) -> Answer:
    """Return an answer as a transport received it, its header names lower-cased."""
    return Answer(status, {name.lower(): value for name, value in headers.items()}, body)


def declared_over(headers: Mapping[str, str], most: int) -> bool:
    """Tell whether an answer's `Content-Length` declares more than `most` bytes, its headers read without regard to case."""
    length = headers.get("content-length")
    return length is not None and length.isdecimal() and int(length) > most


def segment(name: str) -> str:
    """Write a name as one path segment, so a separator in it reaches lemonfiber as written."""
    return urllib.parse.quote(name, safe=NOTHING_SAFE)


def held(name: str, sentence: str) -> str:
    """Write a name as one path segment, refusing with `sentence` one a URL would resolve away."""
    if name in UNKEPT_SEGMENTS:
        raise MisaskedError(sentence, status=HTTPStatus.BAD_REQUEST)
    return segment(name)


A_JOB: Final = "Work is named by the name its accepting reply gave it, and what was given is not a name that can be sent."
"""What a job's name a URL would resolve away is refused with."""


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
    return Call(call.method, call.path, {**call.headers, **credential.header()}, call.body, call.most)


def filled_in(read: Read, query: Query | None) -> tuple[str, Query]:
    """Return a read's path with each segment a caller fills written in, and the query left to send.

    A segment is one value, written escaped so it stays one segment and cannot
    reach a path beside the read's own. One not given, given as a list, or one a
    URL would resolve away is refused before anything is sent.
    """
    given = dict(query or {})
    path = read.path
    for name in READS[read].segments:
        path = placed(path, name, given.pop(name, None))
    return path, given


def placed(path: str, name: str, value: Scalar | Sequence[Scalar] | None) -> str:
    """Return the path with the segment `name` written in as one escaped value.

    A value not given, given as a list, or one a URL would resolve away is
    refused before anything is sent.
    """
    one = written(value) if isinstance(value, str | int) else None
    if one is None or one in UNKEPT_SEGMENTS:
        sentence = f"This read needs one `{name}` it can send, and was not given one."
        raise MisaskedError(sentence, status=HTTPStatus.BAD_REQUEST)
    return path.replace(f"{{{name}}}", segment(one))


def read_call(read: Read, query: Query | None) -> Call:
    """Ask for what a command prints under `--json`."""
    path, rest = filled_in(read, query)
    return Call(HTTPMethod.GET, path + search(rest), {"Accept": JSON_TYPE})


def capabilities_call() -> Call:
    """Ask what the stack can do, for the credential the call carries."""
    return Call(HTTPMethod.GET, CAPABILITIES, {"Accept": JSON_TYPE})


def logs_call(services: Sequence[str], forms: Sequence[str], tail: int | None) -> Call:
    """Ask for what the services have been saying: those named, of the forms named, the last `tail` lines.

    Following the logs as they grow is not asked for here: lemonfiber answers it
    with a job rather than with lines, and the lines arrive on the live stream.
    """
    query: Query = {"service": services, "form": forms, "tail": tail}
    return Call(HTTPMethod.GET, LOGS + search(query), {"Accept": JSON_TYPE})


def bundle_call(name: str) -> Call:
    """Ask for one support bundle, by the name it was written under."""
    sentence = "A support bundle is named by the name it was written under, and what was given is not a name that can be sent."
    return Call(HTTPMethod.GET, f"{BUNDLE}/{held(name, sentence)}", {"Accept": ANY_TYPE})


def picture_call(template: str, name: str, value: str, query: Query | None) -> Call:
    """Ask for one picture, by the value its path's segment `name` is filled with."""
    path = placed(template, name, value)
    return Call(HTTPMethod.GET, path + search(query), {"Accept": ", ".join(PICTURE_TYPES)}, most=PICTURE_MOST)


def action_call(action: ActionRequest | str, arguments: Mapping[str, Json] | None) -> Call:
    """Tell lemonfiber to do something the command line could also do: a request, or an action by name."""
    if isinstance(action, str):
        sentence = "An action is named by its name, and what was given is not a name that can be sent."
        return posted(f"{ACTIONS}/{held(action, sentence)}", arguments or {})
    if arguments is not None:
        sentence = "An action's request carries its own arguments, and was given more beside it."
        raise MisaskedError(sentence, status=HTTPStatus.BAD_REQUEST)
    return posted(f"{ACTIONS}/{segment(action.ACTION)}", action.arguments())


def job_call(job: str, method: HTTPMethod) -> Call:
    """Ask where work stands with `GET`, or let its name go with `DELETE`."""
    return Call(method, f"{JOBS}/{held(job, A_JOB)}", {"Accept": JSON_TYPE})


FORGET: Final = "forget"
"""What a job's path is followed by where its name is let go and its work left running."""


def forget_call(job: str) -> Call:
    """Let a name go and leave the work it stands for running."""
    return Call(HTTPMethod.POST, f"{JOBS}/{held(job, A_JOB)}/{FORGET}", {"Accept": JSON_TYPE})


def session_call(password: str, name: str | None) -> Call:
    """Offer a password, and a household member's name where it is one, for a session."""
    offer = {"password": password} if name is None else {"name": name, "password": password}
    return posted(SESSION, offer)


def keys_call() -> Call:
    """Ask for the integration keys the credential may see, without their secrets."""
    return Call(HTTPMethod.GET, KEYS, {"Accept": JSON_TYPE})


def mint_call(minting: Minting, **more: Json) -> Call:
    """Mint one integration key with the operator's proof, with `more` beside it in the body."""
    asked: dict[str, Json] = {"name": minting.name, "scope": minting.scope, "purpose": minting.purpose}
    if minting.device is None:
        proof: dict[str, Json] = {"password": minting.password}
    else:
        proof = {
            "device": minting.device.device,
            "challenge": minting.device.challenge,
            "signature": base64url(minting.device.signature),
        }
    return posted(KEYS, {**asked, **proof, **more})


def register_device_key_call(registering: Registering) -> Call:
    """Register a device key with its public half, its attestation and the operator's password."""
    return posted(
        DEVICE_KEYS,
        {
            "name": registering.name,
            "public_key": base64url(registering.public_key),
            "attestation": registering.attestation.fields(),
            "password": registering.password,
        },
    )


def device_keys_call() -> Call:
    """Ask for the operator's device keys."""
    return Call(HTTPMethod.GET, DEVICE_KEYS, {"Accept": JSON_TYPE})


def device_key_challenge_call(name: str) -> Call:
    """Ask a challenge for one device key, by its name as one path segment."""
    return Call(HTTPMethod.POST, f"{device_key_path(name)}/challenge", {"Accept": JSON_TYPE})


def revoke_device_key_call(name: str) -> Call:
    """Revoke one device key, by its name as one path segment."""
    return Call(HTTPMethod.DELETE, device_key_path(name), {"Accept": JSON_TYPE})


def register_push_endpoint_call(registering: PushEndpointRegistering) -> Call:
    """Register a push endpoint with its name, its address, and its WebPush key and secret in base64url."""
    return posted(
        PUSH_ENDPOINTS,
        {
            "name": registering.name,
            "endpoint": registering.endpoint,
            "p256dh": base64url(registering.p256dh),
            "auth": base64url(registering.auth),
        },
    )


def push_endpoints_call() -> Call:
    """Ask for the push endpoints this credential keeps."""
    return Call(HTTPMethod.GET, PUSH_ENDPOINTS, {"Accept": JSON_TYPE})


def remove_push_endpoint_call(name: str) -> Call:
    """Remove one push endpoint, by its name as one path segment, refusing a name a URL would resolve away."""
    sentence = "A push endpoint is named by its name, and what was given is not a name that can be sent."
    return Call(HTTPMethod.DELETE, f"{PUSH_ENDPOINTS}/{held(name, sentence)}", {"Accept": JSON_TYPE})


def device_key_path(name: str) -> str:
    """Return the door of one device key, refusing a name a URL would resolve away."""
    sentence = "A device key is named by its name, and what was given is not a name that can be sent."
    return f"{DEVICE_KEYS}/{held(name, sentence)}"


def base64url(raw: bytes) -> str:
    """Return bytes as the stack reads them in a body: base64url, unpadded."""
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


def revoke_call(name: str) -> Call:
    """Revoke one integration key, by its name as one path segment, refusing a name a URL would resolve away."""
    sentence = "A key is revoked by its name, and what was given is not a name that can be sent."
    return Call(HTTPMethod.DELETE, f"{KEYS}/{held(name, sentence)}", {"Accept": JSON_TYPE})


def collect_call(claim: str) -> Call:
    """Collect the key a claim was minted for, with the claim alone."""
    return posted(KEY_CLAIMS, {"claim": claim})


def posted(path: str, body: Mapping[str, object]) -> Call:
    """Send a JSON body to a door that takes one, asking to be answered in JSON."""
    headers = {"Accept": JSON_TYPE, "Content-Type": JSON_TYPE}
    return Call(HTTPMethod.POST, path, headers, json.dumps(dict(body)).encode())
