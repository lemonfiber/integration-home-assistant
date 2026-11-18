# Copyright (c) 2026 NightWorksIO
"""The `served` envelope, and the shapes only `served` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import typing


class ServedEnvelope(typing.TypedDict):
    """The envelope carrying `served`."""

    api_version: int
    data: ServedReport
    host: typing.NotRequired[str | None]
    job: typing.NotRequired[str | None]
    kind: typing.Literal["served"]


class ServedReport(typing.TypedDict):
    """What a run serving the surface presents, answers to and wrote down."""

    fingerprint: typing.NotRequired[str | None]
    """What a phone pins for the certificate presented, where the run is encrypted."""
    named: typing.NotRequired[str | None]
    """The name a request has to carry beyond this machine, where the run is encrypted on
    a network.
    """
    unrecorded: typing.NotRequired[str | None]
    """Why where it is served could not be written down, where it could not."""


__all__ = [
    "ServedEnvelope",
    "ServedReport",
]
