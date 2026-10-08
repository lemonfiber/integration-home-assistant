# Copyright (c) 2026 NightWorksIO
"""Setting an entry up against the stand-in: what it reads first, what each scope yields, and each way it fails."""

from typing import TYPE_CHECKING

from homeassistant.config_entries import ConfigEntryState
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers import issue_registry as ir

from custom_components.lemonfiber import coordinator
from custom_components.lemonfiber.connection import Reason, Scope
from custom_components.lemonfiber.const import DOMAIN
from tests.conftest import reauthenticating, serve
from tests.stack import Feed, Reply, event, problem

if TYPE_CHECKING:
    import pytest
    from homeassistant.core import HomeAssistant
    from pytest_homeassistant_custom_component.common import MockConfigEntry

    from tests.stack import Stack


async def set_up(hass: HomeAssistant, entry: MockConfigEntry) -> None:
    """Set the entry up and let everything it started settle."""
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()


async def test_a_read_key_follows_the_stream_and_builds_the_entities(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack)
    await set_up(hass, entry)
    assert entry.state is ConfigEntryState.LOADED
    assert entry.runtime_data.connected.scope is Scope.READ
    entities = er.async_entries_for_config_entry(er.async_get(hass), entry.entry_id)
    assert len(entities) == 15
    assert all(one.unique_id.startswith(f"{entry.entry_id}-") for one in entities)
    assert stack.asked("/api/events") == 1
    assert await hass.config_entries.async_unload(entry.entry_id)
    assert entry.state is ConfigEntryState.NOT_LOADED


async def test_an_act_key_is_known_by_the_actions_it_may_call(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack, "act")
    await set_up(hass, entry)
    assert entry.runtime_data.connected.scope is Scope.ACT


async def test_a_members_key_yields_no_technical_entity_and_opens_no_stream(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack, "member")
    await set_up(hass, entry)
    assert entry.state is ConfigEntryState.LOADED
    assert entry.runtime_data.connected.scope is Scope.MEMBER
    assert entry.runtime_data.technical is None
    assert er.async_entries_for_config_entry(er.async_get(hass), entry.entry_id) == []
    assert stack.asked("/api/events") == stack.asked("/api/version") == 0


async def test_a_refused_key_asks_for_a_new_one(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack)
    stack.reply("/api/capabilities", Reply(403, problem("ADMIT-4", "Not admitted.")))
    await set_up(hass, entry)
    assert entry.state is ConfigEntryState.SETUP_ERROR
    assert entry.error_reason_translation_key == Reason.KEY_REFUSED
    assert reauthenticating(hass)


async def test_a_stream_refusing_the_key_asks_for_a_new_one(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack)
    stack.reply("/api/events", Reply(403, problem("ADMIT-4", "Not admitted.")))
    await set_up(hass, entry)
    assert entry.state is ConfigEntryState.SETUP_ERROR
    assert reauthenticating(hass)


async def test_a_stack_out_of_reach_is_tried_again(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack)
    hass.config_entries.async_update_entry(entry, data={**entry.data, "pin": "0" * 64})
    await set_up(hass, entry)
    assert entry.state is ConfigEntryState.SETUP_RETRY
    assert entry.error_reason_translation_key == Reason.PIN_MISMATCH


async def test_what_only_the_person_can_put_right_is_raised_as_a_repair_until_setup_reaches_the_stack(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack)
    pin = entry.data["pin"]
    hass.config_entries.async_update_entry(entry, data={**entry.data, "pin": "0" * 64})
    await set_up(hass, entry)
    issues = ir.async_get(hass)
    raised = issues.async_get_issue(DOMAIN, f"{entry.entry_id}_{Reason.PIN_MISMATCH}")
    assert raised is not None
    assert raised.translation_key == Reason.PIN_MISMATCH
    assert raised.translation_placeholders == {"title": entry.title}
    hass.config_entries.async_update_entry(entry, data={**entry.data, "pin": pin})
    await hass.config_entries.async_reload(entry.entry_id)
    await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.LOADED
    assert issues.async_get_issue(DOMAIN, f"{entry.entry_id}_{Reason.PIN_MISMATCH}") is None


async def test_a_failure_another_try_may_cure_raises_no_repair(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack)
    stack.reply("/api/version", Reply(500, problem("FAIL-1", "The engine is not answering.")))
    await set_up(hass, entry)
    assert ir.async_get(hass).issues == {}


async def test_a_version_that_cannot_be_read_is_tried_again(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack)
    stack.reply("/api/version", Reply(500, problem("FAIL-1", "The engine is not answering.")))
    await set_up(hass, entry)
    assert entry.state is ConfigEntryState.SETUP_RETRY
    assert entry.error_reason_translation_key == Reason.REFUSED
    assert entry.error_reason_translation_placeholders == {"sentence": "The engine is not answering."}


async def test_a_stream_carrying_no_dashboard_in_time_is_let_go_and_tried_again(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    serve(stack)
    quiet = Feed()
    quiet.say(event("news", {"items": []}))
    stack.stream(quiet)
    monkeypatch.setattr(coordinator, "FIRST_SNAPSHOT_WITHIN", 0.2)
    await set_up(hass, entry)
    assert entry.state is ConfigEntryState.SETUP_RETRY
    assert entry.error_reason_translation_key == Reason.NO_DASHBOARD


async def test_a_stream_in_another_version_is_tried_again(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack)
    feed = Feed()
    feed.say(event("dashboard", {}, version=2))
    stack.stream(feed)
    await set_up(hass, entry)
    assert entry.state is ConfigEntryState.SETUP_RETRY
    assert entry.error_reason_translation_key == Reason.VERSION_MISMATCH
