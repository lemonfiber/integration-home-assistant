# Copyright (c) 2026 NightWorksIO
"""Reaching a stack with its address, a key and its certificate pin, and naming whichever of the three failed."""

from dataclasses import dataclass, field
from enum import StrEnum
from typing import TYPE_CHECKING, Final

from homeassistant.const import CONF_API_KEY, CONF_URL
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from lemonfiber import (
    KEY_CALLABLE,
    REFUSAL_CODES,
    Address,
    AddressRefusedError,
    ApiVersionMismatchError,
    AsyncClient,
    CertificatePin,
    CertificateRefusedError,
    Credential,
    CredentialRefusedError,
    DeclinedError,
    LemonfiberError,
    NotAdmittedError,
    Read,
    RefusedError,
    UnexpectedKindError,
    UnknownKindError,
    UnreachableError,
    UnreadableResponseError,
    expect,
)
from lemonfiber.address import ENCRYPTED, split

from .const import CONF_PIN

if TYPE_CHECKING:
    from collections.abc import Mapping

    from homeassistant.core import HomeAssistant
    from lemonfiber import CapabilitySet
    from lemonfiber.contract import CapabilityState

BASE: Final = "base"
"""Where a config flow puts an error that belongs to no one field."""

UNPERMITTED: Final[CapabilityState] = "unpermitted"
"""What a capability comes to for a credential whose scope does not reach it."""

KEY_IN_THE_CLEAR: Final = next(code for code, listed in REFUSAL_CODES.items() if listed.name == "KEY_IN_THE_CLEAR")
"""The refusal of a key sent from another machine without the TLS its pin verifies, looked up by its registry name."""


class Reason(StrEnum):
    """Why a stack could not be reached with what was given, each a translation key."""

    ADDRESS_REFUSED = "address_refused"
    ADDRESS_NOT_HTTPS = "address_not_https"
    PIN_MALFORMED = "pin_malformed"
    PIN_MISMATCH = "pin_mismatch"
    UNREACHABLE = "unreachable"
    KEY_MALFORMED = "key_malformed"
    KEY_REFUSED = "key_refused"
    KEY_IN_THE_CLEAR = "key_in_the_clear"
    NOT_LEMONFIBER = "not_lemonfiber"
    VERSION_MISMATCH = "version_mismatch"
    NO_DASHBOARD = "no_dashboard"
    REFUSED = "refused"


FIELD_OF: Final[Mapping[Reason, str]] = {
    Reason.ADDRESS_REFUSED: CONF_URL,
    Reason.ADDRESS_NOT_HTTPS: CONF_URL,
    Reason.PIN_MALFORMED: CONF_PIN,
    Reason.PIN_MISMATCH: CONF_PIN,
    Reason.UNREACHABLE: CONF_URL,
    Reason.KEY_MALFORMED: CONF_API_KEY,
    Reason.KEY_REFUSED: CONF_API_KEY,
    Reason.KEY_IN_THE_CLEAR: CONF_URL,
    Reason.NOT_LEMONFIBER: CONF_URL,
    Reason.VERSION_MISMATCH: BASE,
    Reason.NO_DASHBOARD: BASE,
    Reason.REFUSED: BASE,
}
"""The field each reason names: the one the person has to change."""


class NotConnectedError(Exception):
    """The stack could not be reached with what was given, and which part of it was wrong."""

    def __init__(self, reason: Reason, placeholders: Mapping[str, str] | None = None) -> None:
        """Hold the reason and what its sentence is filled in with."""
        super().__init__(reason.value)
        self.reason = reason
        self.placeholders: Mapping[str, str] = placeholders or {}

    @property
    def field(self) -> str:
        """Return the field the person has to change, or `base` where it is none of them."""
        return FIELD_OF[self.reason]


PLAIN: Final[tuple[tuple[type[LemonfiberError], Reason], ...]] = (
    (CertificateRefusedError, Reason.PIN_MISMATCH),
    (UnreachableError, Reason.UNREACHABLE),
    (NotAdmittedError, Reason.KEY_REFUSED),
    (UnreadableResponseError, Reason.NOT_LEMONFIBER),
    (UnknownKindError, Reason.NOT_LEMONFIBER),
    (UnexpectedKindError, Reason.NOT_LEMONFIBER),
)
"""The failures that name one reason whatever they carry, in the order they are asked about."""


def refused(error: LemonfiberError) -> NotConnectedError:
    """Return what a failure from the client says about the address, the key or the pin."""
    if isinstance(error, DeclinedError) and error.code == KEY_IN_THE_CLEAR:
        return NotConnectedError(Reason.KEY_IN_THE_CLEAR)
    if isinstance(error, ApiVersionMismatchError):
        return NotConnectedError(Reason.VERSION_MISMATCH, {"spoken": str(error.spoken), "served": str(error.served)})
    for kind, reason in PLAIN:
        if isinstance(error, kind):
            return NotConnectedError(reason)
    sentence = error.sentence if isinstance(error, RefusedError) else str(error)
    return NotConnectedError(Reason.REFUSED, {"sentence": sentence})


class Scope(StrEnum):
    """What a key reaches, as the stack's capabilities say: every read, every read and some actions, or one member's own."""

    READ = "read"
    ACT = "act"
    MEMBER = "member"


def scope_of(capabilities: CapabilitySet) -> Scope:
    """Return a key's scope from what the stack says the key may ask for."""
    if capabilities.of_read(Read.STATUS) == UNPERMITTED:
        return Scope.MEMBER
    if any(capabilities.of_action(action) not in {None, UNPERMITTED} for action in KEY_CALLABLE):
        return Scope.ACT
    return Scope.READ


@dataclass(frozen=True, slots=True)
class Connected:
    """A client that reached the stack, the pin it holds the stack to, and what the key may do there."""

    client: AsyncClient = field(repr=False)
    pin: CertificatePin = field(repr=False)
    capabilities: CapabilitySet
    scope: Scope

    @property
    def technical(self) -> bool:
        """Tell whether the key reaches the stack's technical side: a `read` or `act` key, and never a member's."""
        return self.scope is not Scope.MEMBER

    async def version(self) -> str:
        """Return the version of lemonfiber the stack runs."""
        try:
            return expect(await self.client.read(Read.VERSION), "version")["data"]["binary"]
        except LemonfiberError as error:
            raise refused(error) from None


def address_of(url: str, pin: CertificatePin) -> Address:
    """Return the address as the client holds it, held to the pin, naming the field that is wrong."""
    try:
        _, scheme, _, _ = split(url)
        if scheme != ENCRYPTED:
            raise NotConnectedError(Reason.ADDRESS_NOT_HTTPS)
        return Address(url, pin=pin)
    except AddressRefusedError:
        raise NotConnectedError(Reason.ADDRESS_REFUSED) from None


async def connect(hass: HomeAssistant, url: str, key: str, pin: str) -> Connected:
    """Reach the stack and ask what the key may do there, in the order a person would check the three.

    The address and pin are read first, then the key's shape, and then the stack
    is asked: the handshake answers for the pin and the address, and the stack's
    answer for the key.
    """
    try:
        held = CertificatePin(pin)
    except AddressRefusedError:
        raise NotConnectedError(Reason.PIN_MALFORMED) from None
    address = address_of(url, held)
    try:
        credential = Credential(key)
    except CredentialRefusedError:
        raise NotConnectedError(Reason.KEY_MALFORMED) from None
    client = AsyncClient(address, credential, session=async_get_clientsession(hass))
    try:
        capabilities = await client.capabilities()
    except LemonfiberError as error:
        raise refused(error) from None
    return Connected(client, held, capabilities, scope_of(capabilities))
