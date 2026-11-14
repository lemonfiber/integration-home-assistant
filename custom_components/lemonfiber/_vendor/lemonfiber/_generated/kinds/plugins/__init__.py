# Copyright (c) 2026 NightWorksIO
"""The `plugins` envelope, and the shapes only `plugins` carries, gathered from its parts.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

from . import expected as _expected
from . import plugin_failing_as_declared as _plugin_failing_as_declared
from . import plugin_proving as _plugin_proving

from .expected import *
from .plugin_failing_as_declared import *
from .plugin_proving import *

__all__: list[str] = []
__all__ += _expected.__all__
__all__ += _plugin_failing_as_declared.__all__
__all__ += _plugin_proving.__all__
