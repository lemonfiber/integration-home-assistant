# Copyright (c) 2026 NightWorksIO
"""What the integration names once and every module reads."""

import logging
from datetime import timedelta
from typing import Final

from lemonfiber import SILENCE_ALLOWED

DOMAIN: Final = "lemonfiber"

CONF_PIN: Final = "pin"
"""The entry field holding the stack's certificate pin. The address and the key use Home Assistant's own names."""

LOGGER: Final = logging.getLogger(__package__)

MANUFACTURER: Final = "NightWorksIO"
MODEL: Final = "lemonfiber"

FIRST_SNAPSHOT_WITHIN: Final = SILENCE_ALLOWED * 2
"""Seconds setup waits for the stream's first dashboard before it is retried: twice the silence a stream is allowed."""

DIAGNOSIS_EVERY: Final = timedelta(hours=1)
"""How often the doctor's findings are read again when the dashboard has given no reason to sooner."""
