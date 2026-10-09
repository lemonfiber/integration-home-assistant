# Copyright (c) 2026 NightWorksIO
"""What a member is playing, as a media player that shows and offers no control."""

from typing import TYPE_CHECKING, Final, override

from homeassistant.components.media_player import MediaPlayerEntity, MediaPlayerEntityDescription
from homeassistant.components.media_player.const import MediaPlayerEntityFeature, MediaPlayerState, MediaType
from homeassistant.core import callback

from .entity import MemberEntity, member_side

if TYPE_CHECKING:
    from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
    from lemonfiber.contract import Medium, Playback

    from .member import MemberCoordinator
    from .runtime import LemonfiberConfigEntry

PARALLEL_UPDATES: Final = 0
"""The entity is written by the member's stream, so it asks the stack nothing itself."""

PLAYING: Final = MediaPlayerEntityDescription(key="playing", translation_key="playing")

CONTENT_TYPES: Final[dict[Medium, MediaType]] = {"film": MediaType.MOVIE, "series": MediaType.EPISODE}
"""What Home Assistant calls each kind of thing a member can be playing. Anything else is named nothing."""


@member_side
async def async_setup_entry(
    entry: LemonfiberConfigEntry,
    theirs: MemberCoordinator,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add what the member is playing."""
    async_add_entities([TheirPlaying(theirs, entry, PLAYING)])


class TheirPlaying(MemberEntity, MediaPlayerEntity):
    """What a member is playing, from the first of their sessions: playing or paused, and idle with none.

    Unavailable until their stream has said what they are playing, and wherever
    the media server could not say.
    """

    _attr_supported_features = MediaPlayerEntityFeature(0)

    def __init__(
        self,
        coordinator: MemberCoordinator,
        entry: LemonfiberConfigEntry,
        description: MediaPlayerEntityDescription,
    ) -> None:
        """Describe the player and read what the member is playing."""
        super().__init__(coordinator, entry, description)
        self._read()

    def _read(self) -> None:
        sessions = self.coordinator.data.sessions()
        self._readable = sessions is not None
        first: Playback | None = sessions[0] if sessions else None
        self._attr_state = MediaPlayerState.IDLE if first is None else _standing(first)
        self._attr_media_title = None if first is None else first["title"]
        self._attr_media_series_title = None if first is None else first.get("series")
        self._attr_media_season = None if first is None else _numbered(first.get("season"))
        self._attr_media_episode = None if first is None else _numbered(first.get("episode"))
        self._attr_media_content_type = None if first is None else CONTENT_TYPES.get(first["medium"])
        self._attr_extra_state_attributes = {} if first is None else {"device": first["device"]}

    @property
    @override
    def available(self) -> bool:
        return super().available and self._readable

    @callback
    @override
    def _handle_coordinator_update(self) -> None:
        self._read()
        super()._handle_coordinator_update()


def _standing(session: Playback) -> MediaPlayerState:
    """Return whether a session is playing or paused."""
    return MediaPlayerState.PAUSED if session["paused"] else MediaPlayerState.PLAYING


def _numbered(number: int | None) -> str | None:
    """Return a season's or episode's number as Home Assistant shows one."""
    return None if number is None else str(number)
