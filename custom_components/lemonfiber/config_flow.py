# Copyright (c) 2026 NightWorksIO
"""Adding a stack with what the key's mint reply gave, replacing a refused key, and moving the address and pin.

Nothing is stored until the stack has answered with the address, the key and the
pin together, and a failure names the one field to change. The operator password
is never asked for.
"""

from typing import TYPE_CHECKING, Any, Final, override

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_API_KEY, CONF_URL

from .connection import BASE, NotConnectedError, connect
from .const import CONF_PIN, DOMAIN

if TYPE_CHECKING:
    from collections.abc import Mapping

    from .connection import Connected

ADDRESS: Final = vol.Required(CONF_URL)
KEY: Final = vol.Required(CONF_API_KEY)
PIN: Final = vol.Required(CONF_PIN)

SETUP: Final = vol.Schema({ADDRESS: str, KEY: str, PIN: str})
REAUTHENTICATION: Final = vol.Schema({KEY: str})
RECONFIGURATION: Final = vol.Schema({ADDRESS: str, PIN: str})


def entered(connected: Connected) -> dict[str, str]:
    """Return the address and pin as the client read them, which is how an entry keeps them."""
    return {CONF_URL: connected.client.address.base, CONF_PIN: connected.pin.hex}


class LemonfiberConfigFlow(ConfigFlow, domain=DOMAIN):
    """Add a stack, replace its key, or move its address and pin."""

    VERSION = 1
    MINOR_VERSION = 1

    async def _connect(
        self, url: str, key: str, pin: str, schema: vol.Schema
    ) -> tuple[Connected | None, dict[str, str], dict[str, str]]:
        """Reach the stack, or return the error to show on the field to change, among the fields this form has."""
        try:
            return await connect(self.hass, url, key, pin), {}, {}
        except NotConnectedError as refusal:
            named = refusal.field if refusal.field in schema.schema else BASE
            return None, {named: refusal.reason.value}, dict(refusal.placeholders)

    @override
    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Ask for the address, the key and the pin, and add the stack once all three are answered for."""
        errors: dict[str, str] = {}
        placeholders: dict[str, str] = {}
        if user_input is not None:
            key = user_input[CONF_API_KEY]
            connected, errors, placeholders = await self._connect(
                user_input[CONF_URL], key, user_input[CONF_PIN], SETUP
            )
            if connected is not None:
                await self.async_set_unique_id(connected.client.address.base)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=connected.client.address.host, data={**entered(connected), CONF_API_KEY: key}
                )
        return self.async_show_form(
            step_id="user",
            data_schema=self.add_suggested_values_to_schema(SETUP, user_input),
            errors=errors,
            description_placeholders=placeholders,
        )

    async def async_step_reauth(self, _entry_data: Mapping[str, Any]) -> ConfigFlowResult:
        """Start asking for a new key, the stack having refused the one held."""
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Ask for a new key only, and keep it once the stack admits it."""
        entry = self._get_reauth_entry()
        errors: dict[str, str] = {}
        placeholders: dict[str, str] = {}
        if user_input is not None:
            key = user_input[CONF_API_KEY]
            connected, errors, placeholders = await self._connect(
                entry.data[CONF_URL], key, entry.data[CONF_PIN], REAUTHENTICATION
            )
            if connected is not None:
                return self.async_update_reload_and_abort(entry, data_updates={CONF_API_KEY: key})
        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=REAUTHENTICATION,
            errors=errors,
            description_placeholders=placeholders,
        )

    async def async_step_reconfigure(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Ask for a new address and pin, keeping the key and the entry."""
        entry = self._get_reconfigure_entry()
        errors: dict[str, str] = {}
        placeholders: dict[str, str] = {}
        if user_input is not None:
            connected, errors, placeholders = await self._connect(
                user_input[CONF_URL], entry.data[CONF_API_KEY], user_input[CONF_PIN], RECONFIGURATION
            )
            if connected is not None:
                address = connected.client.address.base
                held = self.hass.config_entries.async_entry_for_domain_unique_id(DOMAIN, address)
                if held is not None and held.entry_id != entry.entry_id:
                    return self.async_abort(reason="already_configured")
                return self.async_update_reload_and_abort(entry, unique_id=address, data_updates=entered(connected))
        return self.async_show_form(
            step_id="reconfigure",
            data_schema=self.add_suggested_values_to_schema(RECONFIGURATION, user_input or entry.data),
            errors=errors,
            description_placeholders=placeholders,
        )
