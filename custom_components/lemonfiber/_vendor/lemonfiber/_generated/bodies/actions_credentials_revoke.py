# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/credentials-revoke`, and the shapes only `/api/actions/credentials-revoke` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class CredentialsRevokeAction(ActionRequest):
    """The action `credentials-revoke`, with the arguments it is posted with. `offer` carries the operator's yes."""

    ACTION = "credentials-revoke"

    offer: str | None = None
    """What was read before answering — the offer a repair's yes was read in, the
    listing a restore's was, what a replacement would stop — as it named itself.
    """
    plugin: str | None = None
    """The plugin an update or a removal acts on, by the id the record of what is
    installed lists it under.
    """
    credential: str | None = None
    """The credential a grant to a third-party plugin is of, by the setting the
    credentials read lists it under.
    """
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "CredentialsRevokeAction",
]
