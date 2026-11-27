# Copyright (c) 2026 NightWorksIO
"""What a phone's push endpoint is registered with: a name, the distributor's address, and its WebPush key and secret."""

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class PushEndpointRegistering:
    """What one push endpoint is registered with.

    The address lets whoever holds it wake the phone, and the key and secret are
    what a wake is encrypted to, so none of the three is in the representation.
    """

    name: str
    """What to call it: lower-case letters, digits, dots, dashes and underscores."""
    endpoint: str = field(repr=False)
    """The `https` address the phone's UnifiedPush distributor gave."""
    p256dh: bytes = field(repr=False)
    """The phone's WebPush public key, an uncompressed P-256 point."""
    auth: bytes = field(repr=False)
    """The phone's WebPush secret."""
