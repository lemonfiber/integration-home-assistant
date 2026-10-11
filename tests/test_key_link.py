# Copyright (c) 2026 NightWorksIO
"""Adding a stack with a key link: its claim collects the key once, and neither the link nor the claim is kept."""

import logging
import urllib.parse
from typing import TYPE_CHECKING, Any, Final

import pytest
from homeassistant.const import CONF_API_KEY, CONF_URL
from homeassistant.data_entry_flow import FlowResultType

from custom_components.lemonfiber.config_flow import BY_LINK
from custom_components.lemonfiber.connection import Reason
from custom_components.lemonfiber.const import CONF_KEY_LINK, CONF_PIN
from tests.conftest import KEY, STACK_ID, configure, opened, serve
from tests.stack import LOOPBACK, Reply, envelope, problem

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from tests.stack import Stack

pytestmark = pytest.mark.usefixtures("no_setup")

CLAIM: Final = "lfc_" + "c" * 43
LATER: Final = 4102444800
"""2100-01-01, a lapse no test reaches."""
EARLIER: Final = 946684800
"""2000-01-01, a lapse every test is past."""
OTHER_PIN: Final = "0" * 64


def link(stack: Stack, **changed: str | int) -> str:
    """Return a key link to the stand-in as a claim's mint writes one, with parameters changed."""
    said: dict[str, str | int] = {
        "address": stack.url,
        "fingerprint": stack.pin,
        "stack": STACK_ID,
        "expires": LATER,
        "claim": CLAIM,
    } | changed
    return "lemonfiber://key?" + urllib.parse.urlencode(said, quote_via=urllib.parse.quote)


def minted(stack: Stack) -> dict[str, object]:
    """Return what collecting the claim answers with."""
    return envelope(
        "minted-key",
        {
            "name": "home",
            "scope": "read",
            "purpose": "home-assistant",
            "secret": KEY,
            "pin": stack.pin,
            "address": stack.url,
        },
    )


async def linked(hass: HomeAssistant, written: str) -> dict[str, Any]:
    """Open setup by key link, and paste one."""
    shown = await opened(hass, BY_LINK)
    return await configure(hass, shown["flow_id"], {CONF_KEY_LINK: written})


async def test_a_key_link_collects_its_key_once_and_keeps_only_what_the_reply_carries(
    hass: HomeAssistant,
    stack: Stack,
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(logging.DEBUG)
    serve(stack)
    stack.reply("/api/keys/claim", Reply(body=minted(stack)))
    result = await linked(hass, link(stack))
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == LOOPBACK
    assert result["data"] == {CONF_URL: stack.url, CONF_API_KEY: KEY, CONF_PIN: stack.pin}
    assert result["result"].unique_id == STACK_ID
    method, path, headers = stack.arrived[0]
    assert (method, path) == ("POST", "/api/keys/claim")
    assert "X-Lemonfiber-Token" not in headers
    assert stack.bodies[0] == ("/api/keys/claim", {"claim": CLAIM})
    assert stack.asked("/api/keys/claim") == 1
    assert stack.arrived[1][2]["X-Lemonfiber-Token"] == KEY
    assert CLAIM not in caplog.text
    assert KEY not in caplog.text


async def test_what_is_not_a_key_link_is_named_on_the_link_and_nothing_is_sent(
    hass: HomeAssistant,
    stack: Stack,
) -> None:
    shown = await linked(hass, link(stack).replace("lemonfiber://key", "lemonfiber://pair"))
    assert shown["errors"] == {CONF_KEY_LINK: Reason.LINK_MALFORMED}
    assert stack.arrived == []


async def test_a_lapsed_link_says_its_ten_minutes_are_over_and_nothing_is_sent(
    hass: HomeAssistant,
    stack: Stack,
) -> None:
    shown = await linked(hass, link(stack, expires=EARLIER))
    assert shown["errors"] == {CONF_KEY_LINK: Reason.CLAIM_LAPSED}
    assert stack.arrived == []


async def test_a_claim_the_stack_turns_away_says_why_in_the_stacks_words(
    hass: HomeAssistant,
    stack: Stack,
) -> None:
    stack.reply("/api/keys/claim", Reply(401, problem("KEY-12", "That claim collects no key")))
    shown = await linked(hass, link(stack))
    assert shown["errors"] == {CONF_KEY_LINK: Reason.CLAIM_REFUSED}
    assert shown["description_placeholders"] == {"sentence": "That claim collects no key"}


async def test_a_claim_goes_nowhere_but_the_certificate_the_link_pins(
    hass: HomeAssistant,
    stack: Stack,
) -> None:
    shown = await linked(hass, link(stack, fingerprint=OTHER_PIN))
    assert shown["errors"] == {"base": Reason.PIN_MISMATCH}
    assert stack.arrived == []


async def test_a_collected_key_the_stack_then_refuses_is_named_as_every_key_is(
    hass: HomeAssistant,
    stack: Stack,
) -> None:
    serve(stack)
    stack.reply("/api/keys/claim", Reply(body=minted(stack)))
    stack.reply(
        "/api/capabilities",
        Reply(body=envelope("capabilities", {"capabilities": {}, "scope": "operator"})),
    )
    shown = await linked(hass, link(stack))
    assert shown["errors"] == {"base": Reason.NOT_A_KEY}


async def test_a_reply_that_names_no_address_or_pin_is_given_the_links(
    hass: HomeAssistant,
    stack: Stack,
) -> None:
    serve(stack)
    bare = envelope(
        "minted-key",
        {"name": "home", "scope": "read", "purpose": "home-assistant", "secret": KEY},
    )
    stack.reply("/api/keys/claim", Reply(body=bare))
    result = await linked(hass, link(stack))
    assert result["data"] == {CONF_URL: stack.url, CONF_API_KEY: KEY, CONF_PIN: stack.pin}
