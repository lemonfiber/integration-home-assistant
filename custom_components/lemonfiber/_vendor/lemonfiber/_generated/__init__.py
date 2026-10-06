# Copyright (c) 2026 NightWorksIO
"""The lemonfiber contract's shapes, generated from the artefact at 79bb11356f6a117d14293c49cd2d154164c5f439.

Generated from `contract/web-api.contract.json`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

from . import envelope as _envelope
from . import key_callable as _key_callable
from . import kinds as _kinds
from . import narrowing as _narrowing
from . import refusals as _refusals
from . import shared as _shared

from .envelope import *
from .key_callable import *
from .kinds import *
from .narrowing import *
from .refusals import *
from .shared import *

__all__: list[str] = []
__all__ += _envelope.__all__
__all__ += _key_callable.__all__
__all__ += _kinds.__all__
__all__ += _narrowing.__all__
__all__ += _refusals.__all__
__all__ += _shared.__all__
