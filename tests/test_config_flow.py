# Copyright (c) 2026 NightWorksIO
"""Adding a stack, replacing its key and moving its address and pin, each checked against the stand-in first."""

from typing import TYPE_CHECKING, Any, Final, cast

import pytest
from homeassistant.config_entries import SOURCE_USER
from homeassistant.const import CONF_API_KEY, CONF_URL
from homeassistant.data_entry_flow import FlowResultType
from lemonfiber import ConfigurationError, LemonfiberError, UnexpectedKindError, UnknownKindError

from custom_components.lemonfiber.config_flow import ANOTHER_STACK
from custom_components.lemonfiber.connection import Reason, refused
from custom_components.lemonfiber.const import CONF_PIN, DOMAIN
from tests.conftest import KEY, MEMBER_ID, STACK_ID, capabilities, entry_for, said, serve
from tests.stack import LOOPBACK, Reply, Stack, envelope, problem, unused_port

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from pytest_homeassistant_custom_component.common import MockConfigEntry


OTHER_PIN: Final = "0" * 64
NEW_KEY: Final = "lfk_" + "b" * 32


@pytest.fixture(autouse=True)
def no_setup(monkeypatch: pytest.MonkeyPatch) -> None:
    """Keep an entry a flow creates or changes from being set up, so a flow is judged on its own."""

    async def set_up(*_: object) -> bool:
        return True

    monkeypatch.setattr("custom_components.lemonfiber.async_setup_entry", set_up)


async def configure(hass: HomeAssistant, flow_id: str, answers: dict[str, str]) -> dict[str, Any]:
    """Answer a flow's form."""
    return said(await hass.config_entries.flow.async_configure(flow_id, answers))


async def submit(hass: HomeAssistant, answers: dict[str, str]) -> dict[str, Any]:
    """Open the setup form and answer it."""
    shown = said(await hass.config_entries.flow.async_init(DOMAIN, context={"source": SOURCE_USER}))
    assert shown["type"] is FlowResultType.FORM
    assert shown["errors"] == {}
    return await configure(hass, shown["flow_id"], answers)


def answers(stack: Stack, **changed: str) -> dict[str, str]:
    """Return the setup form answered with what the stand-in's mint reply would give, with fields changed."""
    return {CONF_URL: stack.url, CONF_API_KEY: KEY, CONF_PIN: stack.pin} | changed


async def test_a_stack_is_added_once_the_address_key_and_pin_are_answered_for(
    hass: HomeAssistant,
    stack: Stack,
) -> None:
    serve(stack)
    result = await submit(hass, answers(stack, url=f" {stack.url}/ ", pin=stack.pin.upper()))
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == LOOPBACK
    assert result["data"] == {CONF_URL: stack.url, CONF_API_KEY: KEY, CONF_PIN: stack.pin}
    assert result["result"].unique_id == STACK_ID
    assert stack.arrived[0][2]["X-Lemonfiber-Token"] == KEY


async def test_a_members_key_is_added_beside_the_stacks_own_as_theirs(
    hass: HomeAssistant,
    stack: Stack,
) -> None:
    serve(stack, "member")
    entry_for(stack).add_to_hass(hass)
    result = await submit(hass, answers(stack))
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["result"].unique_id == f"{STACK_ID}:member:{MEMBER_ID}"
    assert ("/api/held", {"most": "1"}) in stack.queries


async def test_a_stack_that_keeps_no_identifier_is_known_by_its_address(
    hass: HomeAssistant,
    stack: Stack,
) -> None:
    serve(stack)
    nameless = capabilities("read")
    cast("dict[str, object]", nameless["data"])["stack"] = None
    stack.reply("/api/capabilities", Reply(body=nameless))
    result = await submit(hass, answers(stack))
    assert result["result"].unique_id == stack.url


async def test_an_answer_to_the_operator_is_no_key(hass: HomeAssistant, stack: Stack) -> None:
    serve(stack)
    stack.reply("/api/capabilities", Reply(body=capabilities("operator")))
    shown = await submit(hass, answers(stack))
    assert shown["errors"] == {CONF_API_KEY: Reason.NOT_A_KEY}


async def test_a_stack_already_added_is_not_added_twice(hass: HomeAssistant, stack: Stack) -> None:
    serve(stack)
    entry_for(stack).add_to_hass(hass)
    result = await submit(hass, answers(stack))
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"


