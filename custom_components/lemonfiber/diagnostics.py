# Copyright (c) 2026 NightWorksIO
"""What an entry hands over for a diagnosis, with the key, the address and the pin withheld."""

from collections.abc import Mapping
from pathlib import Path
from typing import TYPE_CHECKING, Final, cast

import lemonfiber
from homeassistant.components.diagnostics import REDACTED
from homeassistant.const import CONF_API_KEY, CONF_URL

from .const import CONF_PIN

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .runtime import LemonfiberConfigEntry

WITHHELD: Final = frozenset(
    {
        CONF_API_KEY,
        CONF_URL,
        CONF_PIN,
        # The address again: the entry is identified by it and named after its host.
        "unique_id",
        "title",
        # The household's front door is an address on the same machine, and the
        # household panel names its members.
        "door",
        "household",
    },
)
"""Every field withheld wherever it appears in what is handed over."""

REVISION: Final = Path(lemonfiber.__file__).parent / "REVISION"
"""Where the client this integration runs records the sdk-python commit it was copied from."""


def revision() -> str:
    """Return the sdk-python commit the client was copied from."""
    return REVISION.read_text(encoding="ascii").strip()


def withheld(value: object) -> object:
    """Return a value with every withheld field that holds anything replaced, at any depth.

    Home Assistant's `async_redact_data` does this too, and is typed with a bare
    `Mapping` that strict typing reads as unknown, so the walk is written here.
    """
    if isinstance(value, Mapping):
        fields = cast("Mapping[object, object]", value)
        return {
            name: REDACTED if name in WITHHELD and held is not None else withheld(held)
            for name, held in fields.items()
        }
    if isinstance(value, list | tuple):
        return [withheld(item) for item in cast("list[object] | tuple[object, ...]", value)]
    return value


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    entry: LemonfiberConfigEntry,
) -> dict[str, object]:
    """Return the client, the entry, the key's scope and what the stack last said, with nothing that identifies or admits."""
    runtime = entry.runtime_data
    technical = runtime.technical
    said: dict[str, object] = {
        "client": await hass.async_add_executor_job(revision),
        "entry": entry.as_dict(),
        "scope": runtime.connected.scope,
        "capabilities": dict(runtime.connected.capabilities.states),
    }
    if technical is not None:
        said |= {
            "version": technical.version,
            "state": technical.stream.state,
            "dashboard": technical.stream.data,
            "diagnosis": technical.diagnosis.data,
        }
    return cast("dict[str, object]", withheld(said))
