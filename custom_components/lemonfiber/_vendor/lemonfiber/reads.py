# Copyright (c) 2026 NightWorksIO
"""Every path this client reaches, held here rather than spelled by a caller.

The contract carries kinds and no endpoints, so a path is knowledge this client
keeps for its callers. `scripts/the_doors_this_client_names.py` holds `Read` to
the reads the contract page names, in both directions.
"""

from enum import StrEnum
from typing import Final


class Read(StrEnum):
    """A read lemonfiber serves, answering with one envelope, named for the command it mirrors.

    Each one's docstring names the kind it answers with; `expect` narrows to it.
    """

    ALERTS = "alerts"
    """What the operator is told about: `alerts`."""
    BACKUPS = "backups"
    """Which backups are here to restore from, by name: `archives`."""
    BANDWIDTH = "bandwidth"
    """How the line is shared: `bandwidth`."""
    CATALOGUE = "catalogue"
    """What each service is for: `catalogue`."""
    CHECKS = "checks"
    """A diagnosis: `doctor`."""
    CLIENTS = "clients"
    """Which app to watch on: `clients`."""
    CONFIG = "config"
    """What the stack is configured to do, narrowed by `key`: `config`."""
    CREDENTIALS = "credentials"
    """Every credential the stack holds, and no value: `credentials`."""
    EXPLAIN = "explain"
    """What one word means, given `word`, or every word: `word` or `glossary`."""
    FORMS = "forms"
    """The forms offered, or what starting those named by `form` comes to: `forms` or `preview`."""
    FRONT_DOOR = "front-door"
    """The one address to hand somebody who lives here: `front-door`."""
    HELD = "held"
    """What `member` can watch, `most` of it: `held`."""
    HISTORY = "history"
    """What lemonfiber has already changed: `history`."""
    HOSTING = "hosting"
    """What this machine keeps running when nobody is watching: `hosting`."""
    MIGRATION = "migration"
    """What is already on this machine: `migration`."""
    NEWS = "news"
    """What a surface can mark as new: `news-items`."""
    OUTBOUND = "outbound"
    """Everything that leaves this machine: `outbound`."""
    PLUGINS = "plugins"
    """The plugins installed: `plugins`."""
    PROVENANCE = "provenance"
    """Where the services come from: `provenance`."""
    QUALITY = "quality"
    """What quality was asked for: `quality`."""
    REQUESTS = "requests"
    """Who is in the household and what each has asked for, narrowed by `member`: `household`."""
    SERVICES = "services"
    """What each service is doing, narrowed by `form`: `status`."""
    SPACE = "space"
    """Where the disk went: `space`."""
    STATUS = "status"
    """What the whole stack is doing: `status`."""
    STORAGE = "storage"
    """What the checks about the disk found: `doctor`."""
    STORED = "stored"
    """What this machine keeps of lemonfiber's: `stored`."""
    STUCK = "stuck"
    """The items whose downloads have stopped: `stuck`."""
    TRACE = "trace"
    """Where one item, `term`, got to: `trace`."""
    UNINSTALL = "uninstall"
    """What one removal, `tier`, would take: `uninstall`."""
    UPDATE = "update"
    """Where `what=stack` or `what=self` stands: `update` or `self-update`."""
    VERSION = "version"
    """The versions in play: `version`."""
    WIRING = "wiring"
    """What the stack wires to what: `wiring`."""

    @property
    def path(self) -> str:
        """Return the path this read is served on."""
        return f"{API}/{self.value}"


API: Final = "/api"
"""What every path begins with."""

LOGS: Final = "/api/logs"
"""What the services have been saying: a `log` envelope a line."""

BUNDLE: Final = "/api/bundle"
"""A support bundle, by name, handed over as the file it is."""

EVENTS: Final = "/api/events"
"""The live stream."""

ACTIONS: Final = "/api/actions"
"""Where every action is asked for, by name."""

JOBS: Final = "/api/jobs"
"""Where work already begun is asked about and released, by name."""

SESSION: Final = "/api/session"
"""Where a password is exchanged, once, for a session."""

CAPABILITIES: Final = "/api/capabilities"
"""What the stack says it can do, for the credential that asked."""