REFUSED_KEY: Final = Reply(403, problem("ADMIT-4", "Not admitted."))
IN_THE_CLEAR: Final = Reply(403, problem("ADMIT-11", "A key from another machine arrives over TLS."))


@pytest.mark.parametrize(
    ("changed", "answer", "field", "reason"),
    [
        ({"pin": "not a pin"}, None, CONF_PIN, Reason.PIN_MALFORMED),
        ({"url": "https://"}, None, CONF_URL, Reason.ADDRESS_REFUSED),
        ({"url": "http://127.0.0.1:8443"}, None, CONF_URL, Reason.ADDRESS_NOT_HTTPS),
        ({"api_key": "lfk with a space"}, None, CONF_API_KEY, Reason.KEY_MALFORMED),
        ({"pin": OTHER_PIN}, None, CONF_PIN, Reason.PIN_MISMATCH),
        ({}, REFUSED_KEY, CONF_API_KEY, Reason.KEY_REFUSED),
        ({}, IN_THE_CLEAR, CONF_URL, Reason.KEY_IN_THE_CLEAR),
        ({}, Reply(body={"api_version": 1}), CONF_URL, Reason.NOT_LEMONFIBER),
    ],
)
async def test_a_failure_names_the_field_to_change_and_the_form_can_be_answered_again(
    hass: HomeAssistant,
    stack: Stack,
    changed: dict[str, str],
    answer: Reply | None,
    field: str,
    reason: Reason,
) -> None:
    serve(stack)
    if answer is not None:
        stack.reply("/api/capabilities", answer, Reply(body=capabilities("read")))
    shown = await submit(hass, answers(stack, **changed))
    assert shown["type"] is FlowResultType.FORM
    assert shown["errors"] == {field: reason}
    done = await configure(hass, shown["flow_id"], answers(stack))
    assert done["type"] is FlowResultType.CREATE_ENTRY


async def test_nothing_answering_names_the_address(hass: HomeAssistant, stack: Stack) -> None:
    shown = await submit(hass, answers(stack, url=f"https://{LOOPBACK}:{unused_port()}"))
    assert shown["errors"] == {CONF_URL: Reason.UNREACHABLE}


async def test_a_stack_speaking_another_version_says_both(hass: HomeAssistant, stack: Stack) -> None:
    serve(stack)
    stack.reply("/api/capabilities", Reply(body=envelope("capabilities", {"capabilities": {}}, version=2)))
    shown = await submit(hass, answers(stack))
    assert shown["errors"] == {"base": Reason.VERSION_MISMATCH}
    assert shown["description_placeholders"] == {"spoken": "1", "served": "2"}


async def test_any_other_refusal_carries_the_stacks_own_sentence(hass: HomeAssistant, stack: Stack) -> None:
    serve(stack)
    stack.reply("/api/capabilities", Reply(500, problem("FAIL-1", "The disk is full.")))
    shown = await submit(hass, answers(stack))
    assert shown["errors"] == {"base": Reason.REFUSED}
    assert shown["description_placeholders"] == {"sentence": "The disk is full."}


@pytest.mark.parametrize(
    ("error", "reason"),
    [
        (UnknownKindError("later"), Reason.NOT_LEMONFIBER),
        (UnexpectedKindError("capabilities", "status"), Reason.NOT_LEMONFIBER),
        (ConfigurationError("The session would send through a proxy."), Reason.REFUSED),
    ],
)
def test_every_failure_of_the_client_comes_to_a_reason(error: LemonfiberError, reason: Reason) -> None:
    assert refused(error).reason is reason


def test_a_failure_with_no_code_of_its_own_says_its_sentence() -> None:
    assert refused(ConfigurationError("Said plainly.")).placeholders == {"sentence": "Said plainly."}


async def test_a_refused_key_is_replaced_by_asking_for_a_new_one_only(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack)
    stack.reply("/api/capabilities", REFUSED_KEY, Reply(body=capabilities("read")))
    shown = said(await entry.start_reauth_flow(hass))
    assert shown["step_id"] == "reauth_confirm"
    assert list(shown["data_schema"].schema) == [CONF_API_KEY]
    refused_again = await configure(hass, shown["flow_id"], {CONF_API_KEY: KEY})
    assert refused_again["errors"] == {CONF_API_KEY: Reason.KEY_REFUSED}
    done = await configure(hass, shown["flow_id"], {CONF_API_KEY: NEW_KEY})
    assert done["type"] is FlowResultType.ABORT
    assert done["reason"] == "reauth_successful"
    assert entry.data == {CONF_URL: stack.url, CONF_API_KEY: NEW_KEY, CONF_PIN: stack.pin}


async def test_a_stack_out_of_reach_while_a_key_is_replaced_is_said_on_the_form(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    hass.config_entries.async_update_entry(entry, data={**entry.data, CONF_PIN: OTHER_PIN})
    shown = said(await entry.start_reauth_flow(hass))
    result = await configure(hass, shown["flow_id"], {CONF_API_KEY: NEW_KEY})
    assert result["errors"] == {"base": Reason.PIN_MISMATCH}


async def test_the_address_and_pin_move_without_removing_the_entry(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    async with Stack() as moved:
        serve(moved)
        shown = said(await entry.start_reconfigure_flow(hass))
        assert shown["step_id"] == "reconfigure"
        assert list(shown["data_schema"].schema) == [CONF_URL, CONF_PIN]
        mismatched = await configure(hass, shown["flow_id"], {CONF_URL: moved.url, CONF_PIN: stack.pin})
        assert mismatched["errors"] == {CONF_PIN: Reason.PIN_MISMATCH}
        done = await configure(hass, shown["flow_id"], {CONF_URL: moved.url, CONF_PIN: moved.pin})
    assert done["type"] is FlowResultType.ABORT
    assert done["reason"] == "reconfigure_successful"
    assert entry.data == {CONF_URL: moved.url, CONF_API_KEY: KEY, CONF_PIN: moved.pin}
    assert entry.unique_id == STACK_ID


async def test_a_key_refused_while_the_address_moves_is_said_on_the_form(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack)
    stack.reply("/api/capabilities", REFUSED_KEY)
    shown = said(await entry.start_reconfigure_flow(hass))
    result = await configure(hass, shown["flow_id"], {CONF_URL: stack.url, CONF_PIN: stack.pin})
    assert result["errors"] == {"base": Reason.KEY_REFUSED}


async def test_the_address_cannot_move_onto_a_stack_another_entry_holds(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    hass.config_entries.async_update_entry(entry, unique_id=stack.url)
    async with Stack() as taken:
        serve(taken)
        entry_for(taken).add_to_hass(hass)
        shown = said(await entry.start_reconfigure_flow(hass))
        result = await configure(hass, shown["flow_id"], {CONF_URL: taken.url, CONF_PIN: taken.pin})
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"


def answering_as(stack: Stack, identity: str) -> Reply:
    """Return the capabilities of a stack naming itself by another identifier."""
    other = capabilities("read")
    cast("dict[str, object]", other["data"])["stack"] = identity
    return Reply(body=other)


async def test_the_address_cannot_move_onto_another_stack(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    async with Stack() as other:
        serve(other)
        other.reply("/api/capabilities", answering_as(other, "01J9ANOTHER00000000000000"))
        shown = said(await entry.start_reconfigure_flow(hass))
        result = await configure(hass, shown["flow_id"], {CONF_URL: other.url, CONF_PIN: other.pin})
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == ANOTHER_STACK
    assert entry.data[CONF_URL] == stack.url


async def test_a_new_key_must_reach_the_stack_the_entry_was_added_for(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack, "member")
    shown = said(await entry.start_reauth_flow(hass))
    result = await configure(hass, shown["flow_id"], {CONF_API_KEY: NEW_KEY})
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == ANOTHER_STACK
    assert entry.data[CONF_API_KEY] == KEY


async def test_an_entry_keyed_by_its_address_takes_the_stacks_identifier_when_its_key_is_replaced(
    hass: HomeAssistant,
    stack: Stack,
) -> None:
    serve(stack)
    entry = entry_for(stack, stack.url)
    entry.add_to_hass(hass)
    shown = said(await entry.start_reauth_flow(hass))
    done = await configure(hass, shown["flow_id"], {CONF_API_KEY: NEW_KEY})
    assert done["reason"] == "reauth_successful"
    assert entry.unique_id == STACK_ID
