# Copyright (c) 2026 NightWorksIO
"""The lemonfiber contract's shapes, generated from the artefact at 2112d04d879bc16f9a6f9f44aa4027613a48b803.

Do not edit: `just generate` rewrites this file from `contract/web-api.contract.json`,
and CI fails on any difference.
"""

import types
import typing

CONTRACT_API_VERSION: typing.Final = 1
"""The wire version these shapes were generated for."""


type Action = (
    ActionRemove
    | ActionRestore
    | ActionDelete
    | ActionWithdraw
    | ActionRepin
    | ActionReconfigure
    | ActionRevoke
    | ActionReinstate
)
"""What an undo does.

Tagged by what it does rather than by the field it sits in, so a reader parsing
one branches on a word rather than on which keys are present.
"""


class ActionDelete(typing.TypedDict):
    """Remove a path that was created."""

    does: typing.Literal["delete"]
    path: str
    """The path to remove."""


class ActionReconfigure(typing.TypedDict):
    """Put one field of a service's own resource back to what it held.

    The only reversal that needs the service itself: the value lives inside it,
    and nothing on the host can write it. A reversal that cannot reach the
    service says so rather than reporting the field restored.
    """

    does: typing.Literal["reconfigure"]
    field: str
    """The field to put back."""
    id: str
    """The identifier to change."""
    resource: str
    """The kind of resource."""
    value: typing.NotRequired[str | None]
    """What to put back, or `None` where it held nothing."""


class ActionReinstate(typing.TypedDict):
    """Make a revoked key good again.

    Worked out so the record of a revoke has a reversal to name, and never carried
    out: a key is revoked because something should stop holding it, and reinstating
    it would hand back what the revoke took away. Whatever still needs a key is
    minted a new one.
    """

    does: typing.Literal["reinstate"]
    name: str
    """The key's name."""


class ActionRemove(typing.TypedDict):
    """Remove the resource that was created."""

    does: typing.Literal["remove"]
    id: str
    """The identifier to remove."""
    resource: str
    """The kind of resource."""


class ActionRepin(typing.TypedDict):
    """Pin a service back to the version it was standing on.

    The one reversal nothing in this product carries out. Which version runs is
    decided by the materialised stack and by what Compose was told to start, and
    a reversal of settings and files reaches neither — so this is worked out,
    reported, and left for the operator rather than attempted.
    """

    current: str
    """The version this run moved it to, which has to still be the one running
    for putting the old one back to be putting anything back.
    """
    does: typing.Literal["repin"]
    previous: str
    """The version to put back."""


class ActionRestore(typing.TypedDict):
    """Restore a value, or remove it where there was none before (`None`)."""

    does: typing.Literal["restore"]
    key: str
    """The setting to restore."""
    value: typing.NotRequired[str | None]
    """What to restore it to, or `None` to remove it."""
    wrote: str
    """What lemonfiber put there, which has to still be there for putting the
    old value back to be putting anything back.

    Carried so that a reversal can ask whether it is undoing its own work.
    Without it a reversal knows only what it would like the setting to say,
    and a setting the operator has since chosen for themselves reads exactly
    like one nobody has touched.
    """


class ActionRevoke(typing.TypedDict):
    """Revoke the key a mint made."""

    does: typing.Literal["revoke"]
    name: str
    """The key's name."""


class ActionWithdraw(typing.TypedDict):
    """Take a region lemonfiber wrote back out of the file it was written into.

    Only where the region is still what was written. One that was edited since, or
    whose markers were, is somebody else's work now, and is left exactly as it is.
    """

    does: typing.Literal["withdraw"]
    key: str
    """The same file beneath the stack directory, as the record of what lemonfiber
    materialised names it.
    """
    owner: str
    """Whose region it is, as its markers name it."""
    path: str
    """The file the region is in."""
    written: int
    """The checksum of what was written between the markers, which has to still be
    what is there for taking it out to be taking out lemonfiber's own work.
    """


class Active(typing.TypedDict):
    """One download still coming down when a reduction was asked for."""

    name: str
    """What it is, as the client names it."""
    progress: int
    """How far along, from zero to a hundred."""
    protocol: str
    """Which client has it."""


class Address(typing.TypedDict):
    """Where the front door is reached, and what is worth knowing about the address."""

    caution: typing.NotRequired[str | None]
    """What is worth knowing about the address itself, where anything is. Absent
    for one that keeps working on its own.
    """
    url: str
    """The whole address, as it would be typed or followed."""


class Admitted(typing.TypedDict):
    """A session opened, and the moment it stops being one.

    The ending is carried rather than left for a client to work out, because a client
    that guessed would be a second opinion about who is admitted — and the two would
    disagree on the day somebody's clock is wrong.
    """

    member: typing.NotRequired[str | None]
    """The household member this session is for, where it is a member's.

    **Absent is the operator**, which is the whole of the discriminator. A second
    field naming which kind of person this is could disagree with this one, and
    the day they disagreed a client would have to choose which to believe.

    The id and nothing else. What that member is called, what they may watch and
    what they have left are read from the household report, which already carries
    all of it per member — so there is one fact here and no second copy of
    anything that could go stale against the read.
    """
    token: str
    """The secret this session is carried by, sent in the header the per-run token is."""
    until: str
    """When it stops being one, written as every other instant this product writes."""


class AdoptReport(typing.TypedDict):
    """What adopting a setup already here came to, or would come to."""

    back_up: list[str]
    """The host paths those services keep their data in, so a backup can be taken of
    exactly the right thing.
    """
    backed_up: typing.NotRequired[str | None]
    """Where the capture of those paths was written, once one has been taken.

    Absent on a rehearsal, which captures nothing, and absent where the setup
    mounted nothing worth capturing. Present on an adoption that went through,
    because an operator told a backup was taken is owed the path to it.
    """
    project: typing.NotRequired[str | None]
    """The project lemonfiber would manage, where exactly one could be adopted."""
    refusal: typing.NotRequired[str | None]
    """Why nothing was done, where nothing was."""
    rehearsed: bool
    """Whether this was a rehearsal: what would have happened, with none of it done.

    Said in a field of its own so that a rehearsal is never told from the real run by
    its wording alone.
    """
    stance: Stance
    """Where the act stands."""
    upgrades: list[CarryingReport]
    """The services whose databases a newer version would upgrade, and whose data
    therefore has to be backed up before anything opens it.
    """


class Affected(typing.TypedDict):
    """One thing that is wrong, as the expanded summary lists it."""

    check: str
    """The check that raised it."""
    downstream: list[str]
    """What is also wrong because of this, counted with it rather than again."""
    exit: typing.NotRequired[int | None]
    """How the service it is about exited, where it has and the engine said.

    The technical half of what happened, kept out of the summary so the plain
    words lead, and here for whoever wants the code.
    """
    meaning: str
    """What it costs the operator. The line expands to items an operator can act
    on, and an item that states only the event leaves the judgement it was
    supposed to save them.
    """
    onset: str
    """When the stack first saw it wrong since it last saw it right, in whole
    seconds since the epoch.

    The condition's own stamp, kept between runs, so every surface that reports
    the check names the same moment and a restart does not make an old fault new.
    """
    remedies: list[str]
    """What to do about it, most likely first."""
    severity: ProblemSeverity
    """How bad it is."""
    summary: str
    """What is wrong, in one line."""


class Alert(typing.TypedDict):
    """One interruption: what happened, which way, and how much it matters."""

    affected: list[str]
    """Every check this alert speaks for, the first being [`Self::check`]. More
    than one where the same event was grouped across several services.
    """
    check: str
    """The check this came from, so an alert and its condition cannot drift apart.
    Where several were grouped, the first of them.
    """
    exit: typing.NotRequired[int | None]
    """How the service it is about exited, where it has and the engine said;
    where several were grouped, how the first of them did.

    The technical half of what happened, kept out of the summary so the plain
    words lead, and here for whoever wants the code.
    """
    kind: str
    """What kind of event it is, shared by every instance of it."""
    meaning: str
    """What it costs the operator, which is the half between the event and the
    fix. \"The tunnel dropped\" and \"restart the gateway\" leave whoever reads
    them to work out for themselves whether anything leaked.
    """
    moment: Moment
    """Which way it went."""
    remedies: list[str]
    """What to do about it, most likely first. An alert that says what happened
    and not what to do is a notification, which is a different and worse thing.
    """
    severity: ProblemSeverity
    """How much it matters. A resolution takes the severity of what resolved,
    because \"the critical thing is over\" is itself worth the attention the
    critical thing had.
    """
    summary: str
    """What happened, in the words the condition was raised with."""


class AlertReport(typing.TypedDict):
    """What the operator will be told about, and what changing it came to."""

    changed: bool
    """Whether this call changed the answer."""
    exceptions: list[ExceptionReport]
    """Events set apart from the preset, quietest name first."""
    means: str
    """What that preset means, in the operator's terms."""
    preset: str
    """The preset in force for events with no exception of their own."""
    rehearsed: bool
    """Whether it only reported what it would have written."""


type Answer = AnswerHeld | AnswerSilent
"""How one download client answered about the limits on it."""


class AnswerHeld(typing.TypedDict):
    """It answered, in both directions."""

    answered: typing.Literal["held"]
    down: BandwidthHeld
    """What became of the download limit."""
    period: typing.NotRequired[Period | None]
    """Which side of the household's day it says it is on, where it keeps the
    hours itself.
    """
    up: BandwidthHeld
    """And of the upload one."""


class AnswerSilent(typing.TypedDict):
    """It did not answer, and this is what it said.

    Its own line rather than an absence, because a client nobody could reach is
    a client whose limits are unknown, and an unknown limit rendered as no
    limit is the report reading better than the stack is.
    """

    answered: typing.Literal["silent"]
    said: str
    """What went wrong, in the words of whatever refused."""


class Api(typing.TypedDict):
    """How lemonfiber talks to a service when seeding.

    The same shape on a plugin's service as on the stack's own, which is what lets a
    plugin name one of these adapters rather than supply one of its own.
    """

    key_source: KeySource
    """Where the credential comes from."""
    kind: ApiKind
    """Selects the client implementation."""
    path: typing.NotRequired[str | None]
    """The file holding the credential, where one applies."""
    version: typing.NotRequired[int | None]
    """The major version of the service's HTTP API — the `/api/vN` path segment.

    Required for the `servarr` shape and read there, because that one shape
    spans two versions (Sonarr and Radarr at v3, Lidarr and Prowlarr at v1),
    so the version is data rather than a guess from a service's name. Absent
    for the other kinds, whose one fixed version their client already knows.
    """


type ApiKind = typing.Literal[
    "servarr",
    "sabnzbd",
    "qbittorrent",
    "seerr",
    "bindery",
    "jellyfin",
    "bazarr",
    "audiobookshelf",
    "nzbhydra2",
]
"""The API shapes lemonfiber knows how to speak.

Four services share the `servarr` shape, which is what makes one client
enough for them. Bindery is its own kind deliberately: it is not a Servarr
application and Prowlarr's app sync does not reach it. Bazarr is its own for
the neighbouring reason: it is told about the \\*arrs rather than being one of
them, in a form body a client of the shared shape could not send.
"""


type AskingStanding = typing.Literal["unlimited", "within-quota", "near-quota", "quota-exhausted"]
"""Where one member stands against what a period allows them.

Four, and the one worth having is the middle: somebody told only when they have run
out has been told too late to do anything but wait, which is the answer this whole
feature exists to avoid handing anybody.
"""


type Assessment = typing.Literal["assessed", "unassessable"]
"""Whether a pass could assess drift — whether it had the record of what lemonfiber
last wrote to compare against.
"""


type Awaiting = typing.Literal["downloads"]
"""What an operation with no bound on it is waiting for.

A case rather than a sentence, so what an operation is waiting for is a value
something can be asked about. The words are built from it in one place below;
a phrase carried here instead would be a phrase every later surface had to
parse back into the fact it came from.
"""


class BackupManifest(typing.TypedDict):
    """The record written inside an archive, and read back to decide a restore.

    Everything a restore needs to know before it overwrites anything: what made
    the archive, when, what data root it was taken against, what it covers, whether
    it is sensitive, and the contents to list. Round-trips through JSON so the same
    value the capture wrote is the value the restore reads.
    """

    created_at: str
    """When it was taken. Opaque here; the surface stamps it from the clock."""
    data_root: str
    """The data root it was taken against, to notice a restore to a different one."""
    members: list[Member]
    """What is inside, for a listing shown before anything is overwritten."""
    product_version: str
    """The lemonfiber version that wrote it, checked against the one restoring."""
    schema: int
    """The archive format, checked before anything inside is trusted."""
    scope: Scope
    """What it covers."""
    sensitive: bool
    """Whether it carries credentials, and so must be handled as sensitive."""


class BackupReport(typing.TypedDict):
    """What a capture produced."""

    pace: Pace
    """What the capture moved, against what a capture is meant to stay inside.

    Read off the room check that already ran, so saying it costs nothing: the trees
    were walked to decide whether the archive would fit, and this is the same number
    put to a second use.
    """
    path: str
    """Where the archive was written, or — on a run that only said what it would
    capture — where it would have gone.
    """
    pruned: list[str]
    """The older backups retention pruned, oldest first — or would prune."""
    rehearsed: bool
    """Whether this run only said what it would capture.

    A flag rather than a second shape, because every other field means the same
    thing either way: a capture is settled before it is written — the room is
    measured, the manifest described, the name and the path derived, and retention
    worked out — so what a rehearsal reports is what a real run would report, with
    the one write left out. What changes is the tense a surface says it in.
    """
    scope: Scope
    """What the backup covers."""
    sensitive: bool
    """Whether it carries credentials, and so must be handled as sensitive."""


class BandwidthHeld(typing.TypedDict):
    """One direction on one client: what it was asked for, took, and is doing."""

    accepted: typing.NotRequired[int | None]
    """What it reports as in force."""
    asked: typing.NotRequired[int | None]
    """What it was asked to hold to, in bytes a second, where anything was."""
    moving: typing.NotRequired[int | None]
    """What it is moving right now, where it reported a figure."""
    verdict: BandwidthVerdict
    """What that adds up to."""


class BandwidthReading(typing.TypedDict):
    """One direction's limit, as declared and as it comes to."""

    limit: Limit
    """The limit as it was expressed."""
    resolved: Resolved
    """What it comes to against the measured line."""
    says: str
    """The limit and the line it was measured against, in one sentence.

    Carried rather than left to each surface, so the rule that a share is never
    shown without the figure it is a share of is kept in one place instead of
    three.
    """


type BandwidthVerdict = typing.Literal["unasked", "nothing-to-limit", "holding", "ignored", "overrunning"]
"""What became of one limit, in one direction, on one client."""


class BesideReport(typing.TypedDict):
    """What standing lemonfiber beside an existing setup came to, or would come to."""

    ports: list[MovedReport]
    """Where each service would listen instead, lowest original port first."""
    refusal: typing.NotRequired[str | None]
    """Why nothing was written, where nothing was."""
    rehearsed: bool
    """Whether this was a rehearsal: what would have happened, with none of it done.

    Said in a field of its own so that a rehearsal is never told from the real run by
    its wording alone.
    """
    stance: Stance
    """Where the act stands."""
    written: typing.NotRequired[str | None]
    """Where the Compose file that says so was written."""


class Beyond(typing.TypedDict):
    """A repair that has run out of chances, and where to go instead."""

    check: str
    """The check whose fault has outlasted every attempt at it."""
    remedy: Remedy
    """What to do about it now that lemonfiber has stopped offering to."""


class Bundle(typing.TypedDict):
    """What a support request said: what a bundle holds, and where it is if it exists.

    One record with an absent path rather than two shapes, because the two answers
    are the same answer at two moments: both list what goes in the file and say how
    large it is, and only one of them has a file to point at. A caller reads whether
    there is a path to know which it has.
    """

    bytes: int
    """How large the file is, or would be."""
    contents: Contents
    """Everything it holds, gathered, redacted and read back."""
    path: typing.NotRequired[str | None]
    """Where it was written, or nothing where a run that writes nothing described it."""
    rehearsed: bool
    """Whether this was a rehearsal: what would have happened, with none of it done.

    Said in a field of its own so that a rehearsal is never told from the real run by
    its wording alone.
    """
    would_go: typing.NotRequired[str | None]
    """Where it would be written, on the run that only describes one.

    The other half of what a description is for. What goes in the file and how
    large it is answer *whether* to make it; where it lands answers *where to find
    it*, and an operator deciding at a shell needs both at the one moment the
    answer can still change what they do. Resolved by the same function the run
    that writes resolves it with, so the path shown and the path written are one.

    Absent on a run that wrote one — `path` is then where it went — and absent on a
    machine that would not say where lemonfiber keeps its own files, which is the
    one destination of the three that needs that answer.
    """


class Candidate(typing.TypedDict):
    """One completed download, and what reclaiming it would come to."""

    bytes: int
    """What it occupies."""
    consequence: typing.NotRequired[str | None]
    """What removing it costs, where it costs anything."""
    name: str
    """What both sides call it."""
    standing: SeedingStanding
    """Where it stands."""


class Cap(typing.TypedDict):
    """A monthly allowance, and what to do at the end of it."""

    exceeded: WhenExceeded
    """What happens when it is reached, chosen when the cap was declared."""
    monthly: int
    """The allowance, in bytes."""


class Capabilities(typing.TypedDict):
    """Every capability this stack has, by the path its request is served at."""

    capabilities: dict[str, CapabilityState]
    """What each comes to for the credential that asked. A request this stack does
    not have is absent rather than listed as anything.
    """


type CapabilityState = typing.Literal["available", "unconfigured", "unpermitted"]
"""What one capability comes to for the credential that asked."""


class Capacity(typing.TypedDict):
    """What the line was measured to carry."""

    down: int
    """Bytes a second down."""
    source: Source
    """Where the figure came from."""
    taken: int
    """When it was taken, in seconds since the epoch."""
    through_tunnel: bool
    """Whether the path it was measured over goes through the VPN tunnel."""
    up: int
    """Bytes a second up.

    Measured apart from the download, because a home connection is asymmetric
    and a single figure for both would make every upload share far larger than
    the operator meant.
    """


class CarryingReport(typing.TypedDict):
    """What adopting one existing service would come to."""

    backup_first: bool
    """Whether its database must be backed up before lemonfiber opens it."""
    because: str
    """What that means for this service's data, in the operator's terms."""
    existing: str
    """The version standing here now."""
    ours: str
    """The version lemonfiber pins."""
    refused: bool
    """Whether lemonfiber will not do this at all."""
    service: str
    """The service, by the name lemonfiber runs it under."""
    verdict: str
    """Which of the two is the later, in one word."""


class CatalogueReport(typing.TypedDict):
    """What this stack holds, and what it used to."""

    removed: list[RemovedService]
    """The services this stack has dropped, in the order it records them.

    Empty for a stack that has never dropped anything, which is a different thing
    from a stack that keeps no record — and told apart by the fact that a stack
    keeping no record cannot be read as having dropped something it did.
    """
    services: list[CataloguedService]
    """The services, in the order the stack declares them.

    Every service the manifest holds rather than the ones some form would start:
    what a service is *for* is the question being asked, and an answer narrowed to
    what is running would leave the operator unable to ask about the one they are
    deciding whether to run.
    """


class CataloguedService(typing.TypedDict):
    """What one service is for, as the stack declares it."""

    criticality: Criticality
    """How much its absence matters."""
    describes: str
    """What it does for the operator, in plain language."""
    id: str
    """The service's id, which is also its Compose service name."""
    name: str
    """What it is called in front of an operator."""
    without_it: str
    """What going without it costs.

    Carried beside the description rather than left to a separate question,
    because the pair is what turns an inventory into a judgement: knowing that
    Bazarr finds subtitles says nothing about whether its being down matters.
    """


class Cause(typing.TypedDict):
    """One thing that could be behind a symptom, and how to tell it from the others."""

    because: str
    """What is wrong."""
    fix: str
    """What to do about it."""
    tell: str
    """How to tell this cause from the others under the same symptom."""


class CertificateReport(typing.TypedDict):
    """What asking for the certificate to be replaced came to."""

    consequence: str
    """What replacing it means for every phone already paired."""
    fingerprint: typing.NotRequired[str | None]
    """What a phone would pin now: the new certificate where it was replaced, the one
    kept where it was not, and nothing where none has been made.
    """
    rehearsed: bool
    """Whether this was a rehearsal: what would have happened, with none of it done.

    Said in a field of its own so that a rehearsal is never told from the real run by
    its wording alone.
    """
    replaced: bool
    """Whether it was replaced. Unconfirmed, it is not, and what replacing it costs is
    what is said.
    """


class ChangeReport(typing.TypedDict):
    """One change lemonfiber made, and whether it could be put back."""

    alongside: int
    """How many changes that one operation made, this one among them.

    An operation is the unit an operator agreed to, and undoing half of one leaves a
    machine in a state nobody chose — so what a single line would take with it is on
    the line rather than left to be counted off the list.
    """
    at: str
    """When it was made, as whole seconds since the Unix epoch, written in decimal.

    A string of digits rather than a number, because it is the stamp the record keeps
    and a stamp is compared and stored as text; what it counts is stated here so a
    reader can turn it into a time without guessing at a format.

    **`0` means the clock was unreadable when the change was written**, not that it
    was made at the epoch: it is how a machine whose clock would not answer stamps a
    change. It is not an instant, so two changes both stamped `0` were not made at
    the same moment, and a reader showing it as a date in 1970 would be inventing
    one.
    """
    because: typing.NotRequired[str | None]
    """Why it could not go further, where it could not."""
    did: str
    """What it did, in the operator's terms."""
    instead: typing.NotRequired[str | None]
    """What to do instead, where there is something."""
    operation: str
    """The operation that made it — a seed, a reconfigure, an applied fix — so a
    history reads as what happened rather than as bare diffs.
    """
    reversal: ChangeReversal
    """How far it could be put back."""
    target: str
    """What it was made to."""


type ChangeReversal = typing.Literal["whole", "partial", "none"]
"""How far a change can be put back.

Published as the closed set it is, rather than as a word a reader has to trust will
be one of three: a surface that lays out a history branches on it, and a set the
contract names is one a generated reader can match exhaustively.
"""


class Changed(typing.TypedDict):
    """What one run of this command did to the machine."""

    installed: bool
    """Whether it installed it, rather than took it back."""
    name: str
    """The command it acted on."""
    rehearsed: bool
    """Whether this was a rehearsal, in which case nothing above happened."""
    started: bool
    """Whether it started the command, which only installing does."""
    touched: list[str]
    """Everything it wrote or removed, so nothing goes unnamed in either direction."""


type ChangelogState = typing.Literal["current", "pending", "stale"]
"""Whether the record describes what this build could have shipped.

The three the specification names, and the distinction between the last two is
the one worth keeping: being behind the tags is a lag, and contradicting them is
a fault.
"""


type Chosen = ChosenDerived | ChosenNamed | ChosenRefused
"""How the front door came to be the one it is."""


class ChosenDerived(typing.TypedDict):
    """Worked out from what the stack declares, which is what a stack whose
    operator has named nothing answers.
    """

    chosen: typing.Literal["derived"]


class ChosenNamed(typing.TypedDict):
    """Named by the operator, by the id the stack declares it under, and it is the
    door.
    """

    chosen: typing.Literal["named"]
    door: str


class ChosenRefused(typing.TypedDict):
    """Named by the operator and refused. The worked-out door stands, and this
    carries what was named and why it is not it.
    """

    chosen: typing.Literal["refused"]
    door: Refusal


type Code = str
"""A stable identifier for a kind of problem.

Stability is the whole point: an operator who searches for a code should find
the same answer a year later. Every code is declared in the error crate's `codes`
module, and a code is never recycled.
"""


class Coming(typing.TypedDict):
    """One download still coming down when the removal was asked for."""

    name: str
    """What it is, as the client names it."""
    progress: int
    """How far along, from zero to a hundred."""


type Condition = typing.Literal["inactive", "degraded", "partial", "active"]
"""What a whole set of services amounts to."""


class ConfigReport(typing.TypedDict):
    """The answer to a configuration command."""

    changed: bool
    """Whether this command changed, or would change, a setting."""
    consequence: typing.NotRequired[str | None]
    """What this change costs, where making it decides something with a
    consequence — moving the library, turning port forwarding off, or naming a
    front door. Stated for a change that is only staged as well as one that
    landed, since the moment before it happens is the moment it is worth reading.
    Absent for a read, and for a change to a setting nobody catalogued a cost for.
    """
    rehearsed: bool
    """Whether this was a rehearsal, so a change that `changed` reports was one
    that *would* be made rather than one that was.
    """
    review: typing.NotRequired[Review | None]
    """The difference between the configuration in force and the one proposed, and
    where that proposal stands: applied, staged for a confirmation, turned away,
    or nothing to do. Absent for a read, which proposes nothing.
    """
    settings: list[SettingReport]
    """The settings asked about — one for a lookup, all of them for a listing."""


class ConflictReport(typing.TypedDict):
    """A port lemonfiber wants for a service that something else already answers on."""

    held_by: str
    """The project already holding it."""
    port: int
    """The host port both want."""
    wanted_by: str
    """The lemonfiber service that would publish it."""


class Consumption(typing.TypedDict):
    """One line of the accounting."""

    category: SpaceCategory
    """What it is about."""
    reclaim: Reclaim
    """What getting it back would cost."""
    tally: Tally
    """What it occupies, counted both ways."""


class Contents(typing.TypedDict):
    """Everything gathered for a bundle, and everything that could not be."""

    missing: list[str]
    """What could not be collected, named.

    Named rather than passed over: a bundle from a machine whose diagnostics will not
    run is exactly the bundle worth having, and a gap nobody mentions reads as an
    absence of trouble rather than as an absence of information.
    """
    pieces: list[Piece]
    """The files, in the order a reader would want them."""
    taken: Taken
    """Where and when it came from."""
    terms: Terms
    """How it was made, and what its operator chose."""


type Cost = typing.Literal["cheap", "consequential"]
"""What changing a decision costs."""


class Counted(typing.TypedDict):
    """One of the two counts the request service keeps, and what it has left."""

    limit: typing.NotRequired[int | None]
    """How many the period allows. Absent where nothing limits them, which is a
    different answer from a limit of nought.
    """
    period: typing.NotRequired[str | None]
    """How long the period is, in the words a household says it in — absent where
    the count runs from the beginning rather than over a window.
    """
    remaining: typing.NotRequired[int | None]
    """How many more they may ask for. Absent where nothing limits them."""
    used: int
    """How many the period has already counted against them."""


class Coverage(typing.TypedDict):
    """How much of a traced series is here, season by season — the aggregate that turns a
    single furthest stage into an answer about the whole. The counts are of parts someone
    asked for; what nobody asked for is reported beside them, never folded in.
    """

    have: int
    """How many wanted parts are here, across every season."""
    seasons: list[SeasonCoverage]
    """Each season, in order."""
    unmonitored: int
    """How many parts nobody asked for, across every season."""
    wanted: int
    """How many parts were asked for, across every season."""


type CredentialReach = CredentialReachUpdated | CredentialReachPending | CredentialReachFailed
"""How far a rotation reached one consumer."""


class CredentialReachFailed(typing.TypedDict):
    """It could not be updated. Named rather than dropped, because a consumer left
    holding the old value is the failure this list exists to surface.
    """

    detail: str
    """Why it could not be."""
    reach: typing.Literal["failed"]


class CredentialReachPending(typing.TypedDict):
    """It will hold the replacement once one more thing happens, and that thing is
    named. A consumer reading the value out of a container's environment has it
    fixed at the moment the container was created, so recording a new one is
    only half of reaching it.
    """

    detail: str
    """What still has to happen, written as the command that does it."""
    reach: typing.Literal["pending"]


class CredentialReachUpdated(typing.TypedDict):
    """It now holds the replacement."""

    reach: typing.Literal["updated"]


type CredentialState = typing.Literal["absent", "active", "stale", "invalid", "rotating", "superseded"]
"""Where a credential stands, as far as lemonfiber can tell without spending it.

Six states rather than a boolean because the operator's next move differs for
each: an absent credential is one to supply, a stale one is one to prove, an
invalid one is one to replace, and the two rotation states exist so a run
interrupted half-way through a replacement is legible rather than mysterious.
"""


type Criticality = typing.Literal["critical", "core", "important", "enhancing", "optional"]
"""How much a service's absence costs.

Serialisable as well as readable, because it reaches an operator: a status
report that says a service is down without saying whether that matters
leaves them to guess, and the manifest already holds the answer.
"""


type DashboardProtocol = typing.Literal["usenet", "torrent"]
"""Which protocol a transfer is moving over, since the same download reads
differently on each — a Usenet download has no peers, a torrent has no server.
"""


type DashboardReading = DashboardReadingKnown | DashboardReadingStale | DashboardReadingUnknown
"""A figure a source reports, kept apart from the two ways it can be missing.

Zero is a value a source gave; stale is the last value a source that has since
gone quiet gave; unknown is a source that never answered at all. Collapsing any
two of them sends an operator after the wrong problem — a stalled download and
a dashboard that simply stopped polling look identical only if the code lets
them.
"""


class DashboardReadingKnown(typing.TypedDict):
    """The source answered this refresh with a value — which may legitimately be
    zero.
    """

    reading: typing.Literal["known"]
    value: int


class DashboardReadingStale(typing.TypedDict):
    """The source did not answer this refresh; this is the last value it gave."""

    reading: typing.Literal["stale"]
    value: int


class DashboardReadingUnknown(typing.TypedDict):
    """The source has never answered, so nothing can be said about it."""

    reading: typing.Literal["unknown"]


class Device(typing.TypedDict):
    """A kind of device somebody in the house might watch on."""

    caution: typing.NotRequired[str | None]
    """What is worth knowing before starting, where anything is."""
    client: str
    """What to use on it."""
    deep_link: typing.NotRequired[str | None]
    """A link that opens the app already pointed at this server, where the app is known to
    take one, with `{address}` where the server's address goes. Absent otherwise, and a
    hand-off then carries the address alone as its code, which the app is pointed at by
    scanning or typing.
    """
    device: str
    """What somebody would call the device they are holding."""
    instead: typing.NotRequired[str | None]
    """What to do instead where this is a bad device to be stuck with."""
    open_source: bool
    """Whether the app named is open source. A closed one may be named, with this false
    beside it, and is never the one recommended.
    """
    support: Support
    """How well served it is."""


type Disposition = typing.Literal["shown", "recorded", "rehearsed", "held", "reapplied", "would-reapply"]
"""What a quality command did to the stored choice."""


class Disturbances(typing.TypedDict):
    """What acting on this stack would take away, one answer per way of acting.

    Named by the situation rather than by the verb, because the verb has two
    spellings: the command line stops named services with `stop` and the HTTP
    surface spells that same operation `down`. These bytes are what both surfaces
    answer with, so a table keyed by verb would be right for one caller and wrong
    for the other. A field each caller maps its own word onto is right for both.

    Carried on the status reading because a surface deciding whether to stop
    something has already read that, and because none of these lengths depends on
    what the stack is currently doing — they are the clocks the run is held to,
    which is a property of the configuration. A second read to learn a length is
    a read a surface would skip, and then it would estimate.
    """

    restarting: TakesAway
    """Restarting services."""
    starting: TakesAway
    """Bringing services up, whether a whole form or named services inside one."""
    stopping: TakesAway
    """Taking services down, interrupting anything still arriving."""
    stopping_after_downloads: TakesAway
    """Taking the stack down once everything still arriving has landed.

    Whole forms only: stopping named services has no such wait to ask for,
    and a caller that asks for both at once is refused.
    """
    switching: TakesAway
    """Changing the running set, which stops whatever falls outside the new one."""


type DoctorCategory = typing.Literal[
    "environment", "storage", "network", "vpn", "credentials", "services", "providers", "queue", "config"
]
"""The family a check belongs to, so a run can be narrowed to one of them.

These are the diagnostic categories the product recognises; the checks that
fill each one arrive over time, so a category may name more than lemonfiber
can yet establish.
"""


class DoctorReport(typing.TypedDict):
    """What a diagnostic run found, and what it amounts to."""

    findings: list[Finding]
    """Each finding, in the order the checks produced them."""
    overall: Overall
    """What the findings amount to, as one word."""
    rehearsed: bool
    """Whether this was a rehearsal: what would have happened, with none of it done.

    Said in a field of its own so that a rehearsal is never told from the real run by
    its wording alone.
    """


type DoctorVerdict = (
    DoctorVerdictPass | DoctorVerdictWarn | DoctorVerdictFail | DoctorVerdictUnverified | DoctorVerdictSkipped
)
"""How a single check turned out.

\"Could not check\" (`Unverified`) is its own variant rather than a level of
severity, so a check that could not run can never be mistaken for one that
passed — the dishonesty this whole subsystem exists to prevent.
"""


class DoctorVerdictFail(typing.TypedDict):
    """Not working."""

    cause: typing.NotRequired[Problem | None]
    """The problem that produced this one, where several share a root."""
    code: Code
    """The stable identifier for this kind of problem."""
    detail: typing.NotRequired[str | None]
    """The underlying technical detail, available but never leading."""
    meaning: str
    """What it means for the operator."""
    outcome: typing.Literal["fail"]
    remedies: list[Remedy]
    """What to do, most likely first."""
    severity: ProblemSeverity
    """How much it matters."""
    state: ProblemState
    """Where it stands with respect to being fixed."""
    summary: str
    """What happened, in one plain sentence."""


class DoctorVerdictPass(typing.TypedDict):
    """Verified working, with the evidence worth showing."""

    note: typing.NotRequired[str | None]
    """What was observed, where stating it helps — an address, a port."""
    outcome: typing.Literal["pass"]


class DoctorVerdictSkipped(typing.TypedDict):
    """A prerequisite was absent, so the check did not apply."""

    outcome: typing.Literal["skipped"]
    reason: str
    """Why the check did not apply."""


class DoctorVerdictUnverified(typing.TypedDict):
    """Could not be established. Never a pass."""

    outcome: typing.Literal["unverified"]
    reason: str
    """Why it could not be determined."""
    remedy: Remedy
    """What the operator can do to get an answer."""


class DoctorVerdictWarn(typing.TypedDict):
    """Working, but degraded or risky."""

    cause: typing.NotRequired[Problem | None]
    """The problem that produced this one, where several share a root."""
    code: Code
    """The stable identifier for this kind of problem."""
    detail: typing.NotRequired[str | None]
    """The underlying technical detail, available but never leading."""
    meaning: str
    """What it means for the operator."""
    outcome: typing.Literal["warn"]
    remedies: list[Remedy]
    """What to do, most likely first."""
    severity: ProblemSeverity
    """How much it matters."""
    state: ProblemState
    """Where it stands with respect to being fixed."""
    summary: str
    """What happened, in one plain sentence."""


class Dropped(typing.TypedDict):
    """A profile left out of a closure, and what it would have needed.

    The provider travels with the profile because a name on its own sends the
    operator looking for a fault. What they have is a stack not configured for
    one of the two ways of downloading, which is a sentence rather than a word.
    """

    needs: StackProtocol
    """The provider it cannot run without."""
    profile: str
    """The profile that will not run."""


class Duration(typing.TypedDict):
    nanos: int
    secs: int


class Edited(typing.TypedDict):
    """A setting changed outside lemonfiber since it last wrote one.

    Both sides, so the operator chooses between them rather than being told one of
    them lost. Values a listing withholds are withheld here too — a report a script
    can log must not be the one place a password is printed.
    """

    found: str
    """What the file holds now."""
    secret: bool
    """Whether either value was withheld rather than shown."""
    wrote: str
    """What lemonfiber last wrote there."""


class Elsewhere(typing.TypedDict):
    """A request one of the stack's services makes, which is not lemonfiber's."""

    destination: str
    """Where its requests go, in the terms an operator would recognise.

    Empty means it reaches nothing, which is an answer. It never means *and we
    do not know*: that is [`Self::recorded`], and the two must not be read as one
    — an unknown service rendered as an empty destination would be this product
    claiming nothing leaves the machine on the strength of having no idea.
    """
    origin: ValueOrigin
    """Whose request it is: the stack's own, or an installed plugin's, named.

    A column in this account rather than an account of its own, because what leaves
    this machine is one question however many parties are asking it.
    """
    purpose: str
    """What it asks for."""
    recorded: bool
    """Whether lemonfiber ships a record of what this service reaches.

    False for a service that arrived in the stack after this build was made, or
    from an operator's own fork. It is listed anyway, because the alternative —
    leaving it out — is a privacy inventory that is complete-looking and short,
    and a reader counting the services on their machine against the ones on this
    list is the reader this surface exists for.
    """
    service: str
    """The service, by the id the stack declares it under."""


type Ending = typing.Literal["updated", "not-fetched", "not-started", "not-reached"]
"""How one service's update ended."""


class Entry(typing.TypedDict):
    """One change, as a reader meets it."""

    reference: typing.NotRequired[str | None]
    """Where it was reviewed, where it was reviewed anywhere."""
    requirements: list[str]
    """The requirements it served, which are the link rather than the headline."""
    summary: str
    """What changed, in the words it was written in."""


class Estimate(typing.TypedDict):
    """About how much room one request will want.

    Carried as a number and a word rather than as a rendered string, so a surface can
    put it in a column and still say what it is. The word is not decoration: a figure
    with nothing hedging it is a promise, and this cannot keep one.
    """

    bytes: int
    """About how many bytes it will take."""
    measured: bool
    """Whether this was measured. Always false — nothing here has measured anything,
    and the field is present so that a surface rendering it cannot forget to say so.
    """


class ExceptionReport(typing.TypedDict):
    """One event kind the operator set apart from the preset."""

    kind: str
    """The kind of event, by the name a finding gives it."""
    wanted: bool
    """Whether it is heard about, whatever the preset would say."""


class Expect(typing.TypedDict):
    """What the answer has to be.

    A status is a claim about the network path rather than about the service: Docker
    publishes a port by putting a proxy in front of it, and that proxy accepts a
    connection before knowing whether anything inside is listening. So a status alone
    is not evidence — except for a refusal, which is the one answer no port proxy can
    produce.

    **A key of the four key-wise constraints is a place rather than a name.** A plain
    name is a top-level member, and one beginning with `/` is a JSON Pointer, extended
    with a step that picks an entry of a list by a field it holds. A flat name was enough while every service answered a flat object, and the
    only thing it could say about a service that nests its payload was that the envelope
    was there — which is a probe that passes by observing that something replied.
    """

    body_starts_with: typing.NotRequired[str | None]
    """What the body must begin with, where it is not JSON."""
    content_type: typing.NotRequired[str | None]
    """A substring of the content type the answer was served as."""
    json: typing.NotRequired[dict[str, Expected] | None]
    """Places the answer must carry, each with the exact value it must hold."""
    json_array_min: typing.NotRequired[int | None]
    """The answer read as an array, with at least this many entries.

    A catalogue is very often a list rather than an object, and none of the
    object-shaped constraints can say anything about one.
    """
    json_at_least: typing.NotRequired[dict[str, int] | None]
    """Places the answer must carry, each with a number it must not be below."""
    json_has_keys: typing.NotRequired[list[str] | None]
    """Places the answer must carry, whatever they hold."""
    json_is_absent: typing.NotRequired[bool | None]
    """The answer did not parse as JSON at all.

    Which is what a service that serves its application shell for every path it does
    not implement answers — and the reason a status alone proves nothing against
    one: the shell comes back `200` whether the API behind it exists or not, so what
    has to be said is that the body was *not* a document.
    """
    json_types: typing.NotRequired[dict[str, ExpectedKind] | None]
    """Places the answer must carry, each with the kind of value it must be."""
    status: typing.NotRequired[int | None]
    """The status the answer must carry."""


type Expected = bool | int | str
"""Exactly what a place must hold.

Three kinds and no nesting: a flag that must be set, a number that must match, or a
word. A value deeper than this is asking about a document rather than about a claim
— and where the thing worth asserting is deeper *in* the answer, the key reaches it
rather than the value growing to match.
"""


type ExpectedKind = typing.Literal["bool", "int", "str", "list", "dict"]
"""The kind of value a key must hold.

Five, and closed. A name outside them is one no runner could evaluate, and an
assertion nothing evaluates is a proof that silently checks less than it says —
which is worse than one that fails.

Named for what it is the kind *of*, rather than `Kind`, because this is published
and whoever generates from it flattens every definition into one scope. `Kind` is
the one name there a generator is certain to want for itself: every envelope this
contract describes is keyed by its `kind`, so the union of them is a `Kind` too, and
two of them in one module is a definition nothing can be compiled against.
"""


type Facing = typing.Literal["asking", "watching", "shelf", "operators", "carriage", "unstated"]
"""What a service published to the local network is to the people in the house."""


type Filenames = bool
"""Whether media filenames are shown as they are.

Replaced unless asked otherwise. A library's contents are not a credential, but they
are the one thing in a bundle that says something about the person rather than about
the machine, and replacing them costs a diagnostic a reader can still follow — the
marks keep two mentions of one file recognisable as one file.

Read from the bare flag a surface carries rather than from a name of its own,
because that is what both surfaces have: `--filenames` on a command line and a
`filenames` in a request body are one word that is there or is not. Which way
round it reads is decided here, once — a surface that read it the other way
round would put a library's contents in a file people post in public.
"""


class Filtered(typing.TypedDict):
    """A service a closure asked for that the configuration leaves out, and why."""

    forms: list[str]
    """The forms that asked for it, in the order the stack declares them."""
    id: str
    """The service's identifier."""
    name: str
    """What it is called in front of an operator."""
    needs: StackProtocol
    """The provider it cannot run without."""
    profile: str
    """The profile it belongs to, which is what the configuration leaves out."""


class Finding(typing.TypedDict):
    """One thing a check established, and how it turned out."""

    category: DoctorCategory
    """The family this belongs to."""
    caused_by: typing.NotRequired[str | None]
    """The check whose finding explains this one, where another does.

    Set after the run rather than by the check itself: a check is independent
    by construction and cannot see what any other found, which is a property
    worth keeping.
    """
    check: str
    """A stable identifier for the thing checked, such as `vpn.egress-match`."""
    onset: typing.NotRequired[str | None]
    """When the stack first saw this check wrong since it last saw it right, in whole
    seconds since the epoch.

    Set after the run from the store of conditions, like [`Self::said`], so it is
    the moment the health summary names for the same check and a restart does not
    move it. Absent where the finding says nothing is wrong, and where the checks
    ran for something other than a diagnosis.
    """
    origin: ValueOrigin
    """Whose check this is: one this build ships, or one a named plugin contributed.

    Carried rather than read off the identifier. A contributed check's id is
    namespaced with the plugin's, and a reader could decode that from the colon —
    but an origin a reader has to decode is one a reader gets wrong, and the day a
    bundled id grew a colon every such reader would misattribute it in silence.
    """
    said: typing.NotRequired[str | None]
    """What the service said for itself, lately.

    Carried on the finding rather than left for the operator to go and fetch,
    because the explanation is almost always in it: a check can say a service is
    not answering, and only the service can say why. Absent where the finding is
    not about a service, where the service is fine, or where the engine would not
    say — an empty section would be a promise of evidence that is not there.

    Set after the run, like [`Self::caused_by`], since reading a service's output
    is not the check's own business and a check that did it would be doing two
    things.
    """
    service: typing.NotRequired[str | None]
    """The service this is about, where it is about one.

    Absent for the checks that are about the machine rather than about
    something running on it — the environment, the filesystem, the operator's
    own choices. Carried so that one service's trouble can be attributed to
    the service underneath it rather than counted as one more independent
    thing wrong.
    """
    service_name: typing.NotRequired[str | None]
    """What the stack calls that service in front of an operator.

    Carried beside the id rather than left for a surface to derive, because the id is
    a key and not a name: capitalising `qbittorrent` does not arrive at qBittorrent,
    and the stack has already written the name down. Absent where the finding is about
    no service, and where the stack declares no service by that id — an id standing in
    for a name would put the key back in front of the operator.

    Set after the run, like [`Self::caused_by`], from the same manifest that says
    which service depends on which.
    """
    title: str
    """The one-line summary of what was checked."""
    verdict: DoctorVerdict
    """How it turned out."""


class Findings(typing.TypedDict):
    """What a proposed change comes to on this machine.

    Empty on every change that comes to nothing beyond its value, which is most of
    them: a report full of empty lists about a timezone would teach the operator to
    skip the one that matters.
    """

    active: list[Active]
    """What is still coming down, where a reduction would interrupt it."""
    edited: typing.NotRequired[Edited | None]
    """The hand-edit found in the configuration file, where one was found."""
    keeps: list[str]
    """What this change leaves exactly as it is, said in full — because an operator
    dropping a way of downloading is weighing whether they lose what they built
    with it.
    """
    library: list[LibraryPath]
    """The library paths the services hold, and what moving the data location does
    to each. Empty for every change that does not move it.
    """
    opens: list[Opening]
    """What this change newly asks the operator for, in the order they meet it."""
    stops: list[str]
    """What this change stops running, by service name."""


class Footprint(typing.TypedDict):
    """The memory the stack estimates a set of services needs.

    An estimate by name as well as by description, because a figure read as a
    measurement is one an operator believes and acts on. It is the sum of what each
    service declares; nothing here has looked at anything running.
    """

    estimated_mib: int
    """The sum of the estimates the services declare, in MiB."""
    unestimated: list[str]
    """The services that declare no estimate, and so are not in the sum."""


class Foreign(typing.TypedDict):
    """Something beneath the data location that the stack did not put there."""

    at: str
    """The directory it is in, relative to the data location — or the file itself,
    where it sits directly in the data location.
    """
    bytes: int
    """What they occupy."""
    files: int
    """How many files were found under it."""


class FormReport(typing.TypedDict):
    """One form the stack declares, as a listing shows it.

    The manifest's own words rather than lemonfiber's: forms come from the stack, so a
    stack of somebody's own names and describes them however it likes, and a listing that
    paraphrased would be describing a different stack from the one being run.
    """

    composable: bool
    """Whether it can be started alongside another form.

    Worth saying in the listing rather than only when a combination is refused: an
    operator choosing between two forms is exactly who needs to know they are a choice.
    """
    description: str
    """What it is for, in one line."""
    id: str
    """What to type to start it."""
    name: str
    """What it is called."""


class FormsReport(typing.TypedDict):
    """Every form this stack declares."""

    forms: list[FormReport]
    """The forms, in the order the stack declares them."""


type Freshness = FreshnessLive | FreshnessAsOf
"""How much a reading can be relied on."""


class FrontDoorBeside(typing.TypedDict):
    """A service the household can reach that is not the front door, and why it is not.

    Carried rather than left out, because the decision is the useful part: an operator
    who can see that the index over every service was considered and refused has been
    told something, where one shown a single name has only been given an answer.
    """

    address: typing.NotRequired[Address | None]
    """The address to hand somebody for this service, read from this machine at the
    moment of asking rather than remembered.

    **Carried because not-the-door is not nowhere.** A household member wanting to
    watch something, or to ask for something, wants the service that faces them —
    and which of the two happens to be the front door is an operator's
    arrangement, not an answer to their question. Without this a surface can hand
    them only whichever one the door turned out to be, and say nothing at all
    about the other.

    Absent where the stack declares no port for it, for the reason the door's own
    address is absent then: an address with no port on it is one a browser answers
    with a refusal, and the manifest is where a port is declared.
    """
    because: str
    """Why it is not somewhere to begin."""
    facing: Facing
    """What it is to the household."""
    service: str
    """The service, by the name it shows itself under."""


class FrontDoorReport(typing.TypedDict):
    """The household's one front door: which service it is, where it stands, and what
    else they can reach that is not it.
    """

    address: typing.NotRequired[Address | None]
    """The address to hand them, read from this machine at the moment of asking
    rather than remembered. Absent where there is no door, and where there is
    one on a machine that will say neither what it is called nor where it is.
    """
    beside: list[FrontDoorBeside]
    """Everything else the household can reach, and why none of it is the door."""
    chosen: Chosen
    """How this came to be the door: worked out from what the stack declares, named
    by the operator, or named by them and refused.

    Carried as a state rather than left to the sentence beneath it, for the reason
    the standing is: an operator whose setting was refused reads the sentence, and
    a browser, a script or a dashboard reads this.
    """
    facing: typing.NotRequired[Facing | None]
    """What that service is to them. Absent for the same reason."""
    meaning: str
    """What this comes to, in the words an operator would say it in — including,
    where there is no door, that there is none.
    """
    service: typing.NotRequired[str | None]
    """The service the household begins at, by the name it shows itself under.
    Absent where this stack publishes nothing they could begin at.
    """
    standing: FrontDoorStanding
    """Where the front door stands."""


type FrontDoorStanding = typing.Literal["established", "library-only", "unreachable", "stranded", "none"]
"""Where the household's one front door stands."""


class Gone(typing.TypedDict):
    """What became of a download the client was asked to let go."""

    bytes: int
    """What it occupied, as the client reported it."""
    name: str
    """What the client is no longer holding."""
    rehearsed: bool
    """Whether this was a rehearsal, which asks the client for nothing."""


class Group(typing.TypedDict):
    """The entries of one kind, under the name an operator reads them by."""

    entries: list[Entry]
    """The changes, in the order they were made."""
    title: str
    """What this group of changes is: new, fixed, faster, or maintenance."""


class Guidance(typing.TypedDict):
    """The guidance in full, for a surface that shows all of it."""

    devices: list[Device]
    """Every device, in the order somebody is likely to be holding one."""
    nothing_is_installed: str
    """What this will not do for them."""
    only_at_home: str
    """True of every device, said once."""
    straining: typing.NotRequired[Straining | None]
    """Why playback here is likely to struggle before any app is chosen, or `None`
    where the preset in force asks for nothing this platform cannot serve.

    Absent far more often than present, and it must be: a caution shown to
    everybody says nothing about anybody's machine, and a reader who meets one
    every time stops reading it.
    """
    trouble: list[Trouble]
    """What to do when it does not work, keyed by the symptom."""


class HandoffClient(typing.TypedDict):
    """One app a device can be pointed at the stack with, and the code that points it."""

    client: str
    """What to use on it."""
    code: str
    """What the code for this app carries: a link that opens the app at this server where
    the app takes one, and the server's address otherwise.
    """
    deep_link: bool
    """Whether [`code`](Self::code) is such a link rather than the address alone."""
    device: str
    """What somebody would call the device they are holding."""
    open_source: bool
    """Whether that app is open source. A closed one is never the recommended path."""


type HandoffRemedy = typing.Literal["invite", "ask-again", "start-server", "record-address"]
"""What there is to do next about a hand-off, which each surface says in its own words.

Carried as a name rather than as a sentence because the act is the same everywhere
and the way to take it is not: a terminal names a command, and an app offers a
control. A sentence written here would have to pick one of them, and every other
surface would then be showing somebody an instruction it cannot carry out.
"""


class HandoffReport(typing.TypedDict):
    """Where one person's hand-off stands, and what to hand them.

    **The code is an address and nothing more.** Whoever holds a copy of it can find the
    server and still has to sign in as somebody, so a code sent to the wrong phone, or
    photographed over a shoulder, gives away where the server is and nothing else.
    """

    address: typing.NotRequired[str | None]
    """The address the code carries. Absent where there is no address to carry, which is
    one of the ways a hand-off fails.
    """
    caution: typing.NotRequired[str | None]
    """What is worth knowing about that address, where anything is: most often that it
    answers only on the home network.
    """
    clients: list[HandoffClient]
    """The apps to point a device at the stack with, each with its code."""
    issued: typing.NotRequired[str | None]
    """When a code was first issued for them, as an instant. Absent until one is."""
    name: str
    """Who it is for, as the media server spells their account where it holds one, and as
    it was asked for otherwise.
    """
    quick_connect: bool
    """Whether the media server offers the sign-in by short code, where one account already
    signed in approves another device.
    """
    reason: typing.NotRequired[str | None]
    """Why it stands there, where that is not the state itself: why an account that is not
    there stops it, and what stopped one that failed. In words any surface can show, so
    it names no command; what to do about it is [`remedy`](Self::remedy).
    """
    rehearsed: bool
    """Whether this was a rehearsal, in which no issue was written down."""
    remedy: typing.NotRequired[HandoffRemedy | None]
    """What there is to do next, where there is anything: named rather than said, so
    that each surface offers it in its own way.
    """
    sessions: list[HandoffSession]
    """The devices signed in to the account now, as the media server lists them."""
    state: HandoffState
    """Where it stands."""
    steps: list[str]
    """How the person signs in on the new device, one step at a time.

    Every step is something the person does on their device, in words any surface can
    show. Asking again afterwards is not one of them: that is [`remedy`](Self::remedy).

    **Guidance and never an approval.** Where the sign-in asks for a short code to be
    approved from a device they are already signed in on, that approval is theirs: it
    is the step that proves the person holding the new device is the person the
    account is for, and a program that took it for them would have proved nothing.
    """


class HandoffSession(typing.TypedDict):
    """One device the media server lists as signed in to the account."""

    client: str
    """The app it signed in with."""
    device: str
    """What the device calls itself."""
    last_seen: typing.NotRequired[str | None]
    """When the media server last heard from it, where it says."""


type HandoffState = typing.Literal["unprovisioned", "ready", "pending", "connected", "failed"]
"""Where one person's hand-off stands.

Read from the media server each time rather than remembered, apart from when a code
was first issued and which devices were signed in then: whether a device is signed in
is the server's to say, and a copy kept here would go on saying it after the person
signed out.
"""


class Handover(typing.TypedDict):
    """Where a finished walkthrough leaves the operator."""

    next: list[Next]
    """What to do next, in order."""


type Hardlink = typing.Literal["linking", "copying", "unknown"]
"""Whether imports are hardlinking or copying — the difference between an import
that is free and one that doubles the disk it uses.
"""


type HealthStanding = typing.Literal[
    "healthy", "stopped", "unconfigured", "advisory", "degraded", "broken", "critical", "unknown"
]
"""What the stack amounts to.

Ordered from best to worst, so the worst of several is a `max` and there is no
second place to encode the ranking.
"""


class HealthSummary(typing.TypedDict):
    """The one-line summary, and what it expands to."""

    affected: list[Affected]
    """Everything that is wrong, worst first, so the line expands to the affected
    items and their remedies rather than to a number nobody can act on.
    """
    standing: HealthStanding
    """The one word."""
    wanting_attention: int
    """How many things are wrong — root causes, counted once each, so a disk that
    filled and the nine imports that then failed is one thing and not ten.
    """
    worst: typing.NotRequired[str | None]
    """The worst thing, named, so the line says something rather than only
    grading. Absent where nothing is wrong.
    """


class Held(typing.TypedDict):
    """One thing the household holds, as a member is shown it.

    What a person recognises and nothing else. There is no file path, no container,
    no bitrate and no library id: a member deciding what to watch is not choosing a
    transcode, and a surface handed those would have to decide not to draw them.
    """

    id: str
    """The identifier the server tells it apart by, which is what asking to play one
    of them names.
    """
    medium: Medium
    """Which of the kinds this product deals in it is."""
    title: str
    """What it is called, in the words the server holds it under."""
    year: typing.NotRequired[int | None]
    """The year it came out, where the server knows one. Absent rather than guessed:
    two films share a title far more often than they share a title and a year.
    """


class HeldReport(typing.TypedDict):
    """What one member can watch, and who they are."""

    available: bool
    """Whether the shelf could be read at all.

    An empty shelf and an unread one are different answers, and collapsing them
    would tell a household they own nothing on the day the media server rebooted.
    Anything that could not be read is said in `findings` and this goes false.
    """
    findings: list[str]
    """What is worth saying about this shelf, in the words its reader would use.

    Always written, empty or not. A field the schema requires and the document
    sometimes omits is one a reader has to guess about, and an empty list already
    says the thing it would say: there is nothing to report about this shelf.
    """
    holdings: list[Held]
    """What they hold, newest first."""
    id: str
    """The identifier the media server files them under."""
    member: str
    """The member this was asked for, by the name they are known by."""
    rehearsed: bool
    """Whether this was a rehearsal: what would have happened, with none of it done.

    Said in a field of its own so that a rehearsal is never told from the real run by
    its wording alone.
    """


class HistoryReport(typing.TypedDict):
    """Everything lemonfiber changed, most recent first."""

    changes: list[ChangeReport]
    """The changes, newest first."""
    horizon: str
    """How far back the record goes, in the operator's terms.

    Stated rather than left to be inferred from the oldest entry: a record that has
    been trimmed and one that has always been short look identical from the entries
    alone, and only one of them means something is missing.
    """


class Holding(typing.TypedDict):
    """One download client, and what became of the limits it was given."""

    answer: Answer
    """What it said."""
    client: str
    """The client, by the name the stack knows it under."""
    pulling: typing.NotRequired[Pulling | None]
    """Whether it is fetching at all, where a declared cap made that a question.

    Absent on a stack with no cap rather than assumed to be fetching: asking
    every client whether it has stopped, on a stack where nothing would ever
    stop it, is traffic spent on a figure nothing would act on.
    """


class HostedCommand(typing.TypedDict):
    """One long-running command, and what stands between it and this machine."""

    command: str
    """How it is typed in a terminal, which is what hosting installs."""
    definition: typing.NotRequired[str | None]
    """The service definition installed for it, where there is one."""
    guarantees: str
    """What it does for as long as it runs, in one sentence."""
    missing: typing.NotRequired[str | None]
    """The program the definition names, where nothing is there any more."""
    name: str
    """lemonfiber's own name for it."""
    output: typing.NotRequired[str | None]
    """Where a hosted run writes the words it would have said on a terminal."""
    runs: typing.NotRequired[str | None]
    """The whole command line that definition runs."""
    standing: Hosting
    """What stands between it and the machine."""


type Hosting = typing.Literal[
    "not-hosted", "hosted", "installed-unverified", "stopped", "orphaned", "unsupported"
]
"""What stands between one long-running command and the machine.

Written with hyphens because these are the words the operator reads and the
requirement names, and a reading that spelled them differently would be a
second vocabulary for one set of facts.
"""


class HostingReport(typing.TypedDict):
    """What this machine keeps running on lemonfiber's behalf.

    Defaultable so a test can read one out of a `Result` without a branch it can
    never take: a closure standing in for the impossible arm is a region no
    passing run enters, and the coverage gate counts those.
    """

    caveat: typing.NotRequired[str | None]
    """What is true of this manager and worth knowing before it is relied on."""
    changed: typing.NotRequired[Changed | None]
    """What this run changed, where it was asked to change something."""
    commands: list[HostedCommand]
    """Every long-running command there is, hosted or not."""
    instruction: typing.NotRequired[str | None]
    """What to do instead, where lemonfiber cannot configure this platform."""
    manager: Manager
    """The service manager this platform has, or the absence of one."""
    rehearsed: bool
    """Whether this was a rehearsal: what would have happened, with none of it done.

    Said in a field of its own so that a rehearsal is never told from the real run by
    its wording alone.
    """


class HouseholdMember(typing.TypedDict):
    """One household member: who they are, what they may watch, when they were last
    seen, and everything they have asked for.
    """

    access: MemberAccess
    """What they may watch."""
    asking: typing.NotRequired[MemberAsking | None]
    """What they may ask for, and what their period has left of it.

    Absent where the request service holds no account for them, and where it could
    not be asked — an unread answer is not an unlimited member, and reporting one as
    the other would tell an operator their quota was never applied.
    """
    claimed: bool
    """Whether somebody has set a password on the account. False is an invitation
    nobody has taken up rather than a member who is not here.
    """
    last_seen: typing.NotRequired[str | None]
    """When the media server last saw them, as it timestamps it. Absent where nobody
    has ever signed in, which is exactly the unclaimed invitations.
    """
    name: str
    """The member, by the name their account is held under."""
    requests: list[MemberRequest]
    """What they asked for, newest first."""
    standing: MemberStanding
    """Where the account stands: an invitation still out or run out, a member who can
    sign in, or one switched off.
    """
    to_hand_over: list[str]
    """What this member would be told, in the words they would read it in.

    Everything a household member is owed at the moment of asking and cannot be
    shown where they ask: what happens to what they ask for, what their period has
    left and when it makes room, roughly what a thing costs before they choose one,
    what is still waiting on an answer, and what was refused and why. Written to
    them rather than about them, so it can be handed over as it stands.

    Empty where there is nothing to tell them — a member the request service holds
    no account for has no standing to report and nothing waiting.
    """


class HouseholdReport(typing.TypedDict):
    """Who is in the household, what each may watch, and what each has asked for."""

    allows: typing.NotRequired[str | None]
    """What that policy allows in a period, in the words a household says it in.

    Absent where nothing limits the household, which is not the same as a policy
    that could not be read: that one leaves [`Self::policy`] absent too.
    """
    available: bool
    """Whether the household could be read at all. A false here is why the list is
    empty, and keeps an unread record from being mistaken for an empty house — the
    same honesty a trace keeps about a silence it did not hear.
    """
    filtering: typing.NotRequired[str | None]
    """What the limits on this household are and are not, where anybody carries one.

    Absent on a household nobody has limited, because there is no claim to be modest
    about. Present the moment there is one, because a parent who has set a limit is
    exactly the reader who might take it for a lock.
    """
    findings: list[str]
    """What could not be read, and anything else worth the operator's attention."""
    members: list[HouseholdMember]
    """Everybody the media server holds an account for, in name order — including
    those who have never asked for anything, and the invitations nobody has taken
    up yet.
    """
    policy: typing.NotRequired[Policy | None]
    """What happens to what the household asks for where nobody chose otherwise for
    one person. Absent where the request service could not be asked.
    """
    rehearsed: bool
    """Whether this was a rehearsal: what would have happened, with none of it done.

    Said in a field of its own so that a rehearsal is never told from the real run by
    its wording alone.
    """


class ImportReport(typing.TypedDict):
    """What copying an operator's own records across came to, or would come to."""

    carried: list[RecordReport]
    """What was carried across."""
    not_carried: list[UnsupportedReport]
    """What could not be carried, and why."""
    project: typing.NotRequired[str | None]
    """The project the records were read from."""
    refusal: typing.NotRequired[str | None]
    """Why nothing was carried, where nothing was."""
    rehearsed: bool
    """Whether this was a rehearsal: what would have happened, with none of it done.

    Said in a field of its own so that a rehearsal is never told from the real run by
    its wording alone.
    """
    stance: Stance
    """Where the act stands."""
    would_carry: list[RecordReport]
    """What would be, where nothing has been yet."""


type Installed = typing.Literal[
    "homebrew", "scoop", "winget", "cargo", "distribution", "installer", "elsewhere", "image", "untellable"
]
"""How this copy of lemonfiber got onto the machine.

Nothing known is the default. Every other answer is a claim about somebody's
machine, and a value that arrived by nobody filling it in has established none of
them.
"""


class Interrupted(typing.TypedDict):
    """An import that stopped part-way, in the words of whatever stopped it."""

    name: str
    """What the service calls it."""
    partial: int
    """What is on disk for it already, where the walk could find it."""
    said: str
    """What the service said, verbatim."""


class Inventory(typing.TypedDict):
    """The whole answer to a question about credentials.

    Every ask answers with the inventory as it now stands, and adds what became of
    whatever else was asked for. An operator who has just rotated something wants to
    see the inventory that rotation produced, not a receipt they have to go and check
    against one.
    """

    held: list[CredentialHeld]
    """Every credential, whether or not it is present."""
    protection: Protection
    """What keeping them in files does and does not protect against."""
    rehearsed: bool
    """Whether this was a rehearsal: what would have happened, with none of it done.

    Said in a field of its own so that a rehearsal is never told from the real run by
    its wording alone.
    """
    revealed: typing.NotRequired[Revealed | None]
    """One value, where one was asked for."""
    rotated: typing.NotRequired[Rotation | None]
    """What became of a rotation, where one was asked for."""


class Invitation(typing.TypedDict):
    """One invitation, as it was just made.

    Carries what the operator has to pass on and nothing else — a name to sign in
    with, one address, and how long it stands. The address is the media server's,
    because setting a first password happens there.
    """

    address: str
    """The one address to send them.

    Where a *person* reaches the media server: built from what this machine is
    called on the network, not from either of the hosts the stack wires itself
    with — those resolve only on this machine or inside the stack, and an
    invitation carrying one sends somebody an address that cannot open.
    """
    applied: typing.NotRequired[InvitationApplied | None]
    """What this offer wrote on the account, where it wrote anything."""
    caution: typing.NotRequired[str | None]
    """What is worth knowing about the address itself, where anything is.

    An address that is a number is one a router can hand elsewhere, so a bookmark
    made from it stops working with nothing here having changed. Carried on the
    invitation because that is the copy somebody keeps.
    """
    decline: typing.NotRequired[str | None]
    """Where they can decline it instead, where the stack runs the decline service.

    A page on the household's own network that refuses this invitation and nothing
    else, and switches the account made for it off. Its token is in this address
    alone: offering the same person again mints a new one, and the old address stops
    declining anything. Absent on a rehearsal, for somebody already in the household,
    and where the stack runs no decline service.
    """
    hours: int
    """How many hours it stands before it is withdrawn.

    Counted from when it was *offered*, which for an account whose password was
    taken off is the moment of the reset rather than when the account was made.
    What happens at the end depends on the account: one nobody has been in is
    removed, and one somebody has is switched off and kept.
    """
    linked: Linked
    """Whether the request service knows about the household yet.

    Separate from `standing`, which is about the media-server account alone. The
    two can disagree — an account made while the request service was unreachable
    is `Made` and `NotYet` — and that disagreement is the state this reports.
    """
    name: str
    """The name they sign in as."""
    rehearsed: bool
    """Whether the account was made, or only described.

    A rehearsal can say the whole answer without writing any of it — the name is
    the one asked for, the address is the stack's, and what has run out has just
    been read — so the only thing separating it from the real run is this.
    """
    standing: InvitationStanding
    """What was found where this was going."""
    suspended: list[str]
    """Accounts somebody had been in, reset and not claimed again in time, switched off
    on the way past rather than removed.

    Kept because removing one takes what they watched with it. Switched off because
    an account with no password that anybody may still claim is the thing a window
    exists to close. Offering it again, or reissuing it, switches it back on. On a
    rehearsal these are the ones that *would* be switched off.
    """
    withdrawn: list[str]
    """Invitations nobody claimed in time, removed on the way past.

    Reported rather than done quietly: an operator who invited somebody last
    week and hears nothing would otherwise have no way to learn the account is
    gone. On a rehearsal these are the ones that *would* be removed.
    """


class InvitationApplied(typing.TypedDict):
    """What an invitation wrote on the account, in the household's own words.

    **Said back so an absence later is explicable.** A member held to a rating who
    cannot find half the library is either this working or a defect, and an operator
    with nothing on record cannot tell which. So the limit, the libraries, what happened
    to content the media server has no rating for, and whether the request service was
    held to the same decision all travel back on the answer that applied them.

    Absent where the offer set nothing at all, which is not the same as an offer that
    set no restrictions: naming neither a library nor a limit is saying nothing about
    access, and nothing is what gets written.

    Serialised in the field names the household read uses for the same facts, rather
    than in the invitation's own spelling: one setting named two ways across two shapes
    is two shapes a client has to be told are about the same thing.
    """

    filtering: str
    """What a limit here is, and what it is not.

    Carried on the answer rather than left to a document, because the reader who
    most needs it is the parent who has just set one.
    """
    libraries: list[str]
    """The libraries they may open, as the operator named them. Empty is every one."""
    limit: typing.NotRequired[str | None]
    """How far up the ratings they may watch, in the words and the certificates this
    media server names in the operator's own country. Absent where no limit was set.
    """
    requesting: Linked
    """Whether the request service was held to the same decision.

    The same three answers a link carries, and for the same reason: what somebody
    may *ask for* is a second service's business, and that service can be down while
    the media server is not. `NotTried` here is a service with no account for them
    yet — nothing to hold rather than a failure to hold something.
    """
    unrated: Unrated
    """What becomes of content the media server has no rating for.

    Held back by default on somebody being narrowed, because a rating limit cannot
    decide about a thing that carries no rating. The cost is real and is why this is
    reported rather than assumed: some legitimate content becomes invisible to them.
    """


type InvitationStanding = typing.Literal["made", "waiting", "joined", "reset"]
"""What was found where the invitation was going.

Offering somebody an account twice is a thing operators do — they forget, or the
first message went unanswered — and it is not a mistake to be refused. Each of
these is an answer, and which one it is decides what there is to say rather than
whether anything worked.
"""


class Item(typing.TypedDict):
    """One thing a removal reaches, said to be going or said to be kept."""

    bytes: typing.NotRequired[int | None]
    """What it occupies, where that is knowable. Absent for a container or a network,
    whose room is the image's rather than their own.
    """
    kept: typing.NotRequired[str | None]
    """Why it is being kept rather than removed, where it is being kept.

    `None` is the ordinary case: this line is going. A reason here is the whole of
    how an image shared with another project, or a path this run could not
    confirm, stays on the list without being taken.
    """
    name: str
    """What it is called — a container name, an image reference, or a full path."""
    secret: bool
    """Whether it holds a credential, so a report can say what destroying it destroys."""
    sort: Sort
    """Which of the four sorts of thing it is."""
    what: str
    """What it is, in the operator's words."""


type Jump = typing.Literal["major", "minor", "patch", "untellable"]
"""How large a step from one version to another is.

Named after the part of the version that moved rather than after a size, because
that is the fact an operator weighs: a first-number change is where a project puts
the work that breaks configurations, and the two behind it are where it puts the
work that does not.
"""


class Kept(typing.TypedDict):
    """One thing lemonfiber keeps on this machine."""

    at: str
    """Where it is, in full."""
    secret: bool
    """Whether it holds a credential, which is what decides how carefully a copy of
    it has to be treated.
    """
    what: str
    """What it is, in the operator's words."""
    why: str
    """Why it is kept."""


class KeyListing(typing.TypedDict):
    """Every key this machine has minted, and what became of a revoke."""

    keys: list[ListedKey]
    """In the order they were minted."""
    purposes: str
    """What a purpose in the listing is worth, said with it."""
    rehearsed: bool
    """Whether this was a rehearsal: what revoking would come to, with nothing revoked."""
    revoked: typing.NotRequired[str | None]
    """The key this run revoked, where it revoked one."""


type KeyPurpose = typing.Literal["home-assistant", "mcp", "other"]
"""What the minter said a key is for.

A label and nothing more. The core cannot tell what a program does with a key, so the
listing shows this as the minter's own declaration rather than as anything verified.
"""


type KeySource = typing.Literal[
    "config-xml", "config-ini", "config-json", "config-yaml", "api-settings", "generated", "none"
]
"""Where a service's credential comes from."""


type KeyState = typing.Literal["active", "revoked", "orphaned", "unconfirmed"]
"""Where a key stands."""


class Leaving(typing.TypedDict):
    """Everything that leaves this machine: lemonfiber's own requests, and the stack's."""

    ours: list[Outbound]
    """Every request lemonfiber makes on its own account, in a fixed order."""
    theirs: list[Elsewhere]
    """The requests made by services this stack runs, attributed to them."""


class Letting(typing.TypedDict):
    """One completed download, what letting it go would cost, and what became of it."""

    agreement: str
    """What this offer names itself, so an answer to it can say which offer it
    answered.
    """
    download: Candidate
    """The download, in the same words the account names it in: where it stands, what
    it occupies, and what removing it costs.
    """
    goes: str
    """What goes with it, carried rather than left for a surface to remember."""
    gone: typing.NotRequired[Gone | None]
    """What became of an answered offer, and nothing where the offer is all this is."""
    rehearsed: bool
    """Whether this was a rehearsal: what would have happened, with none of it done.

    Said in a field of its own so that a rehearsal is never told from the real run by
    its wording alone.
    """


type Level = typing.Literal["unknown", "ample", "advisory", "warning", "critical", "exhausted"]
"""Where a volume stands."""


class LibraryPath(typing.TypedDict):
    """One library path a service files into, and what moving the data location does
    to it.
    """

    because: str
    """Why it does or does not, in the operator's terms."""
    carried: bool
    """Whether the library at this path survives the move."""
    host: typing.NotRequired[str | None]
    """The host directory it would resolve to after the move, where the move can
    resolve it at all.
    """
    path: str
    """The path as that service holds it, which is a path inside its container."""
    service: str
    """The service holding it."""


class LifecycleReport(typing.TypedDict):
    """What a lifecycle command did, or would have done."""

    action: str
    """The Compose subcommand that was run."""
    command: list[str]
    """The exact command, so what happened is never a matter of trust."""
    condition: typing.NotRequired[Condition | None]
    """What those services amount to, as one word."""
    forwarding: typing.NotRequired[str | None]
    """What starting the stack did about the VPN's forwarded port, where it did
    anything. Absent in the ordinary case — the client was already on it, or
    there is no tunnel to forward through — and a sentence where the client was
    moved, or could not be.
    """
    held: typing.NotRequired[str | None]
    """Why nothing was run, where a start declined to run anything.

    Absent for every ordinary command, which is what makes it readable: a
    lifecycle report with an empty plan and a status of nothing is a report of
    something that did not happen, and without this there is nowhere to say
    whether that was a fault or the correct answer. A start at a login declines
    for three reasons the operator would each act on differently — the stack was
    stopped on purpose, autostart was never asked for, or this machine is on its
    battery and nobody said to start anyway — and a run nobody is watching has to
    leave the reason somewhere a reader finds later.
    """
    plan: Plan
    """What the named forms came to: the profiles, the services they hold, and
    what the configuration left out.

    The resolved plan itself rather than a copy of its parts, because it is
    stated to the operator before the command runs and read out of the
    report afterwards — two accounts of one run, and a second shape for it
    would be a way for them to differ.
    """
    port_conflicts: typing.NotRequired[list[ConflictReport]]
    """Host ports this start wants that another Compose project on this machine
    already answers on, each named on both sides.

    Empty for every action that starts nothing, and empty on a machine running one
    stack. Reported rather than refused: a port somebody deliberately shares is
    their business, and the start goes ahead — what this changes is whether an
    operator meeting a bind failure knows who is holding the port.
    """
    rehearsed: bool
    """Whether this was a rehearsal."""
    services: list[Service]
    """What each service ended up doing, where the action waited to find out, or
    where a start did not complete, read once when it ended.

    Empty for actions that do not wait. Stopping is finished when Compose
    says it is, and surveying afterwards would only report the absence it
    was asked to produce. A start that failed is not waited on, and names every
    service it addressed and those they depend on as the engine had them then.
    """
    stack_edits: list[StackEdit]
    """Stack files the operator has edited, left as they set them rather than
    overwritten with lemonfiber's own. Empty in the ordinary case; a named entry
    warns that an upgrade would change a file they changed, and shows the diff.
    """
    status: typing.NotRequired[int | None]
    """The exit status, absent for a rehearsal or a signalled process."""
    switched: typing.NotRequired[Switched | None]
    """What narrowing moved, where the command was a switch. Absent for every
    other action, which is what tells a reader that nothing was left running
    on purpose.
    """


type Limit = LimitUnlimited | LimitShare | LimitAbsolute
"""How much of the line something may take."""


class Line(typing.TypedDict):
    """One narrated line: a step, and what was specifically true of it."""

    detail: str
    """What was specifically true — the evidence that makes the line worth reading
    rather than a spinner. Empty where there is nothing particular to say.
    """
    said: str
    """What it is doing, in plain language."""
    step: WalkthroughStep
    """The step being narrated."""


type Link = typing.Literal["hardlinked", "copied"]
"""What the import did with the finished download — the difference between one copy of a
file and two.
"""


type Linked = typing.Literal["made", "not-yet", "not-tried"]
"""Whether the request service has been given an account for the household yet.

The account somebody watches with is made on the media server, and it stands on its
own from that moment — nothing has to be running for them to claim it. Being able
to *ask* for something is a second account, on a second service, and that service
can be down while the first is not.

So this is reported rather than made a condition of the invitation: an operator who
invites somebody during an outage has still invited them, and what they cannot do
yet is worth one line rather than a refusal.
"""


class LinkingReport(typing.TypedDict):
    """What an existing layout costs, where it cannot hold a hardlink."""

    because: str
    """Why they cannot, naming the filesystems it is about."""
    cost: str
    """What that costs, in room rather than in adjectives."""
    filesystems: list[str]
    """The filesystems the existing setup keeps its data on."""
    forced: bool
    """Whether lemonfiber will do it. Always false: the layout and the library in it
    are the operator's, and correctness does not outrank their data.
    """
    links: bool
    """Whether imports can be hardlinks across this layout. False whenever this is
    reported at all, since a layout that links is not reported.
    """
    remedy: str
    """What would fix it, offered."""


class ListedKey(typing.TypedDict):
    """One key as the listing shows it, without its secret."""

    member_minted: bool
    """Whether a household member minted it for themselves."""
    minted: str
    """When it was minted."""
    name: str
    """The name it was minted under."""
    purpose: KeyPurpose
    """What the minter said it is for. A declaration, not something the core verified."""
    revoked: typing.NotRequired[str | None]
    """When it was revoked, where it has been."""
    scope: str
    """What it admits: `read`, `act` or `member:<name>`."""
    state: KeyState
    """Where it stands."""
    used: typing.NotRequired[str | None]
    """When it was last admitted, where it has been."""


class Listing(typing.TypedDict):
    """The archives this machine has kept."""

    archives: list[str]
    """Each one by the name it was written under, newest first.

    The name is the whole of what another surface needs: it is what a restore
    asks for, and it carries the moment the archive was taken and what it
    covers, because that is how a capture names one.
    """


type LogLevel = typing.Literal["trace", "debug", "info", "warn", "error", "fatal"]
"""How bad a line says it is.

Ordered, so a filter can ask for \"warnings and worse\" without a table of which
level outranks which. Deliberately coarse: these six are what services agree
on, and a seventh that only one of them writes would be a level nobody could filter
by across the stack.
"""


class LogLine(typing.TypedDict):
    """One line of output from one service, and how bad it says it is.

    What a machine-readable surface hands on, rather than the engine's line alone, so
    a consumer can mark the lines that say they failed, or find the first of them,
    without reading the text for itself — a second reading of severity would be a
    second answer, and the two would disagree about some service's spelling.
    """

    at: typing.NotRequired[str | None]
    """When the container itself says it wrote the line, where it said so.

    Kept verbatim and unparsed. Containers disagree with the host clock and
    with each other, and the only defensible ordering is each container's own
    account of itself — which a reader can only apply if it is carried
    rather than replaced by an arrival time.
    """
    level: typing.NotRequired[LogLevel | None]
    """How bad the line says it is, in one lowercase word.

    Absent where the line says nothing about itself. It is never guessed from
    the stream the line arrived on or from the words in it: most of this stack
    writes ordinary progress to standard error, and a line saying it could not
    find something is often a routine miss.
    """
    line: str
    """The line, without its trailing newline."""
    service: str
    """The Compose service it came from."""
    stream: Stream
    """Which stream it arrived on."""


type Manager = typing.Literal["launchd", "systemd", "unsupported"]
"""The service manager a machine has, or the absence of one lemonfiber configures.

The absence is the default, because a machine nobody has told is a machine
nothing is known about, and guessing at a manager is how a report comes to
claim a platform it never asked.
"""


type Medium = typing.Literal["film", "series", "other"]
"""The kinds of thing a household holds.

Named rather than passed through as the server's own word, because a surface
drawing \"Series\" against one server and \"tvshow\" against another would be
rendering a detail of which server this household runs.

`Medium` rather than `Kind`, `Holding` or `Sort`: this product already calls the two
request services a [`crate::media::Kind`], a request's suspension a
[`crate::service::asking::Holding`], and what one line of a manifest is a
`uninstall::Sort` — and one word meaning two things in one vocabulary is how a
reader comes to trust the wrong one. The contract flattens every type name into one
namespace, so a clash there is a clash for anything reading it by name.
"""


class Member(typing.TypedDict):
    """One entry in an archive's contents listing."""

    archive_path: str
    """Where it sits inside the archive."""
    label: str
    """What it is, in the operator's terms."""


class MemberAccess(typing.TypedDict):
    """What one member may watch, in the household's own words.

    Read off the media server's account rather than kept here: that is where access is
    decided, and a second copy is a copy able to disagree.
    """

    administrator: bool
    """Whether the account administers the media server."""
    age_limit: typing.NotRequired[int | None]
    """The highest rating they may watch, where the operator set a limit."""
    disabled: bool
    """Whether the account is switched off — held, but unable to sign in."""
    every_library: bool
    """Every library, rather than a chosen few. The ordinary case."""
    libraries: list[str]
    """The libraries they may watch where it is not every one, by the names the
    operator gave them — or by the server's identifiers where the library list
    could not be read, which a finding says.
    """
    rated: typing.NotRequired[Rated | None]
    """What that limit comes to in the certificates this media server names, in the
    operator's own country. Absent where no limit is set.
    """
    restriction: Restriction
    """What they are held to, in one word — including where what they may watch and
    what they may ask for disagree.
    """
    unrated: Unrated
    """What becomes of content the media server has no rating for.

    Said either way, because an unexplained absence is the thing this answers: a
    restricted member missing half the library is either this setting or a defect,
    and an operator cannot tell which from silence.
    """


class MemberAsking(typing.TypedDict):
    """What one member may ask for, where the request service could be asked.

    Both counts, because the service keeps them apart and folding them would report a
    household as within its limit while the half that matters is spent: television is
    counted a season at a time, so one ask for a six-season series spends six.
    """

    films: Counted
    """Films, counted one to a request."""
    frees_up: typing.NotRequired[str | None]
    """When the count next lets go of something, so one more becomes possible.

    Absent where nothing limits them, and where the request service's own dates
    could not be read — an invented one would be a promise about a day on which
    nothing happens. The period is a window that rolls rather than a month that
    ends, so this is the moment their earliest counted request ages out.
    """
    policy: Policy
    """What happens to what they ask for."""
    standing: AskingStanding
    """Where they stand against what their period allows, taken over both counts."""
    television: Counted
    """Television, counted one to a season."""


class MemberRequest(typing.TypedDict):
    """One thing a household member asked for, and where it stands in their words."""

    estimate: typing.NotRequired[Estimate | None]
    """About how much room it will want, at the quality in force.

    A guess and labelled as one — see [`crate::asking::Estimate`]. Absent where the
    request service names a kind this build does not know, since there is nothing to
    guess the length of.
    """
    id: int
    """The number the request service files it under, which is how one is named again
    when somebody rules on it.
    """
    media: typing.NotRequired[str | None]
    """What kind of thing it is — a series, a film — in the household's own words.
    Absent where the request service names a kind this build does not know.
    """
    refused: typing.NotRequired[Refused | None]
    """Why it was turned down, where it was turned down from here.

    **The request service keeps none**, so this is lemonfiber's own record and is
    said to be — a reason presented as delivered would end the operator's job at
    exactly the point it begins. Absent on a request nobody has refused, and on one
    refused in the request service itself, where there are no words to report and
    inventing some would put them in somebody's mouth.

    Whether the words were carried to the person who asked is the record's own
    `told`, which is why the two travel together: what an operator does next turns
    on it, and a reason read without it is a reason of unknown standing.
    """
    state: typing.NotRequired[RequestState | None]
    """Where the request stands, or absent where the request service reports a status
    this build does not know rather than guessing it into the nearest word.
    """
    title: typing.NotRequired[str | None]
    """What it is called, where the service filing it has been told about it and its
    library could be read. Absent for a request no service holds yet — one still
    awaiting approval has been handed to nobody, so there is no title to find.
    """
    waiting_days: typing.NotRequired[int | None]
    """How many whole days it has been waiting on somebody, where it is waiting at all
    and the service's own date could be read.

    Only on the ones nobody has ruled on. A request already answered has not been
    waiting since it was made, and a figure beside one would be counting the wrong
    thing.
    """


type MemberStanding = typing.Literal["invited", "expired", "declined", "active", "suspended"]
"""Where one member's account stands.

**Switched off is its own answer rather than a flag beside another.** An account the
media server switched off after too many wrong passwords reads, on every other field,
exactly like one that works — and the person holding it has only been told their
password is wrong. What unlocks it is a reissue, which is the operator's to do, so the
operator is the one who has to be able to see it.
"""


class Mended(typing.TypedDict):
    """One repair, and what became of it."""

    outcome: RepairOutcome
    """How it turned out, once the check was asked again."""
    repair: Repair
    """What was proposed."""


class Metered(typing.TypedDict):
    """What the stack itself moved in a calendar month, and what that leaves out."""

    down: int
    """Bytes pulled down, as far as the clients count them."""
    excludes: str
    """What this count does not include, always said."""
    incomplete: list[str]
    """What is known to be missing from the count itself, where anything is."""
    month: str
    """The month, as the client that dated the figures dates them."""
    up: int
    """Bytes given back."""


class MigrationReport(typing.TypedDict):
    """What is already on this machine, before anything is proposed."""

    beside: list[MovedReport]
    """Where each service would listen to run beside the existing setup."""
    carrying: list[CarryingReport]
    """What adopting each recognised service would come to, by service name."""
    conflicts: list[ConflictReport]
    """Ports wanted by lemonfiber that an existing service already holds."""
    linking: typing.NotRequired[LinkingReport | None]
    """What the existing layout costs where it cannot hold a hardlink, absent where
    it can.
    """
    modes: list[ModeReport]
    """What may be done about what was found, least destructive first."""
    not_carried: list[UnsupportedReport]
    """What no migration carries across, whatever mode it runs in."""
    read: bool
    """Whether the engine answered at all.

    False means the survey found nothing because it could not look, which is a
    different answer from finding nothing, and the only one that must never be
    read as an empty machine.
    """
    standing: list[StandingReport]
    """Existing projects, by project name."""
    unsupported: list[UnsupportedReport]
    """What was found and cannot be adopted."""


class MintedKey(typing.TypedDict):
    """A key minted, with everything a client on another machine needs to use it.

    The only document that ever carries the secret. Every surface that renders it does so
    once, and nothing here writes it down.
    """

    address: typing.NotRequired[str | None]
    """Where a client on another machine reaches the stack: the `https` address it was
    last served at on the network. Absent where it has never been served that way.
    """
    caution: typing.NotRequired[str | None]
    """What is worth knowing before handing the key over, where anything is: how to
    serve the stack so another machine can reach it.
    """
    name: str
    """The name it was minted under."""
    pin: typing.NotRequired[str | None]
    """The certificate that address presents: SHA-256 over its DER encoding, in
    lower-case hex. A client off this machine pins it.
    """
    purpose: KeyPurpose
    """What the minter said it is for."""
    scope: str
    """What it admits: `read`, `act` or `member:<name>`."""
    secret: Secret
    """The secret, sent in `X-Lemonfiber-Token`. It is not shown again."""


class ModeReport(typing.TypedDict):
    """One thing an operator may do about a setup already here."""

    disturbs: bool
    """Whether carrying it out stops or alters what is already running."""
    mode: str
    """The word an operator types for it."""
    preselected: bool
    """Whether it is offered already chosen. Only adopting is."""
    what: str
    """What choosing it would come to, in the operator's terms."""


type Moment = typing.Literal["onset", "resolved"]
"""Which way a condition went.

Both directions are worth saying and neither is worth saying twice. An operator
told a disk filled up and never told it was resolved goes on believing it — so
resolution is an alert in its own right rather than the absence of one.
"""


class MusicChoice(typing.TypedDict):
    """One audio-format choice in force, for media that has no resolution — the same
    question as a [`PresetChoice`], answered in format terms rather than resolution.
    """

    format: str
    """The format's plain-language name."""
    means: str
    """What it means, in the operator's terms."""
    note: str
    """The practical caveat worth knowing — playing it, or finding it."""
    scope: str
    """What this applies to — `music`."""
    size_per_hour: str
    """Roughly how much disk an hour of it takes."""
    targets: str
    """The audio format it targets, in plain terms."""


class MusicReport(typing.TypedDict):
    """What choosing an audio format for music did: the choice, whether it was recorded
    or only rehearsed, and — once recorded — what became of applying it to the music
    service.

    Music has no resolution and no community profile to lean on, so unlike a resolution
    preset the choice is carried straight to the service through its API. The choice is
    still recorded first, so it is remembered even when the service cannot be reached.
    """

    choice: MusicChoice
    """The format chosen, what it means, and what it costs."""
    disposition: Disposition
    """Whether the choice was recorded, or only rehearsed."""
    outcome: typing.NotRequired[Triggered | None]
    """What became of applying it to the music service, or `None` for a rehearsal
    that applied nothing.
    """
    rehearsed: bool
    """Whether this was a rehearsal: what would have happened, with none of it done.

    Said in a field of its own so that a rehearsal is never told from the real run by
    its wording alone.
    """


class Newest(typing.TypedDict):
    """The newest of each kind, by what names them and nothing else.

    What the event stream says. A surface marks a tab from it without reading the
    items, and reads [`News`] on the screen that lists them.
    """

    problems: list[NewsCheck]
    """The checks most recently found wrong, each with its onset."""
    requests: list[int]
    """The numbers of the household's newest requests."""
    unread: list[NewsKind]
    """The kinds that could not be read, as [`News::unread`] names them."""
    updates: list[str]
    """The versions of the newest releases in the record this build carries."""


class News(typing.TypedDict):
    """What a surface can mark as new, newest first within each kind."""

    problems: list[NewsProblem]
    """The checks found wrong, the most recent onset first."""
    requests: list[NewsRequest]
    """What the household has asked for, highest number first."""
    unread: list[NewsKind]
    """The kinds that could not be read.

    A kind named here has an empty list because nothing could be read, not because
    nothing is there. A surface that took the empty list as everything there is
    would mark all of it as new once it could be read again.
    """
    updates: list[NewsUpdate]
    """The releases in the record this build carries, newest first."""


class NewsCheck(typing.TypedDict):
    """A check found wrong, by the check and when it went wrong."""

    check: str
    """The check that raised it."""
    onset: str
    """When the stack first saw it wrong since it last saw it right, in whole seconds
    since the epoch.
    """


type NewsKind = typing.Literal["updates", "requests", "problems"]
"""One of the three kinds of thing a surface can mark as new."""


class NewsProblem(typing.TypedDict):
    """One check found wrong, by the check and when it went wrong."""

    check: str
    """The check that raised it."""
    onset: str
    """When the stack first saw it wrong since it last saw it right, in whole seconds
    since the epoch: the same moment the health summary names for it.
    """
    summary: str
    """What is wrong, in one line."""


class NewsRequest(typing.TypedDict):
    """One request, by its number."""

    by: str
    """Who asked for it, by the name the media server holds them under."""
    number: int
    """The number the request service files it under."""
    title: typing.NotRequired[str | None]
    """What it is called, where a service has been told about it."""


class NewsUpdate(typing.TypedDict):
    """One release, by its version."""

    delivers: typing.NotRequired[str | None]
    """What it set out to deliver, where the record says."""
    version: str
    """The version, without the tag's leading letter."""


type Next = typing.Literal["more-content", "household", "client-apps"]
"""One thing to do next."""


class Notes(typing.TypedDict):
    """What a surface shows about the record, given the version asking."""

    releases: list[ReleaseSummary]
    """Every release the record holds, newest first."""
    requirements: dict[str, Requirement]
    """What each requirement the running release cites is, and where it is defined."""
    running: typing.NotRequired[Release | None]
    """What the running version changed, where the record holds its release."""
    state: ChangelogState
    """Whether the record describes what this build could have shipped."""


class OccupantReport(typing.TypedDict):
    """One container of somebody else's stack, as the engine reports it."""

    adoptable: bool
    """Whether lemonfiber knows this service and could take it over as it stands."""
    ports: list[int]
    """Every host port it publishes, lowest first."""
    running: bool
    """Whether it is running now, as against present but stopped."""
    service: str
    """The Compose service name it answers to."""


class Opening(typing.TypedDict):
    """One thing a way of downloading newly asks the operator for.

    What is opened and nothing beside it: an operator adding Usenet is shown the
    Usenet provider and the settings its login is kept in, and never the tunnel,
    which they neither need nor asked about.
    """

    because: str
    """Why this protocol needs it."""
    setting: typing.NotRequired[str | None]
    """The setting its answer is kept in, where it is kept in one. Absent for an
    account the operator has to go and obtain, which no setting holds.
    """
    what: str
    """What it is, in the operator's terms."""


type Origin = typing.Literal["operator", "service", "lemonfiber"]
"""Who produced a credential, which decides what can be done about it."""


class Outbound(typing.TypedDict):
    """One request lemonfiber makes, where it goes, and what refusing it costs."""

    allowed: bool
    """Whether this machine's settings allow it."""
    cost: str
    """What stops working once it is off."""
    destination: list[str]
    """Where it goes as this machine is configured. Empty where nothing is
    configured to reach, which is not the same as switched off.
    """
    purpose: str
    """Why lemonfiber asks."""
    reach: OutboundReach
    """Which request this is."""
    sends: str
    """Exactly what travels in the request."""
    switch: str
    """The setting that switches it off."""


type OutboundReach = typing.Literal[
    "registry", "guides", "echo", "indexer", "usenet", "household", "updates", "plugin-source", "catalogue"
]
"""One of the requests lemonfiber makes on its own account.

Nine, and the closed set is the claim. A tenth is a decision somebody makes by
adding a variant here and answering four questions about it, rather than one
that happens by somebody building a request.

The sixth is the one that carries somebody's words rather than a credential or a
name, and it was added deliberately and late: five of these prove or fetch
something and could say what travels in a phrase, and this one travels to a
person. What that costs is the same four answers as the rest, and one more thing
the others do not owe — it is the only entry whose destination is somebody else's
choice, so the list names the two services it can reach and the sender is handed
them rather than holding addresses of its own.

The seventh is the only one this program makes about *itself*, and the one most easily
left off a list of what this program reaches. What it costs to allow is the shortest
answer on the list: it carries nothing at all, so the only thing switching it off
keeps from anybody is the knowledge that a version came out.

The eighth goes where the operator points it and nowhere else: a plugin's git
source, named at install. It is the only entry whose destination nobody chose in
advance, which is why it is made only when somebody names one.

The ninth goes to one place this build names, and only when an operator installs a
plugin by name: the catalogue's newest release, for its index and the signature over
it.
"""


class Outside(typing.TypedDict):
    """Something an uninstall leaves behind, and how to remove it by hand."""

    by_hand: str
    """How to remove it on this platform, as the operator would type or do it."""
    found: bool
    """Whether this machine was found to have it.

    A survey that could not look says nothing was found rather than that nothing
    is there, which is why the entry is listed either way and this field carries
    the difference.
    """
    what: str
    """What it is."""
    why: str
    """Why it is not lemonfiber's to take away."""


class Outsized(typing.TypedDict):
    """One file far larger than the rest."""

    bytes: int
    """What it occupies."""
    path: str
    """Where it is."""
    times_typical: int
    """How many times the middle file of this walk it is."""


type Overall = typing.Literal["healthy", "degraded", "broken", "unknown"]
"""What a run's findings amount to."""


class Pace(typing.TypedDict):
    """What a capture came to, against the time a capture is meant to take.

    Reported and never enforced. The room check already walks the trees to decide
    whether the archive fits, so the bytes are in hand before anything is written and
    cost nothing extra to say — and what they are measured against is the work, not a
    clock. A wall-clock gate on a machine whose disk throughput varies by more than the
    margin either passes for reasons unrelated to this product or fails for them, and
    neither reading is worth having.
    """

    brisk: bool
    """Whether this capture is inside it."""
    budget: int
    """The bytes a capture may move and still be expected to finish in time.

    Carried with the reading rather than left for a reader to look up, so a surface
    showing this does not need a second copy of the number to compare against.
    """
    moved: int
    """The bytes the captured trees came to, as the room check measured them."""


class Pairing(typing.TypedDict):
    """Pairing material, and what the operator is told beside it."""

    caution: typing.NotRequired[str | None]
    """What is worth knowing about the address itself, where anything is."""
    compare: str
    """The fingerprint in the short form a person compares with what the phone shows
    after typing the line in, as [`comparable`] derives it.
    """
    material: PairingMaterial
    """The material itself."""
    replacing: str
    """What would make every paired phone refuse this machine, said now rather than
    discovered then. In words any surface can show: how the certificate is replaced
    is each surface's own to say, so this names no command.
    """
    until: str
    """When it stops being good, as a date and a time of day."""
    written: str
    """The material as the one line a code carries and a person types."""


class PairingMaterial(typing.TypedDict):
    """What a phone is handed, exactly as it reads it.

    Four fields and no more: a reader refuses one it does not know, which is what keeps a
    credential from ever riding along under a name nobody thought to forbid.
    """

    address: str
    """Where the phone reaches the stack: an `https` address on the household network."""
    expires: int
    """When the material stops being good, in seconds since the Unix epoch."""
    fingerprint: str
    """The certificate that address presents: SHA-256 over its DER encoding, in
    lower-case hex. Not the digest of its public key.
    """
    stack: str
    """The stack's own identifier: opaque, minted once from nothing and kept, and the
    same across every issue of the material, a change of address and a replacement of
    the certificate. Not the stack's name and not its version, and it carries nothing
    about the household or anybody in it.
    """


type PanelArray_of_Queue = PanelArray_of_QueueReady | PanelArray_of_QueueUnavailable
"""A panel's content, or the reason its source could not fill it.

The difference between \"this panel is up to date\" and \"this panel's source is
unreachable\" is the whole of degrading honestly: an unavailable panel says so,
in its own words, rather than showing stale data as current or blank data as
zero — and the panels beside it stay live.
"""


class PanelArray_of_QueueReady(typing.TypedDict):
    """The source answered; here is the panel."""

    data: list[Queue]
    panel: typing.Literal["ready"]


class PanelArray_of_QueueUnavailable(typing.TypedDict):
    """The source could not be reached, for this stated reason."""

    data: PanelArray_of_QueueUnavailableData
    panel: typing.Literal["unavailable"]


class PanelArray_of_QueueUnavailableData(typing.TypedDict):
    reason: str
    """Why the panel could not be filled, in the operator's terms."""


type PanelArray_of_Service = PanelArray_of_ServiceReady | PanelArray_of_ServiceUnavailable
"""A panel's content, or the reason its source could not fill it.

The difference between \"this panel is up to date\" and \"this panel's source is
unreachable\" is the whole of degrading honestly: an unavailable panel says so,
in its own words, rather than showing stale data as current or blank data as
zero — and the panels beside it stay live.
"""


class PanelArray_of_ServiceReady(typing.TypedDict):
    """The source answered; here is the panel."""

    data: list[Service]
    panel: typing.Literal["ready"]


class PanelArray_of_ServiceUnavailable(typing.TypedDict):
    """The source could not be reached, for this stated reason."""

    data: PanelArray_of_ServiceUnavailableData
    panel: typing.Literal["unavailable"]


class PanelArray_of_ServiceUnavailableData(typing.TypedDict):
    reason: str
    """Why the panel could not be filled, in the operator's terms."""


type PanelArray_of_Transfer = PanelArray_of_TransferReady | PanelArray_of_TransferUnavailable
"""A panel's content, or the reason its source could not fill it.

The difference between \"this panel is up to date\" and \"this panel's source is
unreachable\" is the whole of degrading honestly: an unavailable panel says so,
in its own words, rather than showing stale data as current or blank data as
zero — and the panels beside it stay live.
"""


class PanelArray_of_TransferReady(typing.TypedDict):
    """The source answered; here is the panel."""

    data: list[Transfer]
    panel: typing.Literal["ready"]


class PanelArray_of_TransferUnavailable(typing.TypedDict):
    """The source could not be reached, for this stated reason."""

    data: PanelArray_of_TransferUnavailableData
    panel: typing.Literal["unavailable"]


class PanelArray_of_TransferUnavailableData(typing.TypedDict):
    reason: str
    """Why the panel could not be filled, in the operator's terms."""


type PanelFrontDoorReport = PanelFrontDoorReportReady | PanelFrontDoorReportUnavailable
"""A panel's content, or the reason its source could not fill it.

The difference between \"this panel is up to date\" and \"this panel's source is
unreachable\" is the whole of degrading honestly: an unavailable panel says so,
in its own words, rather than showing stale data as current or blank data as
zero — and the panels beside it stay live.
"""


class PanelFrontDoorReportReady(typing.TypedDict):
    """The source answered; here is the panel."""

    data: FrontDoorReport
    panel: typing.Literal["ready"]


class PanelFrontDoorReportUnavailable(typing.TypedDict):
    """The source could not be reached, for this stated reason."""

    data: PanelFrontDoorReportUnavailableData
    panel: typing.Literal["unavailable"]


class PanelFrontDoorReportUnavailableData(typing.TypedDict):
    reason: str
    """Why the panel could not be filled, in the operator's terms."""


type PanelHouseholdReport = PanelHouseholdReportReady | PanelHouseholdReportUnavailable
"""A panel's content, or the reason its source could not fill it.

The difference between \"this panel is up to date\" and \"this panel's source is
unreachable\" is the whole of degrading honestly: an unavailable panel says so,
in its own words, rather than showing stale data as current or blank data as
zero — and the panels beside it stay live.
"""


class PanelHouseholdReportReady(typing.TypedDict):
    """The source answered; here is the panel."""

    data: HouseholdReport
    panel: typing.Literal["ready"]


class PanelHouseholdReportUnavailable(typing.TypedDict):
    """The source could not be reached, for this stated reason."""

    data: PanelHouseholdReportUnavailableData
    panel: typing.Literal["unavailable"]


class PanelHouseholdReportUnavailableData(typing.TypedDict):
    reason: str
    """Why the panel could not be filled, in the operator's terms."""


type PanelStorage = PanelStorageReady | PanelStorageUnavailable
"""A panel's content, or the reason its source could not fill it.

The difference between \"this panel is up to date\" and \"this panel's source is
unreachable\" is the whole of degrading honestly: an unavailable panel says so,
in its own words, rather than showing stale data as current or blank data as
zero — and the panels beside it stay live.
"""


class PanelStorageReady(typing.TypedDict):
    """The source answered; here is the panel."""

    data: Storage
    panel: typing.Literal["ready"]


class PanelStorageUnavailable(typing.TypedDict):
    """The source could not be reached, for this stated reason."""

    data: PanelStorageUnavailableData
    panel: typing.Literal["unavailable"]


class PanelStorageUnavailableData(typing.TypedDict):
    reason: str
    """Why the panel could not be filled, in the operator's terms."""


type PanelVpn = PanelVpnReady | PanelVpnUnavailable
"""A panel's content, or the reason its source could not fill it.

The difference between \"this panel is up to date\" and \"this panel's source is
unreachable\" is the whole of degrading honestly: an unavailable panel says so,
in its own words, rather than showing stale data as current or blank data as
zero — and the panels beside it stay live.
"""


class PanelVpnReady(typing.TypedDict):
    """The source answered; here is the panel."""

    data: Vpn
    panel: typing.Literal["ready"]


class PanelVpnUnavailable(typing.TypedDict):
    """The source could not be reached, for this stated reason."""

    data: PanelVpnUnavailableData
    panel: typing.Literal["unavailable"]


class PanelVpnUnavailableData(typing.TypedDict):
    reason: str
    """Why the panel could not be filled, in the operator's terms."""


class Part(typing.TypedDict):
    """One part of a traced item — an episode of a series. A film has no parts: the item is
    the whole, and a trace of it says all there is to say. A series does not, which is the
    gap this closes: \"the show is imported\" is true the moment one episode lands, and reads
    as done while nine are still missing.
    """

    number: int
    """Its number within that season."""
    season: int
    """Which season it belongs to."""
    stage: Stage
    """How far this one part got, on the same scale as the item as a whole."""
    title: str
    """Its title, as a person would name it."""


class Passed(typing.TypedDict):
    """Where a refusal's words were carried, and when."""

    at: typing.NotRequired[str | None]
    """When the attempt was made, absent where the clock could not be written down."""
    to: list[str]
    """The services they reached, by the names the member knows them by. Empty where
    there was nowhere this could send.
    """


class PausedClient(typing.TypedDict):
    """What one download client said about being paused or resumed."""

    client: str
    """The client, by the name the stack knows it under."""
    now: typing.NotRequired[Pulling | None]
    """What it read back after it was asked. Absent on a rehearsal, which asks nothing,
    and where the client could not be reached.
    """
    unreached: typing.NotRequired[str | None]
    """Why it could not be reached, in its own words where it gave any."""
    was: typing.NotRequired[Pulling | None]
    """Whether it was fetching before it was asked, where it said."""


type Pausing = typing.Literal["pause", "resume"]
"""Which of the two was asked for."""


class PausingReport(typing.TypedDict):
    """What pausing or resuming every download client came to."""

    asked: Pausing
    """Which of the two was asked for."""
    caution: typing.NotRequired[str | None]
    """What a resume runs into where a spent cap had stopped the clients: they are let
    go as asked, and the cap stops them again the next time the line is checked.
    """
    clients: list[PausedClient]
    """Every download client the stack runs, in the order the stack declares them."""
    rehearsed: bool
    """Whether this was a rehearsal: what each client is doing now, with nothing asked
    of any of them.
    """


type Period = typing.Literal["active", "quiet"]
"""Which side of the household's day a moment falls on."""


type Phase = typing.Literal["in-progress", "reviewing", "applying", "applied"]
"""Where an in-flight or finished setup stands in its lifecycle.

The persisted marker a later run reads to tell answers still being gathered
from a half-written apply. Only these four are ever written: the two states a
run infers instead of storing — no setup at all, and an apply that stopped
mid-write — are read off the world rather than trusted from a file (see
[`Status`]).
"""


class Piece(typing.TypedDict):
    """One file inside a bundle: the name it will carry, and what it holds.

    Held in memory rather than written as it is gathered, because everything is read back
    before anything is written. A bundle that had already put one file on disk when it
    found a credential in the next would have to be unwritten, and unwriting is the kind of
    thing that half-works.
    """

    body: str
    """What it holds, already redacted."""
    name: str
    """What it is called inside the bundle."""


class Plan(typing.TypedDict):
    """What will be run, and what was left out.

    Serialisable because it is an answer in its own right: asking what a form
    would do is a question a script asks as readily as a person, and the plan a
    lifecycle report carries is this same value rather than a retelling of it.
    """

    dropped: list[Dropped]
    """Profiles the closure asked for that the configuration does not support."""
    filtered: list[Filtered]
    """The services those profiles hold, each with what it needed and who asked.

    The same answer as [`Self::dropped`], a service at a time. A surface showing what
    did not start shows services, and one holding its own copy of which service sits
    in which profile would be a second copy of the stack's vocabulary.
    """
    footprint: Footprint
    """What the stack estimates the services that would start need."""
    forms: list[str]
    """The forms the operator named, in the order they named them."""
    profiles: list[str]
    """The profiles to activate, sorted so the command is reproducible."""
    running: typing.NotRequired[list[str] | None]
    """Which of [`Self::services`] are already running, where a form's introspection
    asked the engine.

    Starting a form leaves what is already running as it is, so a running service
    is not one the start would bring up. Absent where nothing asked, which is every
    plan but a preview's; `null` where the engine would not say, which is never said
    as nothing running.
    """
    services: list[str]
    """The services those profiles start, in the order the stack declares them.

    A service belongs to exactly one profile, so a service two named forms
    both reach is here once. That is a property of the manifest rather than
    of a pass over this list: the union is over profiles, and a service
    appearing twice is not a state this can hold.
    """


type PluginAdapterOwner = typing.Literal["lemonfiber"]
"""Whose an adapter is.

One answer, and the field exists so that the answer is on the wire: an adapter a
plugin could bring would be code a stranger wrote running with lemonfiber's
authority, which nothing here can load.
"""


class PluginChange(typing.TypedDict):
    """One change installing a plugin makes to the machine.

    A path and what goes at it, which is the whole of what an install touches. Two of
    them can be edits to a file the stack already has — the proxy's and the
    dashboard's — and those say so, as a region, so an operator reading the account
    knows which of their files the install writes into.
    """

    path: str
    """Where it lands, in full.

    In full rather than relative to the stack, because *what is this about to do
    to my machine* is answered by a path somebody can go and look at — and a
    relative one is right about a directory the reader has to work out for
    themselves.
    """
    puts: PluginPuts
    """What lands there."""


class PluginChangedCheck(typing.TypedDict):
    """One check that stands differently after an install than it did before."""

    before: typing.NotRequired[DoctorVerdict | None]
    """How the same check read before the install, or nothing where it was not
    raised at all.

    Absent means the check produced no finding beforehand, which is read as it
    holding: a finding no longer raised is a fault no longer there, and the same
    rule read backwards is that one not yet raised was not yet a fault.
    """
    now: Finding
    """The check as it reads now, with everything the diagnosis says about it.

    The finding itself rather than a summary of it, because what an operator does
    next is read the remedy, the service's own output and what else is causing it
    — and a second, thinner shape of the same fact is where those stop arriving.
    """


type PluginConstraint = typing.Literal[
    "status",
    "json",
    "json_has_keys",
    "json_types",
    "json_at_least",
    "json_array_min",
    "json_is_absent",
    "content_type",
    "body_starts_with",
]
"""A kind of constraint an expectation can put on a body.

The same vocabulary a proof's expectation and a contributed check's use, so that
\"a status alone is not evidence\" is one rule rather than three. Read as well as
written: a declaration that an assertion fails on a recording names the one of these
that fails there.
"""


class PluginDeclaration(typing.TypedDict):
    """What a plugin declared about itself, as its install read it."""

    claims: typing.NotRequired[list[str]]
    """Every capability it claims, core and its own, in the order it declares them.

    Apart from what its services fill: a claim is what it says it can do and has to
    demonstrate, and a capability of its own is claimed without anything asking for
    it.
    """
    license: typing.NotRequired[str]
    """The licence it is distributed under."""
    overrides: typing.NotRequired[list[PluginOverriding]]
    """Every bundled setting it declares it may change."""
    reaches: typing.NotRequired[list[str]]
    """Every destination a recipe of its could reach that is not one of its own
    services: a service of this stack's, or a name outside it.

    Recorded as declared rather than sorted into the two here, because which names
    are this stack's is a question about the stack, and the stack a record is read
    against is the one on the machine when it is read.
    """
    reviewed: typing.NotRequired[bool]
    """Whether anybody reviewed it before it was installed.

    True for a plugin installed by name through a catalogue index whose signature
    verified, and false for every install from a source an operator named. Carried
    rather than left implicit, because an unreviewed plugin is to be said to be one
    for as long as it is installed.
    """
    secrets: typing.NotRequired[list[PluginSecret]]
    """Every credential it says it will hold."""
    upstream: typing.NotRequired[str]
    """Where its source is published, as the plugin names it."""


type PluginDeclaredVerdict = typing.Literal["fails"]
"""The one verdict a declaration may name."""


type PluginEvidence = typing.Literal["recordings", "service"]
"""What the verdicts in a report were reached against.

One value, because one is all this build can produce: nothing here asks a service
anything. It is a field rather than a sentence for the reason a verdict is one — a
reader handed `demonstrated` has nothing else in the document to tell a recording
that answered from a service that did, and the weaker of those two claims must not
be readable as the stronger. The prose says it on the page; this says it to
whatever consumes the report: an author's own CI, a catalogue, anything counting
passes. Naming the axis now is what made the second kind of evidence a change the
compiler walked somebody through rather than one they had to remember.
"""


class PluginExpectedFailure(typing.TypedDict):
    """A recording an assertion fails on, the one constraint of its expectation that fails
    there, and why.

    For an assertion whose passing state nobody can record, such as a check that a server
    has an owner where claiming one needs an account the plugin's CI does not hold: the
    state it exists to find can be recorded, and the declaration says which constraint
    tells the two states apart. It changes the verdict on that recording and on nothing
    else — the live service and every other recording are held to the expectation as it
    is written.

    It names a constraint rather than only a recording, because a recording that began
    failing for another reason — a truncated file, an error recorded by mistake — would
    otherwise read as failing as declared, excusing a failure nobody had looked at.
    """

    constraint: PluginConstraint
    """The key of the expectation that fails on the recording, and one it carries."""
    fixture: str
    """The recording the assertion fails on. It may be the assertion's own `fixture`."""
    place: typing.NotRequired[str | None]
    """Where within that constraint it fails, written exactly as the expectation writes
    it. Present for a key-wise constraint and absent for one about the whole answer.
    """
    reason: str
    """Why this recording is one the assertion fails on. Reported with the verdict every
    time.
    """
    verdict: PluginDeclaredVerdict
    """`fails`, and nothing else: passing is what the expectation already says, and
    could-not-run is never excused.
    """


class PluginFailingAsDeclared(typing.TypedDict):
    """One recording an assertion fails on as its manifest declares."""

    constraint: PluginConstraint
    """The constraint of the expectation that fails there."""
    fixture: str
    """The recording."""
    held: str
    """What the recording held there."""
    place: typing.NotRequired[str | None]
    """Where within that constraint, for one that looks at places."""
    reason: str
    """Why the manifest says this recording is one the assertion fails on."""


class PluginInstall(typing.TypedDict):
    """What an install came to, and what it took to get there.

    **The three lists below are stated whether the run wrote anything or not, and that
    is the whole of what makes a rehearsal worth running.** A rehearsal that reported
    less than the real run would be a preview of a different operation; one that
    reported it from code of its own would be a second derivation free to disagree
    with the one that acts. So they are filled in one place, from the manifest and from
    the very list of writes the install is carried out from, and the surface says them
    in whichever tense `recorded` calls for.
    """

    against: typing.NotRequired[PluginEvidence | None]
    """What those verdicts were reached against, or nothing where none were reached.

    Carried rather than assumed, because the two kinds of evidence are not the
    same claim: an author's read asks the recordings a plugin ships, and an
    install asks the service running on this machine. The weaker must not be
    readable as the stronger, and a reader handed a verdict has nothing else in
    the document to tell them apart.
    """
    changes: list[PluginChange]
    """Every change it makes to the machine, in the order it makes them."""
    contests: list[WiringContest]
    """Every ask of the stack's the install leaves contested that is not contested
    now, as it would then stand.

    A plugin's service that claims what the stack asks for is a candidate like any
    other, so installing it leaves the ask refused until somebody chooses — which is
    a change to what the stack does, and stated with the rest before it happens.
    """
    overrides: list[PluginOverriding]
    """Every bundled thing the plugin declares it will change.

    The full extent rather than a sample of it: a manifest may change a bundled
    setting only through a recipe, and a recipe reaching one no `[[override]]`
    names is refused before anything is written.
    """
    proofs: list[PluginProving]
    """Every proof that has to hold before the plugin is installed, and on a run
    that asked them, what each came to.
    """
    recorded: bool
    """Whether it was written down. A rehearsal leaves this false."""
    reversed: typing.NotRequired[UndoReversal | None]
    """What putting the install back came to, where something failed and it was.

    The rollback layer's own report rather than a shape of this verb's: what went
    back, and what did not with the reason each is still standing. Absent on a run
    that had nothing to put back, which is both a rehearsal and an install that
    held.
    """
    verified: typing.NotRequired[PluginVerification | None]
    """What the stack's own checks made of the install, or nothing on a run that
    asked them nothing.

    The other half of what an install has to establish, and the half a plugin
    cannot establish for itself: its proofs say the plugin works, and this says the
    stack still does. Absent on a rehearsal, which writes nothing and so has
    nothing to hold a reading against.
    """
    would: PluginInstalled
    """What the install settled, said whether or not it was written down."""


class PluginInstalls(typing.TypedDict):
    """What is installed, and what installing one came to.

    One answer for the reading and for the verb, because they are one question: an
    operator who has just installed something wants to see it among what they had, and
    a rehearsal that showed only the new entry would not say what it is joining.
    """

    agreement: typing.NotRequired[str | None]
    """What this run's reading names itself, so an answer to it can say which reading
    it answered; nothing on the reading of what is installed, which offers nothing.

    Named part by part, so an answer refused because something moved is told which
    part did.
    """
    install: typing.NotRequired[PluginInstall | None]
    """What this run's install came to, or nothing where it only read.

    Boxed for the reason the update is: it carries a whole account, and every other
    run's report would otherwise be as large as the one run that installs.
    """
    installed: list[PluginInstalled]
    """Every plugin the record holds.

    What it holds, rather than what it would hold: a rehearsal wrote nothing, so
    what it settled is in `install` and not here. A listing that counted it
    would report an install that did not happen.
    """
    rehearsed: bool
    """Whether this was a rehearsal: what would have happened, with none of it done.

    Said in a field of its own so that a rehearsal is never told from the real run by
    its wording alone.
    """
    removal: typing.NotRequired[PluginRemoval | None]
    """What this run's removal came to, or nothing where it removed nothing.

    Beside the install rather than in place of it, and never both at once: an
    install and a removal are two verbs with two accounts, and a field that held
    whichever happened would make a reader ask which one this was before they could
    read it.
    """
    sources: typing.NotRequired[list[PluginSource]]
    """Whether each installed plugin's source can still be fetched, asked now.

    Filled on the reading of what is installed and nowhere else, for the reason
    `substituted` is: it is the one read an operator makes of what each plugin is
    doing, and the one moment this machine asks anybody where a plugin came from. A
    run that installs, updates or removes one leaves it empty.
    """
    substituted: typing.NotRequired[list[PluginSubstituted]]
    """Every capability the operator chose an installed plugin's service to fill.

    Filled on the reading of what is installed, which is the one read of what each
    plugin is doing; a run that installs, updates or removes one leaves it empty,
    because none of them changes a choice.
    """
    update: typing.NotRequired[PluginUpdate | None]
    """What this run's update came to, or nothing where it updated nothing.

    A third field rather than an install and a removal filled in together, for the
    reason those two are apart: an update is one operation with one account.

    Boxed because it carries a whole install's account beside the reversal, and
    every other run's report would otherwise be as large as the one run that updates.
    """


class PluginOverriding(typing.TypedDict):
    """One bundled thing a plugin declares it will change."""

    setting: str
    """Which bundled setting it changes."""
    why: str
    """What changing it is for."""


class PluginPair(typing.TypedDict):
    """One value a recipe could carry to one destination, as the operator agrees to it."""

    approval: str
    """What approving this pair is written as, on the command line and over the web."""
    origin: str
    """Whose value it is, as the step that captures it says; empty where no step does."""
    to: str
    """Where it may be carried, by the name the manifest gives it."""
    value: str
    """What the value is called within the recipe."""


class PluginPlaced(typing.TypedDict):
    """One service of an installed plugin, as it was placed."""

    api: typing.NotRequired[Api | None]
    """The adapter lemonfiber reaches it through, where the plugin named one.

    Defaulted for a record written before this was kept, which reads as naming
    none: a service operated generically, as it was when installed.
    """
    config_path: str
    """Where inside the container its one configuration directory is mounted.

    Resolved rather than optional. The record answers where the directory is, and
    a run that re-derived the fallback would answer for a container it did not
    write the day that fallback moved.
    """
    description: typing.NotRequired[str]
    """What the plugin says it does for the operator, which is what its dashboard entry
    says beside it.
    """
    digest: str
    """The digest that fixes what runs."""
    image: str
    """The registry path, carrying no pin of its own."""
    listens: typing.NotRequired[int | None]
    """The port it answers on inside the stack's network, where it declared one."""
    media_types: typing.NotRequired[list[str]]
    """The media it files, in the stack manifest's vocabulary, which decides what it
    comes to in each service that asks for what it provides.

    Defaulted for a record written before this was kept, which reads as filing
    nothing named.
    """
    name: typing.NotRequired[str]
    """What it is called, for a reader, which is what its dashboard entry is listed as.

    Defaulted for a record written before this was kept, which lists it by its id
    rather than leaving it off the panel.
    """
    networks: typing.NotRequired[list[str]]
    """The stack's own networks it joins beside the default one, because a stack service
    it stands in for is on them.

    Settled at install from the stack it was installed beside and written down, so
    the container lemonfiber writes for it stays a function of this record alone.
    Defaulted for a record written before this was kept, which reads as joining none
    and staying on the default network.
    """
    provides: typing.NotRequired[list[str]]
    """Every core capability this one service fills, which is what makes it a candidate
    when the stack asks for one.

    Per service rather than read off the plugin's whole list, because a wiring
    reaches a service and not a plugin: of a plugin's two services, the one that
    fills a capability is the one an ask for it would reach. Defaulted for a record
    written before this was kept, which reads as filling nothing — a service nothing
    is wired to, rather than one wired to on a guess.
    """
    reached: typing.NotRequired[PluginReached | None]
    """How it is reached, or nothing where it has no listener."""
    service: str
    """The service's id, which is the name its container is written under."""
    tag: str
    """The readable name that digest went by when it was installed."""
    takes_data: bool
    """Whether the library is mounted for it."""


class PluginProving(typing.TypedDict):
    """One proof that has to hold before a plugin is reported installed."""

    asks: str
    """What it asks, as the method and the path it is asked at."""
    came_to: typing.NotRequired[PluginVerdict | None]
    """What asking it came to, or nothing where it was not asked.

    Absent on a rehearsal, which asks nothing. That is a different fact from a
    proof that was asked and established nothing, and the two must not read alike:
    one is an account of what would happen, the other is a service that did not
    answer.
    """
    establishes: str
    """What it establishes, in one line."""
    of: typing.NotRequired[str | None]
    """Which of the plugin's services it asks, where the manifest settles that.

    Nothing where it does not, which is a manifest the reader has already refused
    — carried as an absence rather than as a guess, so that a report built from a
    manifest nobody held to the reader says *this was not settled* instead of
    naming whichever service came first.
    """
    proof: str
    """The proof's id, which its verdict is reported against."""
    why: str
    """Why it is worth asserting."""


type PluginPuts = typing.Literal["directory", "document", "region"]
"""What an install puts at one path."""


type PluginReached = PluginReachedLoopback | PluginReachedHousehold
"""How an installed service is reached, where it is reached at all.

The tier is the arm, so the label a tier earns lives only in the arm entitled to
one. Only a household service is proxied — the bundled policy is that an admin
surface does not get a name on the household network — and a record able to carry
a loopback service with a hostname would be a record able to describe the thing
that policy exists to prevent.

**The group is on both arms, and that is not an oversight.** Only the proxy is
the household tier's alone; the bundled dashboard carries an entry for an
operator surface too, with the address it links to rendered from the tier — nine
of the shipped stack's own entries point at this machine. A record that kept the
group for the wider tier alone would leave a loopback service off the panel its
bundled neighbours are on.

A tier and never an address, either way: lemonfiber renders one from the other
exactly as it does for a bundled service, so the two-tier policy stays a property
of the system rather than a request a plugin made.
"""


class PluginReachedHousehold(typing.TypedDict):
    """From the household, through the stack's own proxy, at this label."""

    group: typing.NotRequired[str | None]
    """The group on the bundled dashboard, where the manifest named one."""
    hostname: str
    """The single label in front of the operator's domain."""
    port: int
    """The port the service listens on."""
    tier: typing.Literal["household"]


class PluginReachedLoopback(typing.TypedDict):
    """From this machine and nowhere else. No route, and no label to route to."""

    group: typing.NotRequired[str | None]
    """The group on the bundled dashboard, where the manifest named one."""
    port: int
    """The port the service listens on."""
    tier: typing.Literal["loopback"]


class PluginRecipe(typing.TypedDict):
    """One recipe, as an operator agrees to what it does."""

    id: str
    """The recipe's id within the plugin."""
    pairs: list[PluginPair]
    """Every value it could carry, and where to."""
    steps: list[PluginStep]
    """Every call, in the order the recipe makes them."""
    title: str
    """What it accomplishes, in one line."""
    why: str
    """Why it is worth running."""


class PluginRemoval(typing.TypedDict):
    """What taking a plugin off the machine came to, or would come to."""

    interrupts: list[str]
    """Every service that stops when it goes, named before any of them does.

    By service rather than by plugin, because a service is what an operator notices
    stopping: a plugin that brought two containers takes two things away, and the
    plugin's name alone would not say which of the addresses they use goes quiet.
    None of them comes back — a removal is not a restart — which is why this is
    stated before the run rather than discovered after it.
    """
    leaves: list[PluginUnfilled]
    """Every capability that would have nothing filling it afterwards.

    Stated before it happens rather than reported after, which is the requirement
    and also the only useful order: an operator told afterwards that their requests
    no longer reach anything has been informed rather than asked.
    """
    plugin: str
    """The plugin this is about."""
    removed: bool
    """Whether the record of what is installed was written without it.

    False on a rehearsal and on a run that got as far as putting the files back and
    no further, which are two different machines and are told apart by what the
    reversal says rather than by a second flag here.
    """
    went_back: UndoReversal
    """What putting its changes back came to, or would come to.

    The rollback layer's own report rather than a shape of this verb's: a removal is
    a reversal with a name on it, and an account of its own would be a second
    description of the same work.
    """


class PluginRequest(typing.TypedDict):
    """What is asked, and where.

    Three fields and no more, and the third is the one worth explaining. A service that
    answers XML unless a caller asks for JSON cannot satisfy a capability whose probe
    requires a JSON assertion, and until this field there was nowhere to ask: Plex
    answers `text/xml` at every path, including the one its health probe uses, unless
    the request carries `Accept: application/json`.

    **It is one media type and not a header map, and the difference is the point.** A
    probe declares who it is asked as, and `none` on every `guarded` probe has meant what
    it says partly because nothing could be presented. A map of headers would make that a
    convention a reviewer has to hold — any service may name its credential header
    whatever it likes, so no list of refused names could ever be closed — where one named
    field keeps it a property of the format. A probe still cannot present anything,
    because there is nowhere to write it.
    """

    accept: typing.NotRequired[str | None]
    """The one representation the answer is asked for, as a media type.

    Absent where the service needs no asking, which is most of them.
    """
    method: str
    """The HTTP method."""
    path: str
    """The path on the service being asked."""


class PluginRestored(typing.TypedDict):
    """Where an update did not hold: what putting the version it replaced back came to."""

    placed: bool
    """Whether everything its record says it placed is on the machine again."""
    running: bool
    """Whether its containers are running again.

    Apart from `placed`, because the two fail differently: a document that would not
    land is a disk, and a container that would not start is the engine — and an
    operator fixes them in different places.
    """
    version: str
    """The version put back, which is the one the record still names."""


class PluginSecret(typing.TypedDict):
    """One credential a plugin says it will hold, without a value and with no place for one."""

    id: str
    """What the value is, within the plugin."""
    of: str
    """Whose credential it is."""
    why: str
    """What holding it is for."""


class PluginServiceAdapter(typing.TypedDict):
    """One adapter of lemonfiber's that one of the plugin's own services names."""

    kind: ApiKind
    """Which of lemonfiber's adapters it is."""
    owner: PluginAdapterOwner
    """Whose it is, which is lemonfiber's."""
    service: str
    """The service that names it."""


type PluginSourceStanding = (
    PluginSourceStandingReachable | PluginSourceStandingUnreachable | PluginSourceStandingUnasked
)
"""What asking a plugin's source came to.

**Unreachable is not untrusted.** A plugin whose source has gone keeps running as it
was installed; what it loses is the way to a newer version, and that is said now
rather than found out at the next update.
"""


class PluginSourceStandingReachable(typing.TypedDict):
    """It answered, so the plugin can be updated from it."""

    standing: typing.Literal["reachable"]


class PluginSourceStandingUnasked(typing.TypedDict):
    """Nothing was asked, so nothing is known either way."""

    standing: typing.Literal["unasked"]
    why: str
    """Why nothing was asked."""


class PluginSourceStandingUnreachable(typing.TypedDict):
    """It did not answer, or is no longer there, so the plugin cannot be updated from it."""

    standing: typing.Literal["unreachable"]
    why: str
    """What asking it said."""


class PluginStep(typing.TypedDict):
    """One call a recipe makes, in the order it makes them."""

    adapter: typing.NotRequired[PluginStepAdapter | None]
    """The adapter the destination is reached through, or nothing where it is a name
    outside the stack, which no adapter of lemonfiber's speaks to.
    """
    id: str
    """The step's id within its recipe."""
    method: str
    """The HTTP method it calls with."""
    path: str
    """The path it calls."""
    to: str
    """Where it calls: a service of this stack's or the plugin's own, or a name outside
    both, as the manifest wrote it. Never a resolved address.
    """


class PluginStepAdapter(typing.TypedDict):
    """The adapter a call reaches its destination through."""

    kind: ApiKind
    """Which of lemonfiber's adapters it is."""
    owner: PluginAdapterOwner
    """Whose it is, which is lemonfiber's."""


class PluginSubstituted(typing.TypedDict):
    """A capability the operator chose one of a plugin's services to fill.

    The only way anything a plugin brought comes to fill what the stack asks for in
    place of the stack's own: a plugin cannot choose, and wiring by name is not
    something a plugin can introduce. So what a plugin substituted is what the operator
    substituted with it, and it is read off the recorded choices rather than off the
    plugin.
    """

    capability: str
    """The capability it fills."""
    plugin: str
    """The plugin whose service it is."""
    service: str
    """The service chosen."""


class PluginUnfilled(typing.TypedDict):
    """A capability that would have nothing filling it."""

    capability: str
    """The core name nothing would fill."""
    filled_by: str
    """The plugin that is filling it now, which is the one going.

    Named rather than left to the reader, because the sentence an operator has to
    act on is *this is the only thing filling it* and a capability on its own does
    not say that.
    """


type PluginVerdict = (
    PluginVerdictPassed | PluginVerdictFailed | PluginVerdictUnproven | PluginVerdictFailingAsDeclared
)
"""What one assertion came to, whatever answered it."""


class PluginVerdictFailed(typing.TypedDict):
    """It does not, in every way it does not."""

    faults: list[str]
    """Every way the recorded answer is not the declared one."""
    outcome: typing.Literal["failed"]


class PluginVerdictFailingAsDeclared(typing.TypedDict):
    """It fails on the recordings its manifest declares it fails on, on the constraint
    each declaration names and on nothing else, and holds on every other recording it
    was run against.

    Apart from passed and from failed, and counted as neither. The assertion does not
    hold there, so a pass would say the opposite of what the recording shows; and the
    failure is the one its author described and gave a reason for, so it does not
    fail the run. Only ever reached against recordings: the live service is held to
    the expectation as it is written.
    """

    declared: list[PluginFailingAsDeclared]
    """Each declared recording, what it held, and why it is one the assertion fails on."""
    outcome: typing.Literal["failing-as-declared"]


class PluginVerdictPassed(typing.TypedDict):
    """The recording answers what the binding declares."""

    outcome: typing.Literal["passed"]


class PluginVerdictUnproven(typing.TypedDict):
    """It could not be run, and so established nothing either way."""

    outcome: typing.Literal["unproven"]
    why: str
    """What stopped it being run."""


class PluginVerification(typing.TypedDict):
    """What the stack's own checks made of an install."""

    broke: list[PluginChangedCheck]
    """Every check this install made worse.

    Empty is the answer an install needs, and it is the common one. What is here
    is what takes the install back.
    """
    unsettled: list[PluginChangedCheck]
    """Every check nothing could be concluded about across the two readings.

    Reported and never acted on. *I could not tell* is not *it is still broken*,
    and an install reversed because a check could not reach a provider it also
    could not reach an hour ago would be punishing a plugin for the weather. It is
    said out loud rather than dropped, because the assurance an operator thought
    they had is the thing that went.
    """


type Policy = typing.Literal["trusted", "within-a-limit", "everything-waits"]
"""What happens to what a household member asks for.

Three, and they are the three the request service can actually be put into. A
household is in one of them because of two settings taken together — whether requests
arrive unseen, and whether a period limits how many — so the words here are a reading
of that pair rather than a fourth setting kept beside it.

Choosing per person is not a fourth policy. It is one of these three chosen for one
member rather than for the house, which is why what a surface offers is a policy and,
separately, who it is for.
"""


class PresetChoice(typing.TypedDict):
    """One preset in force, and what it means for the media it applies to — the
    operator's question answered in their own terms, with no scoring vocabulary.
    """

    means: str
    """What it means, in the operator's terms rather than the tool's."""
    needs_transcoding_here: bool
    """Whether this host would have to transcode it in software — the caution
    stated before a choice a household cannot smoothly play.
    """
    preset: str
    """The preset's plain-language name."""
    resolution: str
    """The resolution and encode it targets."""
    scope: str
    """What this applies to: `everything`, or a specific media type."""
    size_per_hour: str
    """Roughly how much disk an hour of it takes."""
    transcoding: str
    """What playback costs, in plain terms."""


class Preview(typing.TypedDict):
    """What a restore would do, shown before anything is overwritten."""

    agreement: str
    """What this listing is, so consent given for it can name which listing it read.

    Carried on every listing rather than only on the ones that would re-point
    something: a surface that has to look for it is a surface that can fail to
    find it, and a restore that would overwrite the same configuration in place
    is still one somebody may agree to.
    """
    downgrade: bool
    """Whether the archive is old enough that a compatibility warning applies."""
    manifest: BackupManifest
    """The archive's own account of itself — its scope, version and contents."""
    relocation: typing.NotRequired[Relocation | None]
    """The data-root difference, where the archive was taken against another one."""


class Problem(typing.TypedDict):
    """Something that went wrong, in the form an operator can act on."""

    cause: typing.NotRequired[Problem | None]
    """The problem that produced this one, where several share a root."""
    code: Code
    """The stable identifier for this kind of problem."""
    detail: typing.NotRequired[str | None]
    """The underlying technical detail, available but never leading."""
    meaning: str
    """What it means for the operator."""
    remedies: list[Remedy]
    """What to do, most likely first."""
    severity: ProblemSeverity
    """How much it matters."""
    state: ProblemState
    """Where it stands with respect to being fixed."""
    summary: str
    """What happened, in one plain sentence."""


type ProblemSeverity = typing.Literal["advisory", "warning", "error", "critical"]
"""How much a problem matters.

Four levels, deliberately. More would not be applied consistently, and
inconsistent severity is worse than coarse severity.
"""


type ProblemState = typing.Literal["actionable", "guided", "remediable", "unknown", "suppressed"]
"""Where a problem stands with respect to being fixed."""


class Propagation(typing.TypedDict):
    """One consumer, and how far the rotation reached it."""

    consumer: str
    """What authenticates with the credential."""
    reach: CredentialReach
    """How far the rotation reached it."""


class Protection(typing.TypedDict):
    """The honest account of what the credential store protects against.

    Two lists and a sentence, carried as data rather than printed here, so the API
    serves the same words the terminal prints and neither can drift into a claim the
    other does not make.
    """

    against: list[str]
    """What it protects against."""
    not_against: list[str]
    """What it does not protect against."""
    summary: str
    """What the storage is, before any claim about it."""


class Protocols(typing.TypedDict):
    """Which download protocols the operator actually has accounts for.

    A form names both, because a form describes what it *does* rather than what
    this operator has paid for. Narrowing happens afterwards, so a tunnel is
    never started with credentials that were never supplied.
    """

    torrent: bool
    """A VPN and torrent client are configured."""
    usenet: bool
    """A Usenet provider is configured."""


class ProvenanceReport(typing.TypedDict):
    """Where every service in this stack comes from."""

    services: list[ServiceProvenance]
    """The services, in the order the stack declares them.

    Every service the manifest holds rather than the ones some form would start:
    what is *in* this stack is the question being asked, and an answer narrowed to
    what is running would leave the operator unable to ask about the service they
    are deciding whether to run.
    """


type Pulling = typing.Literal["fetching", "stopped"]
"""Whether a client is fetching at all, where a cap made it a question.

Apart from the limits above rather than folded in with them, because it answers
a different question and a client held to a crawl is not a client that stopped.
A word that named both would be the vocabulary this whole path exists to avoid.
"""


class QualityReport(typing.TypedDict):
    """The operator's quality choice, what each preset means, and what the command
    did with it.
    """

    choices: list[PresetChoice]
    """The global choice first, then each media type set apart from it."""
    customised: bool
    """Whether the Recyclarr config has been hand-edited since lemonfiber wrote it —
    the `customised` state, in which the preset is no longer authoritative until
    it is deliberately re-asserted. For a reapply, whether an edit was overwritten.
    """
    disposition: Disposition
    """What became of the choice."""
    music: typing.NotRequired[MusicChoice | None]
    """The audio-format choice for music, where one is set — media that has no
    resolution, so it is reported apart from the resolution presets rather than
    forced into their shape.
    """
    overwritten: typing.NotRequired[StackEdit | None]
    """The hand-edited config a reapply replaced — or, rehearsed, would replace — with
    the diff of what goes against what lands in its place.

    Absent everywhere else, and absent for a reapply over a config already in
    lemonfiber's own hand. Consent given against a yes-or-no is consent to
    something the operator was never shown: they know a file they edited is about
    to go, and not which of their lines is in it. The lines are masked the way
    every stack-file diff is, so a key that drifted is named without its value.
    """
    rehearsed: bool
    """Whether this was a rehearsal: what would have happened, with none of it done.

    Said in a field of its own so that a rehearsal is never told from the real run by
    its wording alone.
    """


class Queue(typing.TypedDict):
    """One `*arr`'s queue, and how much of it is stuck."""

    depth: int
    """How many items are queued."""
    service: str
    """The service whose queue this is."""
    stuck: int
    """How many of them are stuck rather than progressing."""


type Ran = bool
"""Whether a walk through setup was carried out or rehearsed, written as the bare
`true` or `false` every other report writes its `rehearsed` as.

Two words rather than a fourth switch on a report that already holds three, which
is a report somebody reads by remembering which `true` means what. On the wire it
is the same boolean every report carries, so a client reads one shape.
"""


class Rated(typing.TypedDict):
    """What one age limit comes to, in the certificates named for it.

    Both sides, because either alone misleads. What is allowed without what is held
    back reads as a limit that stops nothing; what is held back without what is allowed
    reads as a limit that stops everything.
    """

    allows: list[str]
    """The certificates at the highest age this limit still lets through.

    Empty where the table names nothing at or below the limit, which is a limit
    that lets nothing rated through at all.
    """
    fell_back: bool
    """Whether these came from lemonfiber's own mapping because the media server's
    table named no certificates.

    Carried rather than hidden: a certificate said to be this household's when it
    is this program's is the kind of claim a parent would act on.
    """
    holds_back: list[str]
    """The certificates at the lowest age this limit holds back.

    Empty where the table names nothing above the limit, which is a limit that
    holds nothing rated back at all.
    """


type Reached = typing.Literal["within", "warning", "exceeded"]
"""Where a month stands against a declared cap."""


type Reaches = ReachesAsked | ReachesByName
"""What one link reaches, and how that was settled."""


class ReachesAsked(typing.TypedDict):
    """An ask for a capability."""

    capability: str
    """The capability asked for."""
    how: typing.Literal["asked"]
    origins: dict[str, ValueOrigin]
    """Where each service that claims it came from: this build's stack, or a
    named plugin.

    Every claimant rather than only what the ask reaches, because a contest
    reaches nothing and is exactly where an operator most needs to know which of
    the names in front of them is not the stack's.
    """
    services: list[str]
    """What the ask reaches — empty where nothing fills it or a contest stands."""
    settled: WiringSettled
    """How it was settled."""


class ReachesByName(typing.TypedDict):
    """A link deliberately kept to a named service, shown as the exception it is."""

    how: typing.Literal["by-name"]
    service: str
    """The service named."""
    why: str
    """Why it is by name."""


type Reason = typing.Literal[
    "no-indexers",
    "indexers-failed",
    "nothing-matched",
    "none-met-the-preset",
    "tunnel-down",
    "not-grabbed",
    "stalled",
    "import-failed",
    "no-media-server",
    "not-visible",
]
"""Why a walkthrough could not go on."""


class Reckoning(typing.TypedDict):
    """Where the disk stands, what is on it, and what could be got back."""

    agreement: str
    """What this offer names itself, so an answer to it can say which offer it was
    answering. The answer is this name, and nothing else is a yes to a cleanup.
    """
    candidates: list[Candidate]
    """The completed downloads, each with where it stands and what removing it
    would cost.
    """
    consumption: list[Consumption]
    """Where the room went, one line per tree plus the services' own files, and
    one line for what is committed but has not landed yet.
    """
    halted: bool
    """Whether new acquisitions are halted to keep the services writable."""
    interrupted: list[Interrupted]
    """The imports that stopped part-way, with what is on disk for each."""
    level: Level
    """Where the stack stands, which is where its worst volume stands."""
    outsized: list[Outsized]
    """The files far enough out of line with the rest to be worth pointing at."""
    reclaimable: list[Consumption]
    """What of that room could be got back, and what each would cost.

    A second reading of bytes already counted above rather than more of them: a
    seeding torrent's file is in the tree it lives in *and* here. Summing the
    two lists together would double what is on the disk, which is the mistake
    this whole module is arranged to avoid.
    """
    reclaimed: typing.NotRequired[Reclaimed | None]
    """What became of an answered cleanup, where the offer was answered."""
    rehearsed: bool
    """Whether this was a rehearsal: what would have happened, with none of it done.

    Said in a field of its own so that a rehearsal is never told from the real run by
    its wording alone.
    """
    volumes: list[Volume]
    """The volumes watched. Either filling stops the stack, so both are reported
    whether or not they are the same drive.
    """


type Reclaim = typing.Literal[
    "by_losing_content",
    "in_progress",
    "at_the_cost_of_ratio",
    "the_easy_win",
    "already_have_it",
    "marginally",
    "you_said_not",
]
"""What getting a line's room back costs."""


class Reclaimed(typing.TypedDict):
    """What became of an answered cleanup."""

    bytes: int
    """What they occupied."""
    gone: list[str]
    """The paths that were taken, or would have been in a rehearsal."""
    left: list[SpaceLeft]
    """What could not be taken, and what the platform said about it."""
    rehearsed: bool
    """Whether this was a rehearsal. Rehearsed, `gone` and `bytes` are what would have
    been taken and nothing was: no room was freed.
    """


class RecordReport(typing.TypedDict):
    """One record carried across, or that would be."""

    kind: str
    """What kind of record it is, in the plural a person reads."""
    name: str
    """What it is called."""
    service: str
    """The service it belongs to."""


class Refusal(typing.TypedDict):
    """A named front door that is not one, and why it is not."""

    because: str
    """Why this stack will not send a household there."""
    named: str
    """What the operator recorded, as they wrote it."""


class Refused(typing.TypedDict):
    """What was said when one request was turned down."""

    at: typing.NotRequired[str | None]
    """When it was turned down, so somebody reading it later knows which answer this
    was rather than assuming it is the newest.

    Absent where the machine's clock could not be written as a date, which is a
    refusal worth keeping the words of and not worth losing them over.
    """
    expired: typing.NotRequired[bool]
    """Whether nobody ruled on it and the period the household agreed to closed it,
    rather than an operator turning it down.

    The words are then this program's own, which is why the two are told apart here
    and not left to be read off the sentence: an operator scanning for what happened
    while they were away is looking for exactly the ones nobody answered, and a
    member is owed the difference between having been refused and having run out.

    Absent from every record written before a household could arrange this, which is
    the right reading of them — they are all somebody's own refusals.
    """
    reason: str
    """Why, in the words it was turned down in."""
    told: typing.NotRequired[Passed | None]
    """Whether the words have been carried to whoever asked, and where to.

    Absent until the one attempt has been made. **This is what makes a second one
    impossible rather than unlikely**: carrying happens only where this is absent,
    and it is written whether anything was reached or not — so a member with nowhere
    to send to is asked about once, and a household is never told the same thing
    twice by a run that happened to be started twice.
    """


class Release(typing.TypedDict):
    """One release, and everything the record holds about it."""

    carried: typing.NotRequired[str | None]
    """The version whose goals this tag carried, where that is not its own."""
    delivers: typing.NotRequired[str | None]
    """What it set out to deliver, in the words the version was staged under."""
    groups: list[Group]
    """The changes, gathered by what kind of change each is."""
    patches: typing.NotRequired[str | None]
    """The version this one patched, where it is a patch."""
    released_on: typing.NotRequired[str | None]
    """The day it was published, where the record of it says."""
    tag: str
    """The tag it was cut from."""
    user_facing: bool
    """Whether anything in it is a change an operator would notice."""
    version: str
    """The version, without the tag's leading letter."""
    withdrawn: typing.NotRequired[str | None]
    """Why it was withdrawn, where it was."""


class ReleaseSummary(typing.TypedDict):
    """One release as a listing shows it: everything but what it changed.

    Kept apart from [`Release`] rather than being it with the entries left out,
    because the two are read for different things. A listing answers which releases
    there have been and which of them was taken back; only the one being read needs
    to carry every line of what it changed.
    """

    delivers: typing.NotRequired[str | None]
    """What it set out to deliver."""
    patches: typing.NotRequired[str | None]
    """The version this one patched, where it is a patch."""
    released_on: typing.NotRequired[str | None]
    """The day it was published, where the record of it says."""
    user_facing: bool
    """Whether anything in it is a change an operator would notice."""
    version: str
    """The version."""
    withdrawn: typing.NotRequired[str | None]
    """Why it was withdrawn, where it was."""


class Relocation(typing.TypedDict):
    """A restore whose archive was taken against a different data root than the one
    configured now, so its stored paths would land where nothing exists.
    """

    now: str
    """The data root configured now."""
    was: str
    """The data root the archive was taken against."""


class Remedy(typing.TypedDict):
    """One thing the operator can do about a problem."""

    action: str
    """The action, phrased as something to do rather than something to know."""
    detail: typing.NotRequired[str | None]
    """Where to look, when that helps."""


class RemovedService(typing.TypedDict):
    """A service this stack used to carry, and what became of it."""

    id: str
    """The id it was declared under, which is the name an operator will look for."""
    reason: str
    """Why it went."""
    removed_in: str
    """The stack version whose catalogue stopped carrying it."""
    replaced_by: typing.NotRequired[str | None]
    """What took its place, where anything did.

    Absent is an answer and the commonest one: most things that go are not
    replaced, and a record that named the nearest surviving service to avoid an
    empty field would be pointing an operator at something that does not do the
    job they are looking for.
    """


class Repair(typing.TypedDict):
    """One repair lemonfiber could carry out."""

    check: str
    """The check whose finding this answers, as the finding names it."""
    does: str
    """What it would do, in the words the operator will read before confirming."""
    effects: list[str]
    """What else changes if it does.

    Stated before it is confirmed and never afterwards, because an effect an operator
    learns about after the fact is not something they agreed to. Empty where a repair
    touches nothing but the thing it names.
    """
    reversible: bool
    """Whether carrying it out is recorded well enough to be undone.

    A repair that cannot be reversed is still worth offering — restarting a container
    is not undoable and is usually right — but the operator confirming one deserves to
    know which kind they are agreeing to.
    """


type RepairOutcome = (
    RepairOutcomeFixed
    | RepairOutcomeFixFailed
    | RepairOutcomeStopped
    | RepairOutcomeDeclined
    | RepairOutcomeWouldOverwrite
    | RepairOutcomeUnmanaged
)
"""How a repair turned out, once the check that raised the finding has been asked again.

Deliberately not a boolean. \"It ran\" and \"it worked\" are different claims, and a model
that cannot tell them apart will eventually report the first as the second.
"""


class RepairOutcomeDeclined(typing.TypedDict):
    """Not carried out, because the operator said no."""

    outcome: typing.Literal["declined"]


class RepairOutcomeFixFailed(typing.TypedDict):
    """It ran, and the check still fails."""

    outcome: typing.Literal["fix_failed"]


class RepairOutcomeFixed(typing.TypedDict):
    """It ran, and the check now passes."""

    outcome: typing.Literal["fixed"]


class RepairOutcomeStopped(typing.TypedDict):
    """It stopped partway, leaving this.

    Named precisely rather than as \"failed\": a half-applied change is a different
    state to be in from an unchanged one, and the operator has to know which they are
    looking at before they try anything else.
    """

    leaving: str
    """What the machine is now in, said plainly."""
    outcome: typing.Literal["stopped"]


class RepairOutcomeUnmanaged(typing.TypedDict):
    """Not carried out, because the operator declared the area it would write
    unmanaged.

    Apart from [`Self::WouldOverwrite`], which is lemonfiber declining to write over
    a change it can see. This is lemonfiber obeying an instruction it was given, and
    telling somebody the first when they wrote the second would send them looking
    for a change they did not make.
    """

    outcome: typing.Literal["unmanaged"]


class RepairOutcomeWouldOverwrite(typing.TypedDict):
    """Refused, because it would have written over something changed by hand."""

    outcome: typing.Literal["would_overwrite"]


class RepairReport(typing.TypedDict):
    """What a repairing run offered, and what it did."""

    acted: bool
    """Whether this run was allowed to act at all."""
    agreement: str
    """What this offer is, so consent given for it can name which offer it read.

    Carried on every report rather than only on the ones that offer something: a
    surface that has to look for it is a surface that can fail to find it, and an
    offer of nothing is still an offer somebody may agree to nothing of.
    """
    beyond: list[Beyond]
    """What has been tried too often to keep offering.

    Said rather than passed over. A repair that quietly stopped being offered leaves
    the operator watching a fault nobody mentions any more, which is worse than being
    told plainly that this is past what lemonfiber can work out.
    """
    mended: list[Mended]
    """What was carried out, in the order it was."""
    offered: list[Repair]
    """What could be put right, whether or not it was."""
    rehearsed: bool
    """Whether this was a rehearsal: what would have happened, with none of it done.

    Said in a field of its own so that a rehearsal is never told from the real run by
    its wording alone.
    """


class ReplaceReport(typing.TypedDict):
    """What standing in place of a setup already here came to, or would come to."""

    agreement: str
    """What this offer names itself: the project and every service it would stop.

    The answer to it is this name, and nothing else is a yes to a replacement. Empty
    where there is nothing to stand in place of, because there is nothing to agree to.
    """
    project: typing.NotRequired[str | None]
    """The project that would be stood in place of."""
    refusal: typing.NotRequired[str | None]
    """Why nothing was stopped, where nothing was."""
    rehearsed: bool
    """Whether this was a rehearsal: what would have happened, with none of it done.

    Said in a field of its own so that a rehearsal is never told from the real run by
    its wording alone.
    """
    stance: Stance
    """Where the act stands."""
    still_running: list[str]
    """The services that would not stop and are still up."""
    stopped: list[str]
    """The services that were stopped."""
    would_stop: list[str]
    """The services that would be stopped, by name."""


type RequestState = typing.Literal[
    "waiting-for-approval", "declined", "failed", "getting", "partly-here", "here", "gone"
]
"""Where one request stands, in the words the person who made it would use.

Deliberately coarser than a [`crate::trace::Stage`]: a member does not need to know
that a release was grabbed but not imported, only that it is on its way. The trace is
where that detail stays, and a request names the item so it can be asked for.
"""


class Requirement(typing.TypedDict):
    """One requirement, and every release that shipped something citing it."""

    feature: str
    """The feature it belongs to, in words."""
    shipped_in: list[str]
    """Every version that shipped something citing it, newest first."""
    url: typing.NotRequired[str | None]
    """Where it is defined, unless it has since been withdrawn."""
    withdrawn: typing.NotRequired[bool]
    """Whether it was withdrawn after it shipped."""


class ResetReport(typing.TypedDict):
    """What a full reset did, or — until it is confirmed — would do: the operator edits it
    reverts back to lemonfiber's own state, and whether it was carried out or only shown.
    """

    confirmed: bool
    """Whether the reset was carried out, or only previewed pending confirmation."""
    rehearsed: bool
    """Whether this was a rehearsal: what would have happened, with none of it done.

    Said in a field of its own so that a rehearsal is never told from the real run by
    its wording alone.
    """
    reverted: list[StackEdit]
    """The operator's edits that were reverted — or, unconfirmed, that a reset would
    revert — each with the diff of what is lost against what lemonfiber restores.
    """
    reverted_connections: list[str]
    """The service connections whose drifted value was reverted to lemonfiber's — or,
    unconfirmed, would be — each named as it reads in a seed report.
    """


type Resolved = ResolvedUnlimited | ResolvedAt | ResolvedUnmeasured
"""What a limit comes to once it is weighed against a measured line."""


type RespiteStanding = RespiteStandingNone | RespiteStandingInForce | RespiteStandingExpired
"""Where a respite stands against the clock."""


class RespiteStandingExpired(typing.TypedDict):
    """It ran out, this long ago. Said once, then cleared."""

    seconds: int
    standing: typing.Literal["expired"]


class RespiteStandingInForce(typing.TypedDict):
    """In force, with this long left."""

    seconds: int
    standing: typing.Literal["in-force"]


class RespiteStandingNone(typing.TypedDict):
    """None was asked for."""

    standing: typing.Literal["none"]


class Restoration(typing.TypedDict):
    """What a restore said: what it would overwrite, and whether it did.

    The listing is present either way, and that is the point of the shape. It is not
    a separate request a surface may or may not make — it is the half of a restore
    that happens before anything is overwritten, so every answer carries it and an
    answer that overwrote nothing is one whose `done` is absent.
    """

    done: typing.NotRequired[RestoreReport | None]
    """What was put back, or nothing where nothing was."""
    rehearsed: bool
    """Whether this was a rehearsal: what would have happened, with none of it done.

    Said in a field of its own so that a rehearsal is never told from the real run by
    its wording alone.
    """
    would: Preview
    """What the archive holds and what restoring it would come to, read before
    anything was touched.
    """


class RestoreReport(typing.TypedDict):
    """What a restore did."""

    from_version: str
    """The lemonfiber version the archive was written by."""
    relocated: typing.NotRequired[Relocation | None]
    """The data root that was re-pointed, where the restore accepted one."""
    scope: Scope
    """What was restored."""


type Restraint = typing.Literal[
    "unlimited", "limited", "scheduled-active", "scheduled-quiet", "overridden", "cap-warning", "cap-exceeded"
]
"""Where the line stands."""


type Restriction = typing.Literal["unrestricted", "rating-limited", "library-limited", "both", "inconsistent"]
"""What one member is held to, in the words a household would use.

The two restrictions are one decision and two services: the media server decides
what may be *watched* and the request service what may be *asked for*. Setting one
without the other is the hole this vocabulary exists to name — a child who cannot
watch something but can pull it into the library has parents who set a limit and got
half of one.
"""


class Revealed(typing.TypedDict):
    """One stored value, handed back because the operator asked for it and said so.

    Separate from [`Held`] rather than a field on it, so that the inventory cannot
    carry a value by accident: a surface that renders the inventory has nothing to
    render, whatever it does.
    """

    name: str
    """Which credential this is."""
    value: typing.NotRequired[str | None]
    """The value, present only where the ask was confirmed."""
    warning: str
    """What the operator is told before it appears, whether or not it appears."""


class Review(typing.TypedDict):
    """A proposed change, read against what is in force, and where it stands."""

    change: ConfigChange
    """The difference, as it would be applied."""
    findings: typing.NotRequired[Findings]
    """What the change comes to on this machine, beyond the value it changes.

    Filled by whoever went and asked — the services where they file, the clients
    what they are fetching — and empty on every change that comes to nothing
    beyond its value. Carried on a staged proposal as well as an applied one: a
    review that withheld this until after the yes would be asking for a yes to
    something unstated.
    """
    proof: typing.NotRequired[Validation | None]
    """What proving the replacement credential came to, where one was proven.

    A replacement is proven against its live service before the credential it
    replaces is discarded, so this is present for exactly those settings and
    absent everywhere else.
    """
    refusal: typing.NotRequired[str | None]
    """Why nothing was written, where nothing was and the reason is not simply that
    somebody has yet to say yes.
    """
    stance: Stance
    """Where the proposal stands."""


type Revoked = typing.Literal["everywhere", "media-server-only", "nothing"]
"""How far a removal got, across the two services a household member exists on.

The media server is removed first and the request service second, because the
request service authenticates *through* the media server — so once the first is gone
they can do nothing either way, and a failure at the second leaves an account that
cannot sign in rather than somebody who can still watch.
"""


type Role = typing.Literal["data", "services"]
"""Which of the two volumes a reading is about."""


class Root(typing.TypedDict):
    """A directory everything lemonfiber keeps sits under."""

    at: str
    """The directory itself."""
    what: str
    """What lives under it, and what losing it would cost."""


class Rotation(typing.TypedDict):
    """What one rotation came to."""

    consumers: list[Propagation]
    """Every consumer, and how far the rotation reached it."""
    credential: str
    """Which credential was to be replaced."""
    settled: Settled
    """What became of the replacement."""


type Scope = ScopeWholeStack | ScopeService | ScopeExisting
"""How much of the stack a backup covers.

Whole-stack is the common case, but restoring one service is often what is
actually wanted — one \\*arr's configuration mangled while the rest is fine —
so the scope is recorded in the archive and honoured on the way back.
"""


class ScopeExisting(typing.TypedDict):
    """An existing setup's own configuration, at the host paths it keeps it in.

    The one scope whose sources are not lemonfiber's layout. A capture taken
    before a takeover has to cover the tree that is already there — lemonfiber's
    own holds nothing worth protecting until the takeover has happened — so the
    host path each tree was read from is recorded here, in the manifest, rather
    than inferred from a layout that does not describe it.

    Recording those paths is also what makes putting one back an ordinary
    extraction the operator performs deliberately, rather than something
    lemonfiber does on their behalf into a tree it does not manage.
    """

    project: str
    """The Compose project the capture was taken from."""
    scope: typing.Literal["existing"]
    trees: list[Tree]
    """The host trees captured, in the order the survey reported them."""


class ScopeService(typing.TypedDict):
    """One named service's configuration alone."""

    name: str
    """The service whose configuration this covers."""
    scope: typing.Literal["service"]


class ScopeWholeStack(typing.TypedDict):
    """Every service's configuration, plus lemonfiber's own and the stack."""

    scope: typing.Literal["whole_stack"]


class SeasonCoverage(typing.TypedDict):
    """How much of one season is actually here, and what is outstanding — the season-level
    answer, which for a series is the one an operator can act on.
    """

    have: int
    """How many of the wanted parts are here."""
    outstanding: list[Part]
    """The wanted parts that are not here yet, each carrying the stage it rests at, so
    one that stalled is told apart from one still downloading.
    """
    season: int
    """The season number. Season zero is where a service files specials."""
    unmonitored: int
    """How many parts nobody asked for — unmonitored and not on disk."""
    wanted: int
    """How many parts were asked for, or are already here — the denominator. Parts
    nobody asked for are counted separately rather than inflating this, so a season
    with every wanted episode present reads as complete even where specials are not.
    """


type Secret = str
"""A key's secret, as it is handed over once.

It has no `Debug` that prints it and no way back from its digest, and nothing here
writes it anywhere: the one reply that carries it is the only place it appears.
"""


class SeedReport(typing.TypedDict):
    """What a seed pass amounted to."""

    assessment: Assessment
    """Whether drift could be assessed, or the expected-state record was lost."""
    rehearsed: bool
    """Whether this pass only said what it would do.

    A flag rather than a second shape, because every connection above means the
    same thing either way: what the service holds is what it holds, and what
    lemonfiber would write is what it would write. What changes is that two of the
    states are reachable only here, and that the last line of the report is an
    instruction to run it for real rather than to run it again.
    """
    unsupported: typing.NotRequired[list[UnsupportedReport]]
    """Services this pass could not wire because it cannot speak to them, each with
    why.

    Not wirings, because nothing was attempted and a wiring says how an attempt
    turned out. Not absences either, which is the point: a pass that skipped a
    service declaring an API shape this build does not speak and said nothing would
    leave the operator who wrote that declaration no way to tell it from a service
    lemonfiber had simply forgotten.
    """
    wirings: list[Wiring]
    """Every connection attempted, and how each turned out."""


type SeedSeverity = SeedSeverityInformational | SeedSeverityWarning
"""How serious a reported connection is.

Drift is normal and usually the operator's own harmless edit, so it is reported
as information rather than a failure. It escalates to a warning only when the
drift breaks the stack — a root folder pointing where nothing exists, a download
client that no longer answers — and a warning that cannot be acted on is noise,
so a warning always names both what broke and what to do about it.
"""


class SeedSeverityInformational(typing.TypedDict):
    """Nothing is broken: the connection is settled, or its drift is the operator's
    own edit that still works.
    """

    severity: typing.Literal["informational"]


class SeedSeverityWarning(typing.TypedDict):
    """The connection breaks the stack. Both the breakage and a remediation are
    named, because a warning the operator cannot act on is noise.
    """

    breakage: str
    """What is broken, in the operator's terms."""
    remediation: str
    """What to do about it."""
    severity: typing.Literal["warning"]


type SeedState = (
    SeedStateWired
    | SeedStateAlreadyWired
    | SeedStateDrifted
    | SeedStateStale
    | SeedStateConflicted
    | SeedStateAdopted
    | SeedStateUnmanaged
    | SeedStateWouldWire
    | SeedStateWouldAdopt
    | SeedStateObserved
    | SeedStateUnmatched
    | SeedStateSkipped
    | SeedStateFailed
    | SeedStateRefused
)
"""How one connection turned out after a seed pass."""


class SeedStateAdopted(typing.TypedDict):
    """An operator's edit adopted as the accepted state, kept across seeds and
    restores. Settled: lemonfiber leaves it as it is.
    """

    state: typing.Literal["adopted"]


class SeedStateAlreadyWired(typing.TypedDict):
    """Present and correct; nothing was done."""

    state: typing.Literal["already-wired"]


class SeedStateConflicted(typing.TypedDict):
    """Both the service's value and lemonfiber's intent moved away from the
    baseline. The conflict is presented — the value the operator set beside the
    one lemonfiber would write — and the value left as it is; lemonfiber does not
    resolve it on its own.

    Both values are shown in the report and serialized with it, so a
    secret-bearing field must not report a conflict through this variant: a
    conflict in a secret is to be reported without either value on show, and
    wants a masked shape of its own rather than this one.
    """

    ours: str
    """The value lemonfiber would write in its place."""
    state: typing.Literal["conflicted"]
    yours: typing.NotRequired[str | None]
    """The value the service now holds, as the operator set it; `None` where
    they cleared it.
    """


class SeedStateDrifted(typing.TypedDict):
    """Present but operator-changed; preserved."""

    state: typing.Literal["drifted"]


class SeedStateFailed(typing.TypedDict):
    """Attempted and rejected, carrying the service's own words."""

    detail: str
    """What the service said."""
    state: typing.Literal["failed"]


class SeedStateObserved(typing.TypedDict):
    """An area the operator declared unmanaged. Nothing was read from the service and
    nothing was written to it, and the reason they gave is carried so a report says
    whose decision it was.

    Apart from [`Self::Unmanaged`], which lemonfiber *infers* from a value it has
    no record of having written, and which it adopts as the baseline so that later
    runs recognise it. This one is a decision somebody wrote down, and it holds
    whether or not lemonfiber would have had anything to say — nothing is adopted,
    because adopting would be the first half of managing it again.
    """

    reason: str
    """Why the operator said to leave it alone, in their own words."""
    state: typing.Literal["observed"]


class SeedStateRefused(typing.TypedDict):
    """Refused by lemonfiber's own policy, carrying the reason a re-run will not
    resolve — such as two \\*arrs pointed at one root folder, or a service that
    does not serve the API version this build speaks. Either way nothing it
    names was written, whether it was refused before the write or the write
    itself found nothing to land in.
    """

    reason: str
    """Why it was refused, in lemonfiber's own words."""
    state: typing.Literal["refused"]


class SeedStateSkipped(typing.TypedDict):
    """Prerequisite unavailable; a later run will complete it."""

    reason: str
    """Why it could not be attempted."""
    state: typing.Literal["skipped"]


class SeedStateStale(typing.TypedDict):
    """Present and still lemonfiber's own value, but behind lemonfiber's intent —
    it should be brought up to date. Reported until an update path applies it,
    and never overwritten in the meantime.
    """

    state: typing.Literal["stale"]


class SeedStateUnmanaged(typing.TypedDict):
    """A value the service already held that lemonfiber never wrote — the operator's
    own, pre-existing. Adopted as the baseline this run rather than reported as
    drift, so an existing setup is taken on instead of flagged wholesale. Its
    value is not shown, so a secret among the adopted is never put on display.
    """

    state: typing.Literal["unmanaged"]


class SeedStateUnmatched(typing.TypedDict):
    """Something on this machine fills what a service asks for, and nothing lemonfiber
    does connects the two — the filler names no adapter, or none lemonfiber pairs with
    what the asker speaks.

    Settled, because no run changes it: the stack, or what is installed, has to. Said
    rather than left out, because a filler nothing reaches and a filler lemonfiber
    forgot would otherwise read the same, and the operator who installed one to stand
    in for another is the one who needs to know which.
    """

    reason: str
    """What fills it, what asked, and why nothing connects them."""
    state: typing.Literal["unmatched"]


class SeedStateWired(typing.TypedDict):
    """Written and read back."""

    state: typing.Literal["wired"]


class SeedStateWouldAdopt(typing.TypedDict):
    """An operator's own value a real run would take on as the accepted state, and
    this one did not.

    Apart from [`Self::WouldWire`] because it is the other direction: nothing would
    be written to the service at all, and what would move is lemonfiber's record of
    what it expects. Its value is not shown, exactly as [`Self::Unmanaged`] does not
    show one, so a secret among the adopted is never put on display by a question.
    """

    state: typing.Literal["would-adopt"]


class SeedStateWouldWire(typing.TypedDict):
    """Not there, or not at what lemonfiber would have it be, and this run only said
    so.

    The one outcome a pass that writes nothing can reach where a pass that writes
    would have written. What a real run would leave the service holding sits beside
    what it holds now, because a report saying a connection would be made without
    saying what it would be made *to* is a count rather than an account — and a
    count is what an operator asking for a rehearsal already has.

    Both values are serialized, so a secret-bearing field must not report through
    this variant carrying one. It does not have to: `ours` is absent exactly where
    a real run would generate the value rather than read it, which is the only
    place a credential arises — the torrent client's web UI password and the media
    server's admin account. A value minted to describe a rehearsal is a secret that
    exists because somebody asked a question, and it would then have to be kept or
    thrown away.

    `yours` is absent where the service holds nothing, and where this run could not
    ask without writing — reading the household's telling means signing in as the
    owner, and a session is state on somebody else's service.
    """

    ours: typing.NotRequired[str | None]
    """What a real run would leave it holding, or `None` where that value would be
    generated rather than read.
    """
    state: typing.Literal["would-wire"]
    yours: typing.NotRequired[str | None]
    """What the service holds now, or `None` where it holds nothing or could not
    be asked.
    """


type SeedingStanding = SeedingStandingNeverImported | SeedingStandingSeeding | SeedingStandingLeftAlone
"""Where one completed download stands."""


class SeedingStandingLeftAlone(typing.TypedDict):
    """The operator asked for this one to be left alone."""

    standing: typing.Literal["left_alone"]


class SeedingStandingNeverImported(typing.TypedDict):
    """Nothing ever linked it into a library: it was never imported, and removing
    it loses nothing.
    """

    standing: typing.Literal["never_imported"]


class SeedingStandingSeeding(typing.TypedDict):
    """It was imported and is still seeding, so removing it has a consequence
    outside this machine.
    """

    ratio: int
    """What it has uploaded against what it downloaded, in hundredths, as the
    client reports it.

    A whole number rather than a fraction because every report this product
    makes is compared for equality somewhere, and a fraction cannot be —
    two figures a client would call the same would not be. The hundredth is
    finer than any decision made on a ratio.
    """
    standing: typing.Literal["seeding"]


type SelfUpdateStanding = typing.Literal["current", "update-available", "managed-externally", "check-failed"]
"""Where a copy of lemonfiber stands, in the words the specification uses.

Nothing known is the default, and it is the right one: a report built before
anything has been read has not established that this copy is current, and a
default that said so would be a claim made by an empty value.
"""


class Service(typing.TypedDict):
    """One service, as it stands."""

    criticality: Criticality
    """How much its absence costs, so a summary can weigh it."""
    depends_on: list[str]
    """The services it needs before it can work, as the manifest declares them.
    Carried so a failure can be attributed to the thing underneath it rather
    than counted as one more independent thing wrong.
    """
    describes: str
    """What it does for the operator, in the stack's own words.

    Carried on the service rather than looked up where it is shown, because this
    is the one struct every surface reads: a listing, the machine-readable reply,
    the web API and the terminal's panel all render this, and a description
    fetched separately by each of them would be four chances to render three.

    The stack's words rather than lemonfiber's, for the reason its absence cost is:
    a stack that adds a service should not need a lemonfiber release before it can
    say what that service is for.
    """
    exit: typing.NotRequired[int | None]
    """How it exited, where it has exited."""
    forms: list[str]
    """Every form it is running for, in the order the stack declares them.

    All of them rather than one, because a service two forms share is there for
    both, and stopping one of them leaves it running for the other. Empty where no
    form it belongs to is up: a service nobody's form holds is not missing from one.
    """
    id: str
    """The service's identifier, which is also its Compose service name."""
    name: str
    """What it is called in front of an operator."""
    profile: str
    """The profile that declared it."""
    state: ServiceState
    """What it is doing."""


class ServiceProvenance(typing.TypedDict):
    """Where one service comes from, as the stack declares it."""

    digest: typing.NotRequired[str | None]
    """The digest of the image that runs, where the stack names one.

    Beside the tag rather than instead of it: the tag is the version somebody reads,
    and the digest is the one image that version was when it was pinned, which is
    what is pulled and what somebody verifies against the registry.
    """
    id: str
    """The service's id, which is also its Compose service name."""
    image: str
    """The image it runs, without a tag."""
    license: str
    """The SPDX identifier of the licence it is published under.

    Stated rather than summarised as *open source*, because the identifier is what
    somebody checks against the project — and because the four in this stack are
    not interchangeable to anybody deciding what to do with what they run.
    """
    name: str
    """What it is called in front of an operator."""
    pinned: str
    """The exact tag this stack pins it at.

    Kept apart from the image rather than written as one reference, so that a
    caller comparing what is pinned against what a project has released is
    comparing versions rather than parsing them out of a string. The two are
    printed together for a person, because a version without the image it belongs
    to names nothing that can be fetched.
    """
    upstream: str
    """The project it is built from.

    The whole point of the entry for anybody verifying: the licence is a string
    this stack wrote down, and this is where somebody goes to find out whether the
    project still agrees with it.
    """


type ServiceState = typing.Literal[
    "failed",
    "crash-looping",
    "unhealthy",
    "absent",
    "stopped",
    "starting",
    "running",
    "healthy",
    "host-managed",
]
"""What one service is actually doing.

Ordered from worst to best, so a form's condition is the minimum across its
services and needs no comparison table. The declaration order is therefore
load-bearing.
"""


class SettingReport(typing.TypedDict):
    """One setting, as it is safe to show."""

    key: str
    """The setting's name."""
    origin: ValueOrigin
    """Where the value came from, beside the value rather than behind a second
    request — reading a setting and reading what put it there are one act.
    """
    secret: bool
    """Whether the value was withheld."""
    value: str
    """Its value, or a note that it is set and withheld."""


type Settled = (
    SettledReplaced
    | SettledRefused
    | SettledUnproven
    | SettledReplacedUnproven
    | SettledRehearsed
    | SettledUnknown
    | SettledElsewhere
)
"""What became of a rotation."""


class SettledElsewhere(typing.TypedDict):
    """A replacement for this one does not come from here.

    Either the operator's provider issued it, in which case inventing one would
    produce a credential no service has ever heard of; or the service that holds
    it offers no way to change it in place. Either way what is owed is a
    sentence saying where a replacement does come from, not an attempt.
    """

    detail: str
    """Where a replacement comes from, and what to do once it exists."""
    settled: typing.Literal["elsewhere"]


class SettledRefused(typing.TypedDict):
    """The service answered and refused the replacement. Nothing was changed."""

    detail: str
    """What the service said, with any credential in it withheld."""
    settled: typing.Literal["refused"]


class SettledRehearsed(typing.TypedDict):
    """Nothing was attempted, because this run only said what a rotation would do.

    Its own outcome rather than one of the refusals above, because it is not a
    refusal: nothing went wrong, and what an operator is being told is what would
    happen if they ran it again meaning it. Carrying its own three fields rather
    than one sentence, because \"it would rotate the qBittorrent password\" is not a
    report — where the value lives is what would be written over, and what is owed
    afterwards is the half nobody finds out about until a consumer stops working.

    No value appears here and none is generated to put here. A replacement minted
    to describe a rotation is a secret that exists because somebody asked a
    question, and it would then have to be kept or thrown away — and one thrown
    away may be one the service has already taken.
    """

    afterwards: list[str]
    """What would still need doing before every consumer held the replacement."""
    detail: str
    """What a real run would do, step by step, in lemonfiber's own words."""
    location: str
    """Where the value that would be replaced is kept."""
    settled: typing.Literal["rehearsed"]


class SettledReplaced(typing.TypedDict):
    """The replacement was proven and is now the value in force."""

    observed: str
    """What the service did while proving it — an observation, never the value."""
    settled: typing.Literal["replaced"]


class SettledReplacedUnproven(typing.TypedDict):
    """The service replaced the credential itself, and the replacement did not answer.

    The one way of not landing that keeps nothing: a service asked to replace its
    own key drops the old one the moment it makes the new one, so there is no order
    that proves first. What is owed is the command that hands the new one out once
    the service answers.
    """

    detail: str
    """What did not answer, and what to run once it does."""
    settled: typing.Literal["replaced-unproven"]


class SettledUnknown(typing.TypedDict):
    """Nothing in this stack holds a credential by that name."""

    known: list[str]
    """The names that would have been accepted."""
    settled: typing.Literal["unknown"]


class SettledUnproven(typing.TypedDict):
    """Nothing usable answered, so the replacement could not be proven. Nothing
    was changed, because an unproven replacement is not a better one.
    """

    detail: str
    """Why nothing could be concluded."""
    settled: typing.Literal["unproven"]


type SetupOutcome = typing.Literal["applied", "abandoned", "already-set-up"]
"""How a setup run ended."""


class SetupReport(typing.TypedDict):
    """What a setup run came to, and what it settled on.

    **Deliberately not the settings themselves.** Setup writes an indexer key and a
    service password among them, and a report a script can read is a report a script
    can log — into a file, a CI transcript, somebody's terminal history. So this says
    what was *decided* and never what was *entered*, and the fields are chosen one at
    a time rather than by serialising a struct that might later gain a secret.

    The indexer's address is left out for that reason rather than because it is
    itself a secret: it is entered beside its key, and the two travel together in
    every place an operator copies them from.
    """

    data_root: typing.NotRequired[str | None]
    """Where the library was put, where a location was chosen."""
    outcome: SetupOutcome
    """How the run ended."""
    protocols: Protocols
    """Which ways of downloading the stack was set up for."""
    service_user: typing.NotRequired[str | None]
    """The user the services run as, as `uid:gid`, where one was set."""


type Shape = typing.Literal["pipeline", "library-only"]
"""Which walkthrough this stack is offered."""


class Sharing(typing.TypedDict):
    """How the line is shared, and what that costs."""

    acting: typing.NotRequired[str | None]
    """What a spent cap is doing to the figures above, where one is spent."""
    applied: bool
    """Whether this run wrote the limits to the clients or only read them."""
    cap: typing.NotRequired[Cap | None]
    """The monthly cap, where one was declared."""
    capacity: typing.NotRequired[Capacity | None]
    """What the line was measured to carry."""
    cautions: list[str]
    """What is worth knowing about that reading before trusting it."""
    clients: list[Holding]
    """What each download client was asked and what it is doing about it."""
    down: BandwidthReading
    """The download limit."""
    means: str
    """What that means for the household."""
    metered: typing.NotRequired[Metered | None]
    """What the stack itself moved this month."""
    ratio: typing.NotRequired[str | None]
    """What throttling the upload costs, where an upload limit is in force."""
    reached: typing.NotRequired[Reached | None]
    """Where the month stands against it."""
    rehearsed: bool
    """Whether this was a rehearsal: what would have happened, with none of it done.

    Said in a field of its own so that a rehearsal is never told from the real run by
    its wording alone.
    """
    respite: RespiteStanding
    """The override, where one is running or has just run out."""
    respite_says: typing.NotRequired[str | None]
    """What the override amounts to, in words."""
    restraint: Restraint
    """Where the line stands."""
    rhythm: typing.NotRequired[Rhythm | None]
    """The household's hours, where any were declared."""
    untouched: list[str]
    """What is outside every limit here."""
    up: BandwidthReading
    """The upload limit, which is declared apart and defaults lower."""
    zone: typing.NotRequired[str | None]
    """The zone the clients read those hours in, where the stack says."""


class Snapshot(typing.TypedDict):
    """Everything the dashboard shows at one moment.

    Each source's panel is filled or marked unavailable on its own, so one dead
    source degrades one region rather than the screen. The surface builds this from
    what it gathered; the standing is read from the same facts so it cannot
    disagree with the panels.
    """

    alerts: list[Alert]
    """What the operator has been told, newest first: what is owed them where a
    channel is refusing, then what has already been said.
    """
    door: PanelFrontDoorReport
    """The one address to hand somebody who lives here.

    On the screen rather than only behind a question, because the operator who
    needs it is not the one who thought to ask: they have just been asked \"what
    do I open?\" by somebody in the next room. Built from the same reading as the
    panels beside it, so the screen and `front-door` cannot name different doors.
    """
    health: HealthSummary
    """The one-line health summary — the same computation every other surface
    uses, so no two of them can grade the same stack differently.

    Always present, unlike the panels: a stack that could not be reached has a
    summary, and it says `unknown`. An absent summary would leave the operator
    to infer health from a blank space, which is the one reading this must never
    be open to.
    """
    household: PanelHouseholdReport
    """What the household has asked for that is not moving.

    On the screen rather than only behind a question, for the reason the door
    beside it is: a request waiting on a decision or failed after one is waiting
    on the operator, and an operator who has to think to ask is one who finds out
    when somebody comes to complain.
    """
    queue: PanelArray_of_Queue
    """The per-service queues."""
    services: PanelArray_of_Service
    """Every service and what it is doing."""
    storage: PanelStorage
    """The storage picture."""
    stuck: list[Stuck]
    """What in the pipeline has stopped, worst first — assessed across the
    download clients and the \\*arrs together, because the failure that matters
    most is invisible inside either.
    """
    telemetry: Telemetry
    """Whether the screen itself can be trusted to be current."""
    transfers: PanelArray_of_Transfer
    """The active transfers."""
    vpn: typing.NotRequired[PanelVpn | None]
    """The VPN, or `None` where no VPN is configured and the panel is omitted
    rather than shown permanently red.
    """


type Sort = typing.Literal["container", "network", "image", "path"]
"""What sort of thing one line of a manifest is."""


type Source = typing.Literal["declared", "observed"]
"""Where a figure for the line came from."""


type SpaceCategory = (
    SpaceCategoryTree
    | SpaceCategoryLanding
    | SpaceCategorySeeding
    | SpaceCategoryOrphaned
    | SpaceCategoryExtracted
    | SpaceCategoryServices
    | SpaceCategoryUnmanaged
)
"""What one line of the accounting is about."""


class SpaceCategoryExtracted(typing.TypedDict):
    """Archives whose extracted contents sit beside them."""

    of: typing.Literal["extracted"]


class SpaceCategoryLanding(typing.TypedDict):
    """What the download clients still have to write."""

    of: typing.Literal["landing"]


class SpaceCategoryOrphaned(typing.TypedDict):
    """Downloads on disk that no service ever took."""

    of: typing.Literal["orphaned"]


class SpaceCategorySeeding(typing.TypedDict):
    """Completed downloads the client is still seeding."""

    of: typing.Literal["seeding"]


class SpaceCategoryServices(typing.TypedDict):
    """The services' own configuration and databases."""

    of: typing.Literal["services"]


class SpaceCategoryTree(typing.TypedDict):
    """One directory beneath the data root, named as the operator named it.

    Per directory rather than one figure for the library, because several
    libraries commonly share a volume and \"the library is large\" tells nobody
    which of them is growing.
    """

    name: str
    of: typing.Literal["tree"]


class SpaceCategoryUnmanaged(typing.TypedDict):
    """What the operator said to leave alone."""

    of: typing.Literal["unmanaged"]


class SpaceLeft(typing.TypedDict):
    """Something a cleanup could not take."""

    at: str
    """Where it is."""
    why: str
    """What the platform said, verbatim."""


class StackEdit(typing.TypedDict):
    """A stack file the operator edited, preserved rather than overwritten, with the
    change an upgrade would make shown against it.
    """

    diff: str
    """The lines that differ between the operator's file and what lemonfiber would
    write — theirs marked `-`, lemonfiber's `+`, the matching head and tail left
    out. Empty where the two differ only in ways `lines` does not see.
    """
    path: str
    """The file's path within the stack directory."""


type StackProtocol = typing.Literal["usenet", "torrent"]
"""A download provider a profile can depend on.

Serialisable as well as readable, for the same reason [`Criticality`] is: it
reaches an operator. A profile left out of a closure is only half reported
without the provider it wanted.
"""


class StackUpdateReport(typing.TypedDict):
    """What updating the stack would change, or what a run of it came to."""

    applied: list[UpdateApplied]
    """What became of each service the run reached, in the order it reached them."""
    backup: typing.NotRequired[str | None]
    """Where the backup taken before anything moved was written."""
    changelog: Notes
    """What the release that brought these pins changed.

    The stack this would move to is the one this build carries, and the release
    that carried this build is what says why it moved. An operator weighing a
    stack update is weighing that, and being shown only which image numbers go up
    is being shown the arithmetic rather than the reason.
    """
    changes: list[UpdateChange]
    """What would move, and what taking each step means."""
    confirmed: bool
    """Whether the steps were agreed to, or only shown."""
    halted: typing.NotRequired[str | None]
    """Why the stack is not as the run found it, where it is not.

    Two runs end that way and an operator has the same thing to do about either:
    one that met a service which would not come back and stopped there, and one
    where every step succeeded and the stack would not start again afterwards.
    The second is not a failure of the update — `state` still says `Updated`,
    because it is — but the stack came down for the capture and something has to
    say that it is still down.
    """
    in_flight: list[str]
    """What the download clients are still working on, named so an operator can
    tell whether the thing they have been waiting for is among them.
    """
    rehearsed: bool
    """Whether this was a rehearsal: what would have happened, with none of it done.

    Said in a field of its own so that a rehearsal is never told from the real run by
    its wording alone.
    """
    stack_edits: list[StackEdit]
    """Stack files the operator had edited, left as they set them rather than
    overwritten with this build's own, each with the change that was held back.
    """
    state: UpdateState
    """The one word the run comes to."""


type Stage = typing.Literal[
    "not-monitored",
    "monitored",
    "searching",
    "found",
    "grabbed",
    "downloading",
    "downloaded",
    "importing",
    "imported",
    "available",
]
"""A stage in an item's journey, ordered from \"nobody asked for it\" to \"playable\". The
declaration order is the pipeline order, so one stage compares less than a later one.
"""


type Stall = typing.Literal[
    "redownload-loop",
    "repeated-import-failure",
    "completed-not-imported",
    "orphaned",
    "stalled-download",
    "waiting-indefinitely",
    "slow",
]
"""Why an item is not moving.

Ordered by how much of the operator's attention each deserves, worst first, so
a summary that leads with the worst category needs no second ranking.
"""


type Stance = typing.Literal["unchanged", "pending", "blocked", "applied"]
"""Where a proposed change stands once it has been read against what is in force."""


class StandingReport(typing.TypedDict):
    """One Compose project on this machine that is not lemonfiber's."""

    project: str
    """The Compose project name."""
    services: list[OccupantReport]
    """Its containers, by service name."""


class Started(typing.TypedDict):
    """Work that outlives the request that started it: its name, and what it was.

    The action is carried beside the name because a client holding several has to
    tell them apart, and asking it to remember which name it gave which request is
    asking it to keep a second copy of what this already knows.
    """

    action: str
    """The action that was asked for, as it was named."""
    job: str
    """The name to ask what became of this work by."""


class StatusReport(typing.TypedDict):
    """What each service is doing, and what that adds up to."""

    active_forms: list[str]
    """The forms the running services are up for, in the order the stack declares them.

    Read from the whole stack whichever forms were asked about. A form counts while
    every service it holds has been started and none has been stopped, and one
    wholly inside a broader form that counts is left out. Each service names the ones
    it is running for.
    """
    condition: Condition
    """What the services amount to, as one word.

    For the whole stack, counted over what the active forms hold and whatever else
    is there, so a stack running part of itself on purpose reads as active. With no
    form up, and for the forms asked about, counted over every service listed.
    """
    disturbs: Disturbances
    """How long each way of acting on these services takes them away for.

    Here so that a surface can say it before it asks the operator to confirm,
    which is the only moment saying it is any use.
    """
    filtered: list[Filtered]
    """What those forms left out for want of a configured provider, service by service.

    Beside the services rather than among them: a service filtered out is the
    configuration being honoured, not a service that did not start.
    """
    forms: list[str]
    """The forms asked about; empty means the whole stack was."""
    services: list[Service]
    """Each service, worst first.

    A service the active forms filtered out is listed only while it is there; one
    that is not is in `filtered` and nowhere else.
    """
    undeclared: list[Undeclared]
    """The containers running under this project that the stack never declared.

    Kept apart from the services rather than mixed in with them, because what is
    known about each is different: a service has a profile, a criticality and a
    description, and one of these has a name and a state and nothing else. Shown
    all the same — something running under this project's name that lemonfiber did
    not put there is the operator's business whether or not lemonfiber understands
    it.
    """
    unsupported: typing.NotRequired[list[UnsupportedReport]]
    """Services that are running and operable like any other, and that lemonfiber
    cannot offer the features needing to know what they are — each with why.

    Empty for the stack this build ships. It fills in for a stack the operator
    maintains, where a declaration can name an API and leave out the part that
    makes it addressable: such a service starts, stops and reports its state
    exactly as the others do, and every feature that would have spoken to it used
    to do nothing and say nothing. Here rather than on the service's own row,
    because it is a statement about what this build can do rather than about how
    the service is faring.
    """


class Stopped(typing.TypedDict):
    """A walkthrough that stopped: where, why, what the services were saying, and what to do."""

    logs: list[str]
    """What the services involved were saying at the time, shown inline rather than left
    for the operator to go and find — a fault report they have to research is a fault
    report they abandon.
    """
    reason: Reason
    """Why."""
    remedy: str
    """The one thing to try."""
    step: WalkthroughStep
    """The step it stopped at."""


class Storage(typing.TypedDict):
    """The storage picture: what is free, when it runs out, and whether imports link."""

    exhaustion: typing.NotRequired[Duration | None]
    """The time until the disk fills at the current rate of the queue draining
    onto it, or `None` where it is not projected to fill.
    """
    free: DashboardReading
    """Bytes free on the data volume — a [`Reading`], since a volume that could
    not be read this refresh must not render as zero free.
    """
    hardlink: Hardlink
    """Whether imports are linking or copying."""


class Stored(typing.TypedDict):
    """Everything lemonfiber keeps on this machine, and what became of it."""

    beside: list[StoredBeside]
    """What is on this machine that is not lemonfiber's to keep or remove."""
    kept: list[Kept]
    """Each thing kept, configuration first and then what can be made again."""
    rehearsed: bool
    """Whether this was a rehearsal: what would have happened, with none of it done.

    Said in a field of its own so that a rehearsal is never told from the real run by
    its wording alone.
    """
    removal: StoredRemoval
    """Whether this run removed any of it."""
    roots: list[Root]
    """The two directories all of it lives under."""


class StoredBeside(typing.TypedDict):
    """Something on this machine that lemonfiber neither keeps nor removes."""

    what: str
    """What it is."""
    why: str
    """Whose it is, and why it is not lemonfiber's to take away."""


class StoredLeft(typing.TypedDict):
    """Something a removal could not take away."""

    at: str
    """The path that is still there."""
    why: str
    """What the machine said about it, so it can be finished by hand."""


type StoredRemoval = StoredRemovalNotAsked | StoredRemovalUnconfirmed | StoredRemovalDone
"""Whether anything was removed on this run, and what became of it."""


class StoredRemovalDone(typing.TypedDict):
    """Carried out."""

    gone: list[str]
    """The directories that are gone."""
    left: list[StoredLeft]
    """What could not be removed, each with the reason."""
    state: typing.Literal["done"]


class StoredRemovalNotAsked(typing.TypedDict):
    """Nobody asked. This is a listing."""

    state: typing.Literal["not-asked"]


class StoredRemovalUnconfirmed(typing.TypedDict):
    """Asked for without the agreement it takes, so nothing was touched."""

    state: typing.Literal["unconfirmed"]


class Straining(typing.TypedDict):
    """Why playback here is likely to struggle, whatever app the household installs.

    Present only where the preset in force asks for transcoding this platform cannot
    do in hardware. It belongs to the guidance rather than to any one device: the
    preset and the platform decide it between them, and every device in the table
    meets it.
    """

    caution: str
    """What that preset asks of this machine, and what playback does where this
    machine cannot give it.
    """
    instead: str
    """What makes it stop."""
    preset: str
    """The preset in force, under the name it was chosen by."""


type Stream = typing.Literal["stdout", "stderr"]
"""Which stream a log line arrived on."""


class Stuck(typing.TypedDict):
    """One thing that is wrong, and why."""

    blocking: typing.NotRequired[str | None]
    """What the service said was blocking it, in its own words, where it said
    anything. A permission denial from an import log is worth more than any
    interpretation of it, and it is the difference between \"stuck\" and
    something an operator can fix.
    """
    held_for: int
    """How long it has been that way, in seconds — what turns \"stuck\" into a
    sentence an operator can weigh.
    """
    items: int
    """How many items this stands for. One in the ordinary case; more where they
    share a cause and the cause is what is wrong — twenty downloads stopped by
    a full disk are one thing to fix, and twenty alerts about it are how an
    operator learns to mute the queue check.
    """
    name: str
    """Which item — or, where several share one cause, that cause."""
    stall: Stall
    """What is wrong with it."""


class StuckEntry(typing.TypedDict):
    """One stuck item queue health found, named so it links straight to its own trace."""

    service: str
    """The \\*arr whose queue is holding it."""
    stage: Stage
    """The stage its download is stuck at."""
    title: str
    """The item's title — the term a `trace` searches by."""


class StuckReport(typing.TypedDict):
    """The items whose downloads are stuck, across the \\*arrs — the landing point for \"N
    items stuck\" that queue health reports, each entry naming the item so the operator
    goes straight to its per-item trace rather than to a count to investigate.
    """

    incomplete: bool
    """Whether an \\*arr's queue could not be read, so the list may be short — reported
    rather than read as \"nothing stuck\", the same honesty a trace keeps.
    """
    items: list[StuckEntry]
    """The stuck items, each linkable to its trace."""
    unsupported: typing.NotRequired[list[UnsupportedReport]]
    """Services whose queue lemonfiber cannot read at all, each with why.

    Apart from [`Self::incomplete`], which is a queue that was asked and would not
    answer. This is a queue that was never asked, because the service declares an
    API shape this build does not speak or a Servarr declaration it cannot reach
    through — and a reading that dropped those would be as short as an unreadable
    queue makes it, without the sentence that says so.
    """


class Substitution(typing.TypedDict):
    """One service standing in for another, worked out before anything is written."""

    asked_by: list[str]
    """Every service that asks for it, so the reach of the change is visible."""
    capability: str
    """The capability whose filler changes."""
    leaves_unfilled: list[Unfilled]
    """What this would leave with nothing filling it, each naming what asked.

    The one thing an operator cannot find out afterwards. A service filling two
    capabilities is replaced for one of them, and the other stops being filled —
    which is a working stack becoming a broken one, on a change that reads as
    swapping like for like.
    """
    now: str
    """What would fill it."""
    setting: str
    """The setting the change writes."""
    was: typing.NotRequired[str | None]
    """What fills it now, where anything does."""
    why: typing.NotRequired[str | None]
    """What the operator said about the choice, where they said anything.

    Read back as the choice's own `why` wherever the choice is read, and absent
    where nothing was said: nothing supplies a reason on the operator's behalf.
    """


class SubstitutionReport(typing.TypedDict):
    """What substituting one service for another would come to."""

    agreement: str
    """What this reading names itself, so a choice answering it can say which reading
    it answered.

    Named part by part — the choice itself, what fills the capability now, what asks
    for it, and what the change would leave unfilled — so a choice refused because the
    wiring moved is told which of those moved.
    """
    applied: bool
    """Whether it was written, or only worked out.

    A run that only says what it would do writes nothing and reports the same
    answer, so the two are told apart here rather than by the caller remembering
    which flags it passed.
    """
    rehearsed: bool
    """Whether this was a rehearsal: what would have happened, with none of it done.

    Said in a field of its own so that a rehearsal is never told from the real run by
    its wording alone.
    """
    substitution: Substitution
    """The change itself, and what it would leave with nothing filling it."""


class SupervisionReport(typing.TypedDict):
    """What a watch saw, once the data root it was guarding was lost."""

    forms: list[str]
    """The forms that were being watched, and are now stopped."""
    reason: str
    """Why the watch ended: the data root vanished, or a different volume took
    its place — or, on a run that only said what a watch would do, that nothing
    was watched at all.
    """
    rehearsed: bool
    """Whether this was a rehearsal: what would have happened, with none of it done.

    Said in a field of its own so that a rehearsal is never told from the real run by
    its wording alone.
    """
    stopped: bool
    """Whether stopping the services succeeded."""
    would: typing.NotRequired[Vigil | None]
    """The watch this run would have kept, where it only said what it would do.

    A guard is the one command with no ending of its own, so a rehearsal of it
    cannot be the command with its last step left out — it would hold until the
    drive was pulled. What it answers with is this instead, and the fields above
    then describe a watch that never began: nothing ended, and nothing was
    stopped. Absent on every watch that actually ran.
    """


type Support = typing.Literal["good", "workable", "poor", "fallback"]
"""How well a device is served."""


class Switched(typing.TypedDict):
    """What narrowing the active set moved.

    Three lists rather than a before and an after, because the operator's question
    is not \"what is running now\" — they can ask that — but \"what did that do\". The
    middle list is the one that makes the verb worth having: it is the promise that
    a download in flight was not interrupted to change the shape of the stack
    around it.
    """

    kept: list[str]
    """Left running: the new closure holds them too, so nothing here asked them to
    stop. Not a promise that nothing touched them — Compose recreates a container
    whose configuration changed — but a promise that narrowing did not.
    """
    started: list[str]
    """Started, because the new closure holds them and they were not up."""
    stop_command: typing.NotRequired[list[str] | None]
    """The exact Compose invocation that stopped what fell outside, so a switch is
    no more a matter of trust than any other action. Absent where nothing had
    to stop.
    """
    stopped: list[str]
    """Stopped, because the new closure does not hold them."""


class Taken(typing.TypedDict):
    """What a reader needs to know before reading a word of the bundle.

    An operator pasting last week's bundle into this week's thread is the commonest way one
    of those threads goes wrong, and nothing in the contents tells either of them.
    """

    at: str
    """When, as a service writes a moment."""
    lemonfiber: str
    """The lemonfiber that wrote it."""
    stack: str
    """The stack it was written from."""


type TakesAway = TakesAwayBounded | TakesAwayOpenEnded
"""How long one way of acting on the stack takes something away for.

Two cases rather than a length and a flag, because *no bound* is not a long
bound and a surface offered a number plus a \"really, though?\" beside it will
show the number. A reader that handles both arms has said both things; one
that handles only the first does not compile.
"""


class TakesAwayBounded(typing.TypedDict):
    """It ends, and this is the longest the run is held to."""

    bound: typing.Literal["bounded"]
    seconds: int
    """The length, in seconds.

    Seconds rather than the engine's own duration shape, because every
    caller of this turns it into a sentence and none of them wants
    nanoseconds to do it.
    """


class TakesAwayOpenEnded(typing.TypedDict):
    """Nothing bounds it, and this is what it is waiting for."""

    bound: typing.Literal["open-ended"]
    until: Awaiting
    """What has to happen before it ends."""


class Tally(typing.TypedDict):
    """What a set of files occupies, counted both ways."""

    files: int
    """How many names were counted."""
    logical: int
    """The bytes the names add up to — what this would take with nothing shared."""
    physical: int
    """The bytes the underlying files add up to — what the volume has actually
    lost to them.
    """
    shared: int
    """How many of those names pointed at a file already counted."""


type Telemetry = typing.Literal["live", "degraded", "disconnected", "no-stack", "unconfigured"]
"""How the screen itself is doing, which is a different question from how the
stack is doing.

The stack's own verdict is [`crate::health::Standing`]; this is only whether the
picture can be trusted to be current. Kept apart because they disagree in both
directions: a healthy stack can be shown through half-failing telemetry, and a
perfectly refreshing screen can be reporting a stack that is on fire.
"""


class Term(typing.TypedDict):
    """A word this product uses, and what somebody meeting it needs to know."""

    also_called: list[str]
    """What other services in this stack call the same thing.

    Sonarr and `SABnzbd` do not agree on words, and an operator moving between
    their screens should not have to work out that two of them are one.
    """
    deep: typing.NotRequired[str | None]
    """More, for somebody who asks — never needed in order to act."""
    forms: list[str]
    """The other forms this product itself writes the word in, where a state or a
    stage is named by one — `grabbed` for `grab`, `seeding` for `seed`.

    Apart from [`Self::also_called`], which is another service's word and one this
    product must never write as its own. These are this product's own words, and a
    surface explaining a word it was sent looks for the word it was sent here, so
    that nothing on the far side has to guess which term an inflection belongs to.
    """
    short: str
    """One sentence: what it is for and what it costs or gains.

    Enough to act on. Somebody who reads only this should not be stuck.
    """
    word: str
    """The word as it appears in the interface."""


class Terms(typing.TypedDict):
    """How a bundle was made: what was bounded, what was replaced, and what its operator asked
    to have shown as it is.

    Carried in the bundle rather than known only to the command that wrote it, because the
    person who reads one is usually not the person who chose any of this.
    """

    filenames: Filenames
    """Whether media filenames were shown."""
    revealed: list[str]
    """The settings the operator asked to have shown as they are."""
    window: str
    """How much of the logs was taken, said as it would be said aloud."""


type Tier = typing.Literal["stop", "services", "configuration", "media"]
"""Which of the four removals was asked for."""


type TraceConfidence = typing.Literal["certain", "uncertain"]
"""How sure the correlation behind a trace is — a release renamed between services can
only be matched fuzzily, and a guess presented as fact is worse than a marked one.
"""


class TraceMoment(typing.TypedDict):
    """One moment in a traced item's history: what happened and when. Where [`TraceStage`]
    is the linear progress, this is the log an \\*arr kept — the grabs, the failed
    downloads, the import and any later removal — so a repeated attempt is seen as the
    pattern it is rather than flattened to a single furthest stage.
    """

    at: str
    """When the service reported it."""
    outcome: TraceOutcome
    """What happened."""


type TraceOutcome = typing.Literal["grabbed", "download-failed", "imported", "removed"]
"""A notable thing that happened to an item, as an \\*arr's history records it. Where the
furthest stage answers \"how far did it get?\", the sequence of outcomes answers \"what
has been tried?\" — a release grabbed more than once, a download that failed and was
tried again, a file imported and later removed. Repeated failed grabs are a pattern
worth seeing, not something a single furthest-stage reading can show.
"""


class TraceReport(typing.TypedDict):
    """Where one item is in the pipeline: how far it got, why it stopped if it did, and the
    stages it passed through — the answer to \"where is my show?\".
    """

    confidence: TraceConfidence
    """How sure the trace is of the item it followed."""
    coverage: typing.NotRequired[Coverage | None]
    """How much of the item is actually here, season by season — present for an item
    made of parts, absent for a film, which is the whole item and has none.

    The furthest stage alone cannot answer this: a series is \"imported\" the moment one
    episode lands, which reads as done while the rest are missing.
    """
    findings: list[str]
    """Disagreements between the services about this item, each in plain language — a
    media server holding what no service is monitoring, and the like. Orthogonal to
    the linear pipeline: not where the item got to, but where two services' views of
    it contradict, surfaced rather than silently reconciled.
    """
    furthest: Stage
    """The furthest stage the item reached."""
    history: list[TraceMoment]
    """The notable events in its history, oldest first — the grabs, failed downloads,
    imports and removals. Repeated attempts show here as the pattern they are, which
    the single furthest stage cannot.
    """
    item: str
    """The term the item was searched for by."""
    matched: bool
    """Whether a monitored item matched the term at all — a false here is itself the
    answer: nobody asked for it.
    """
    stages: list[TraceStage]
    """The stages it passed through, in order."""
    stall: typing.NotRequired[str | None]
    """Why it stopped, where it plainly has — or absent where it is progressing or done."""


class TraceStage(typing.TypedDict):
    """One stage a traced item reached, named as the operator would read it: the stage,
    the service that recorded it, and when.
    """

    at: typing.NotRequired[str | None]
    """When it happened, as the service reported it — absent for a stage inferred
    rather than timed, such as being monitored.
    """
    service: str
    """The service that recorded it."""
    stage: Stage
    """The stage reached."""


class Transfer(typing.TypedDict):
    """One active download, as the dashboard shows it."""

    eta: typing.NotRequired[Duration | None]
    """The time left, or `None` where it is stalled and there is none to give."""
    name: str
    """What is being downloaded."""
    progress: int
    """How far along, as a percentage from zero to a hundred."""
    protocol: DashboardProtocol
    """How it is being downloaded."""
    speed: DashboardReading
    """The current speed in bytes per second — a [`Reading`], because a genuine
    zero (stalled) and a source that has gone quiet mean opposite things here,
    and this is the very figure that difference is about.
    """


class Tree(typing.TypedDict):
    """One host tree captured from a setup lemonfiber does not manage.

    Both halves are needed to find it again: the archive path says where it sits
    inside the archive, and the host path says where it was read from. Nothing
    derives the second from the first, because a tree outside lemonfiber's layout
    has no layout to derive it from.
    """

    archive_path: str
    """Where it sits inside the archive."""
    host_path: str
    """Where it was read from, on the machine whose setup was taken over."""


type Triggered = TriggeredStarted | TriggeredNotStarted | TriggeredFailed
"""What became of asking one service to re-search its existing content."""


class TriggeredFailed(typing.TypedDict):
    """The service refused the command or could not be reached."""

    detail: str
    """The service's own account of why."""
    state: typing.Literal["failed"]


class TriggeredNotStarted(typing.TypedDict):
    """The service had not finished starting — no key yet — so nothing was asked of
    it; running the upgrade again once it is up will reach it.
    """

    state: typing.Literal["not-started"]


class TriggeredStarted(typing.TypedDict):
    """The re-search was accepted and now runs in the service's background."""

    state: typing.Literal["started"]


class Trouble(typing.TypedDict):
    """Something somebody reports, and what is likely behind it.

    Keyed by the symptom rather than the cause: the person asking has the symptom,
    and which cause it is is the thing they cannot yet say.
    """

    causes: list[Cause]
    """What is likely behind it, most likely first."""
    symptom: str
    """What somebody says is happening, in their words."""


class Undeclared(typing.TypedDict):
    """A container running under this project that the stack description never declared.

    Its own type rather than a [`Service`] with the fields left blank. A service
    carries a profile and a criticality, and there is no honest value for either here:
    filling them in would have lemonfiber asserting how much something matters when
    the only thing it knows about it is that it exists.
    """

    describes: str
    """What it does for the operator — which is exactly what is not known."""
    id: str
    """The Compose service name the engine reports it under."""
    state: ServiceState
    """What it is doing, read the same way a declared service's state is."""


class Undo(typing.TypedDict):
    """A single reversal, for the surface to carry out."""

    action: Action
    """What reversing it does."""
    target: str
    """The service or file to reverse it against."""


class UndoLeft(typing.TypedDict):
    """One change a reversal did not put back, and why it did not."""

    because: str
    """Why it is still standing, in the operator's terms."""
    target: str
    """What the change was against — a service, or lemonfiber's own environment file."""


class UndoNoted(typing.TypedDict):
    """What putting one change back means beyond the change itself."""

    because: str
    """What goes back, what does not go with it, and what to do instead."""
    target: str
    """What the change was against."""


class UndoReversal(typing.TypedDict):
    """What putting a run back came to.

    A report rather than a bare list, because it is what an envelope carries and an
    envelope carries a document. Two lists, and the second is the one that matters when
    it is not empty: what went back, and what did not with the reason it did not.
    """

    left: list[UndoLeft]
    """What was not put back, each with the reason it was not.

    A reversal an operator asked for by name has to say what it did *not* do. Five
    changes asked back and three carried out is a machine in a state nobody has been
    told about, and \"some of it worked\" is the sentence that makes somebody go
    looking by hand. Empty where everything went back, which is the common case.

    On a run that only said what it would do, this is what it cannot promise: a
    change that goes back through the service that made it goes back only where that
    service is answering, and a rehearsal has not asked one.
    """
    noted: typing.NotRequired[list[UndoNoted]]
    """What putting these changes back means beyond the changes themselves.

    Empty on almost every run. What lands here is a change the judgement can put
    back in full and that still leaves something behind — the one in force today
    being a setting that re-points where data lives, which goes back while the
    library stays exactly where it was moved to.

    Neither list above can carry it. It did not fail to go back, so it is not what
    was left; and reporting only that it went back would send an operator looking
    for their files at an address that no longer names them.
    """
    rehearsed: bool
    """Whether this run only said what it would put back.

    A flag rather than a second shape, because the two lists mean the same thing
    either way and a caller reading them should read one document. What changes is
    the tense a surface says them in.
    """
    reversed: list[Undo]
    """What was put back, in the order it was — or, on a run that only said what it
    would do, what would go back.
    """


class Unfilled(typing.TypedDict):
    """A capability something asks for and nothing fills, and what asked for it.

    The pair rather than the name: a capability nothing fills is a fact about the
    stack, and a capability *`seerr` asks for* and nothing fills is a thing somebody
    can act on. Reporting the first and leaving the second to be worked out is the
    obscure failure at the point of use this exists instead of.
    """

    by: str
    """The service that asked."""
    capability: str
    """What it asked for."""


class Uninstall(typing.TypedDict):
    """A removal, before or after it happened."""

    manifest: UninstallManifest
    """What removing would come to, or what it came to."""
    rehearsed: bool
    """Whether this was a rehearsal: what would have happened, with none of it done.

    Said in a field of its own so that a rehearsal is never told from the real run by
    its wording alone.
    """
    removal: UninstallRemoval
    """Whether anything was removed on this run."""


class UninstallConfidence(typing.TypedDict):
    """How much of a manifest was read and how much stood in for what could not be."""

    complete: bool
    """Whether every source this tier needed answered."""
    unread: list[str]
    """What could not be read, each in the words of whatever refused.

    The point of the field: a manifest that is short says so and says why, rather
    than reading as a machine with less on it than it has.
    """


class UninstallLeft(typing.TypedDict):
    """Something a removal could not take."""

    by_hand: str
    """How to finish it by hand."""
    name: str
    """What is still there."""
    why: str
    """What the machine said about it, verbatim."""


class UninstallManifest(typing.TypedDict):
    """What removing would come to, shown before anything is removed."""

    agreement: str
    """What this reading names itself, so an answer says which reading it answered."""
    backup: typing.NotRequired[str | None]
    """Whether a backup was offered before configuration is destroyed, and how."""
    bytes: int
    """What the lines that are going occupy, where that is knowable."""
    coming: list[Coming]
    """What is still coming down, which stopping would interrupt."""
    confidence: UninstallConfidence
    """How much of this was read, and what could not be."""
    foreign: list[Foreign]
    """What is beneath the data location that the stack did not put there.

    Not a warning. While this is non-empty the data location is never removed as
    one tree, and only the stack's own directories beneath it are offered.
    """
    items: list[Item]
    """Every line it reaches, each said to be going or said to be kept."""
    keeps: str
    """What it leaves alone, in the operator's words."""
    outside: list[Outside]
    """What lemonfiber cannot remove, each with how to remove it by hand."""
    removes: str
    """What it takes, in the operator's words."""
    tier: Tier
    """Which removal this is."""
    volume: typing.NotRequired[str | None]
    """Whether the data location is on a network share or a drive that unplugs.

    Said where it is, so removing across a mount an operator forgot was a mount is
    something they read before agreeing rather than after.
    """


type UninstallRemoval = (
    UninstallRemovalSurveyed | UninstallRemovalConfirmed | UninstallRemovalComplete | UninstallRemovalPartial
)
"""Whether anything was removed on this run, and what became of it.

Four states rather than the five a removal passes through. `removing` is the
interval between the last two and is said through the narrator as it happens — a
value returned at the end cannot be the state a run is in while it runs, and a
variant nothing could ever answer with would be a state that is documentation
pretending to be a value.
"""


class UninstallRemovalComplete(typing.TypedDict):
    """Everything the manifest named as going is gone."""

    credentials: list[str]
    """The credentials this destroyed, said rather than left to be inferred."""
    gone: list[str]
    """What went, by the name the manifest gave it."""
    state: typing.Literal["complete"]


class UninstallRemovalConfirmed(typing.TypedDict):
    """The tier and the manifest were agreed to, and this run changes nothing — the
    state a rehearsal ends in.
    """

    state: typing.Literal["confirmed"]


class UninstallRemovalPartial(typing.TypedDict):
    """Some of it could not be removed, and each of those is named with how to
    finish it by hand.
    """

    credentials: list[str]
    """The credentials this destroyed."""
    gone: list[str]
    """What went, by the name the manifest gave it."""
    left: list[UninstallLeft]
    """What is still there, and how to remove it."""
    state: typing.Literal["partial"]


class UninstallRemovalSurveyed(typing.TypedDict):
    """Everything is enumerated with its size, and nothing has been removed."""

    state: typing.Literal["surveyed"]


type Unrated = typing.Literal["held-back", "let-through"]
"""What is to happen to content the media server has no rating for.

A choice rather than a default, because a great deal of content carries no rating
and either answer is wrong for somebody: holding it back makes legitimate content
invisible, and letting it through lets through the one thing nobody vetted.

Spelled `HeldBack` and `LetThrough` rather than blocked and allowed, because
[`Allowed`] is the shape this sits on and a field called `unrated: Allowed` would
read as the opposite of what it is.

A word rather than a flag on both the read and the write, so the setting is named
the same in the answer that reports it as in the call that made it — and so neither
[`Access`] nor the report built from it becomes a row of four unlabelled booleans.

Letting it through is the default because it is the media server's: a new account
is made holding nothing back, so that is the state an account is found in rather
than a decision anybody took.
"""


class UnsupportedReport(typing.TypedDict):
    """Something lemonfiber cannot act on, named rather than passed over.

    Written for a migration survey and read by two reports now. The second is the
    status of a stack the operator maintains themselves, where a service declaring an
    API this build cannot reach is named the same way — what, and why — rather than
    being dropped from every feature that would have used it. One shape for both,
    because \"named rather than passed over\" is the whole of what either is saying and
    two shapes would be two ways of saying it.
    """

    because: str
    """Why lemonfiber cannot act on it, in the operator's terms."""
    what: str
    """What was found, by the name the thing that found it gives it — a project and
    service for a survey, a service id for a stack lemonfiber runs.
    """


class UpdateChange(typing.TypedDict):
    """What updating one service would change."""

    because: str
    """What the step means, in the words an operator decides on."""
    current: str
    """The version it is standing on now."""
    irreversible: bool
    """Whether taking it is a step nothing walks back."""
    jump: Jump
    """How large the step between them is."""
    refused: bool
    """Whether lemonfiber refuses to take it at all."""
    service: str
    """The service, by its manifest id, which is also its Compose service name."""
    target: str
    """The version this build pins for it."""


class UpdateReport(typing.TypedDict):
    """Where this copy of lemonfiber stands, and what moving it would come to."""

    afterwards: str
    """What updating leaves alone, and what it needs afterwards."""
    asked: typing.NotRequired[str | None]
    """The version the operator asked to move to, where they asked for one."""
    at: typing.NotRequired[str | None]
    """Where the running binary is, with any link followed, or nothing where this
    machine would not say.

    The answer to which of several copies on a search path is the one that ran, so
    a version somebody quotes can be attributed to a file rather than to a name.
    """
    carries: str
    """What a release brings besides the program, and when any of it is fetched."""
    changed: typing.NotRequired[str | None]
    """What the version on offer says it changed, as its release page words it.

    The question an operator is actually weighing. Carried as the notes were
    written rather than taken apart here, because what a surface does with them
    is a surface's business — a terminal flattens them, a browser renders them,
    and a script wants them as they came.
    """
    command: typing.NotRequired[str | None]
    """Exactly what to type, where there is something exact to type."""
    configuration: typing.NotRequired[str | None]
    """Whether the version named can read the configuration on this machine.

    Only where a version was named, since it is the question a downgrade asks and
    nothing else does.
    """
    installed: Installed
    """How this copy got onto the machine."""
    instead: typing.NotRequired[str | None]
    """Why there is nothing exact to type, where there is not; or, where typing the
    command is not the whole of the move, what has to follow it.
    """
    offered: typing.NotRequired[str | None]
    """The newest version released, where the check could read one."""
    owner: typing.NotRequired[str | None]
    """The tool that owns this copy, where one does."""
    replaceable: typing.NotRequired[bool | None]
    """Whether the directory holding the running binary can be written to.

    Nothing where it was not asked, which is every copy a package manager owns —
    replacing one of those is that tool's business and not this one's. Asked by
    trying rather than by reading permission bits, and reported rather than acted
    on: a copy this operator cannot replace is a thing to say with the path, never
    a reason to go looking for a way to become somebody else.
    """
    running: str
    """The version running now."""
    standing: SelfUpdateStanding
    """Which of the states this is."""
    untold: typing.NotRequired[str | None]
    """Why availability could not be told, where it could not."""


type UpdateReversal = typing.Literal["rollback", "restore"]
"""How a service could be put back the way it was.

The distinction is the whole of why this is reported rather than left to be
worked out: pinning the previous image again is a minute's work, and restoring a
backup is an evening. Offering the first where only the second can succeed is
worse than offering nothing, because it is acted on.
"""


type UpdateState = typing.Literal["current", "updates-available", "updated", "partial", "failed"]
"""Where the stack stands against the versions this build pins.

Exactly one of these is true of a run at a time. A surface that had to say
\"updates available, and also partly applied\" would be reporting the question
rather than the answer.
"""


class UpgradeMedia(typing.TypedDict):
    """One media type an upgrade covers: its chosen quality, that quality's cost, and —
    once confirmed — what became of asking its service to re-search.

    Reported per media type rather than as one figure, because each type carries its
    own preset and so its own cost: film at maximum and television at space-saving are
    upgraded to different bars, and a single number would misstate one of them.
    """

    media_type: str
    """The media type — `tv` or `movies`."""
    outcome: typing.NotRequired[Triggered | None]
    """What became of the re-search, or `None` where the upgrade was not confirmed
    and only the cost was stated.
    """
    preset: str
    """The preset in force for it."""
    size_per_hour: str
    """Roughly what an hour of it costs at that preset."""


class UpgradeReport(typing.TypedDict):
    """What upgrading existing content did, or — unconfirmed — would do.

    Upgrading re-acquires the existing library at the chosen quality, which is a
    large, bandwidth-expensive operation, so it is a separate explicit action whose
    cost is stated before it runs and which does nothing until confirmed. Each *arr
    re-searches against its own current cutoff, so the report speaks per media type
    rather than asserting one preset across the library.
    """

    confirmed: bool
    """Whether the operator confirmed; without it nothing was triggered, only the
    cost stated.
    """
    media: list[UpgradeMedia]
    """Per media type: its preset, that preset's cost, and — confirmed — the outcome."""
    rehearsed: bool
    """Whether this was a rehearsal: what would have happened, with none of it done.

    Said in a field of its own so that a rehearsal is never told from the real run by
    its wording alone.
    """


type Validation = ValidationValid | ValidationRejected | ValidationUnreachable | ValidationDegraded
"""What proving a credential against its live service established — never the
input, only the outcome.

Read back as well as built. A surface that is not in this process asks setup to
prove a credential and is told what came of it, so the four outcomes are tagged
by name rather than distinguished by which field is present — the same reason an
answer carries the step it belongs to.
"""


class ValidationDegraded(typing.TypedDict):
    """It authenticated, but cannot do the job it is for — exhausted, limited, or
    otherwise unable.
    """

    detail: str
    """What it can no longer do, and why where the service says."""
    outcome: typing.Literal["degraded"]


class ValidationRejected(typing.TypedDict):
    """The service answered and refused: the credential is wrong for it."""

    detail: str
    """What the service said, in terms the operator can act on."""
    outcome: typing.Literal["rejected"]


class ValidationUnreachable(typing.TypedDict):
    """Nothing usable answered, so nothing can be concluded about the credential."""

    detail: str
    """Why nothing usable came back."""
    outcome: typing.Literal["unreachable"]


class ValidationValid(typing.TypedDict):
    """Proven working, carrying the capability observed while proving it."""

    observed: str
    """The observed fact — what the service did, not that it merely answered."""
    outcome: typing.Literal["valid"]


type ValueOrigin = (
    ValueOriginBundled
    | ValueOriginOperator
    | ValueOriginPlugin
    | ValueOriginUnknown
    | ValueOriginOverridden
    | ValueOriginOrphaned
)
"""Where a value in force came from.

Published under a name of its own because the generated schema keys on the type's
bare name, and a second `Origin` in the crate would be merged with this one into a
single definition carrying the variants of both — a published contract saying a
credential may be *unknown* and a setting may be *service*, neither of which is
true, and neither of which the additive-only surface check would refuse.
"""


class ValueOriginBundled(typing.TypedDict):
    """This build's own, out of what lemonfiber ships rather than out of a choice."""

    origin: typing.Literal["bundled"]


class ValueOriginOperator(typing.TypedDict):
    """The operator settled it, whether by answering for it or by editing it since."""

    origin: typing.Literal["operator"]


class ValueOriginOrphaned(typing.TypedDict):
    """A plugin set it and is no longer installed, and the value is still in force.

    Only where the record of what is installed was read and does not hold that
    plugin. A record that would not read cannot say a plugin is gone, so that is
    an unknown rather than this.
    """

    named: str
    """Which plugin set it."""
    origin: typing.Literal["orphaned"]


class ValueOriginOverridden(typing.TypedDict):
    """An installed plugin set it over a value that was there before, and that value
    is carried with it: what is in force and what it replaced are read together.
    """

    named: str
    """Which plugin set what is in force."""
    origin: typing.Literal["overridden"]
    replaced: ValueReplaced
    """What it replaced, and where that came from."""


class ValueOriginPlugin(typing.TypedDict):
    """A named plugin set it."""

    named: str
    """Which one, so the thread back to it is a name rather than a search."""
    origin: typing.Literal["plugin"]


class ValueOriginUnknown(typing.TypedDict):
    """It could not be established, and what stopped it."""

    origin: typing.Literal["unknown"]
    why: str
    """What stopped it being established, so the gap reads as a reason rather
    than as a shrug.
    """


class VersionReport(typing.TypedDict):
    """What versions are in play: the binary, the stack it operates, and what changed.

    The changelog is here rather than behind a request of its own because it answers
    the second half of the same question. \"Which version am I on\" is asked by
    somebody deciding whether to move, and what they need next is what the version
    they are on actually brought — so every surface that already reaches this read
    reaches both halves, and none of the three had to learn a new question.
    """

    binary: str
    """The running binary's version."""
    changelog: Notes
    """What this build's release changed, and every release there has been."""
    compose: typing.NotRequired[str | None]
    """What the container engine reports, when it could be asked."""
    stack: str
    """The version of the stack this build operates."""
    supported_schema: list[int]
    """The manifest schema generations this build reads."""


class Vigil(typing.TypedDict):
    """The watch a run would keep, and what it would do at the end of it."""

    command: list[str]
    """The invocation it would run the moment that location went, word for word.

    Built by the same path a real watch stops the services through, rather than
    described beside it: an argv reported from a second reckoning is one nobody
    runs, and the one nobody runs is the one that stops being right.
    """
    every: int
    """How often it would look, in seconds."""
    root: str
    """The data location it would hold."""


class Vocabulary(typing.TypedDict):
    """Every word this product explains, for somebody who asked what there is to ask
    about.
    """

    words: list[Term]
    """The words, in the order somebody meets them."""


class Volume(typing.TypedDict):
    """One volume, as one run measured it."""

    at: str
    """The path that was measured."""
    committed: int
    """The bytes already committed to landing here."""
    free: typing.NotRequired[int | None]
    """Bytes free, or nothing where the volume could not be read."""
    level: Level
    """Where it stands."""
    limit: typing.NotRequired[int | None]
    """The effective limit — the mount's own size, which on a dataset given a
    quota is the quota rather than the device beneath it.
    """
    point: str
    """Where the volume holding it is mounted, which is what the limit belongs to."""
    projected: typing.NotRequired[int | None]
    """What would be free once the committed content has landed."""
    reading: Freshness
    """What the reading is worth."""
    role: Role
    """Which of the two this is."""


class Vpn(typing.TypedDict):
    """What the VPN is doing, and whether the download client is actually behind it."""

    country: str
    """The country that address is in."""
    egress_matches: bool
    """Whether the download client's own egress address matches the tunnel's —
    the one thing that proves traffic is genuinely leaving through it.
    """
    exit_ip: str
    """The tunnel's exit address as the outside world sees it."""
    forwarded_port: typing.NotRequired[int | None]
    """The port the provider forwards, where forwarding is on."""


class WalkthroughReport(typing.TypedDict):
    """What a first-content walkthrough did — the whole of it, narrated line by line as it
    happened and gathered here so the ending can be rendered, serialised and exited on.
    """

    already_here: bool
    """Whether what was asked for was already here, and so was not acquired again."""
    handover: typing.NotRequired[Handover | None]
    """Where it leaves the operator, where it worked."""
    in_background: bool
    """Whether the download was handed to the background rather than waited out."""
    item: typing.NotRequired[str | None]
    """What it walked, where it got as far as choosing something."""
    lines: list[Line]
    """Every line it said, in order — the same lines the operator watched arrive, kept so
    a machine-readable run is not a silent one.
    """
    link: typing.NotRequired[Link | None]
    """What the import did with the file, where it got that far."""
    proves: str
    """What it set out to prove, said so the operator knows what they watched."""
    shape: Shape
    """Which walk this was."""
    state: WalkthroughState
    """Where it ended up."""
    stopped: typing.NotRequired[Stopped | None]
    """Where and why it stopped, where it did."""
    suggestions: list[str]
    """What could have been walked instead, where nothing was chosen — the safe first
    attempts, so an operator with an empty library is not left guessing.
    """


type WalkthroughState = typing.Literal[
    "offered",
    "skipped",
    "searching",
    "grabbing",
    "downloading",
    "importing",
    "complete",
    "failed",
    "abandoned",
]
"""What has become of a walkthrough."""


type WalkthroughStep = typing.Literal[
    "choosing", "searching", "grabbing", "downloading", "importing", "scanning", "available"
]
"""One step of the walk, ordered from picking something to watching it play."""


type WhenExceeded = typing.Literal["pause", "throttle", "continue"]
"""What to do when a declared cap is reached."""


type Whose = typing.Literal["stack", "operator"]
"""Who settled a contest between claimants."""


class Wired(typing.TypedDict):
    """One of the stack's links, answered."""

    by: str
    """The service the link runs from — what asked."""
    reaches: Reaches
    """What it reaches."""


class Wiring(typing.TypedDict):
    """One connection, and how it turned out."""

    connection: str
    """What was being connected, such as `SABnzbd into Sonarr`."""
    severity: SeedSeverity
    """How serious the outcome is — information by default, a warning where the
    connection breaks the stack.
    """
    state: SeedState
    """How it turned out."""


class WiringContest(typing.TypedDict):
    """An ask several services claim and nothing has chosen between, so it reaches
    nothing.
    """

    by: str
    """The service that asked."""
    capability: str
    """What it asked for."""
    claimants: list[str]
    """Every claimant, named — a plugin's with the plugin beside it."""


class WiringReport(typing.TypedDict):
    """What this stack wires to what."""

    unfilled: list[Unfilled]
    """Every capability something asks for and nothing fills, naming what asked.

    Repeated out of the links above rather than left to be found among them: a
    stack with one unfilled ask among twenty working ones is a stack whose one
    problem is a line in a list, and a consumer that had to notice it would be
    the reason nobody did.
    """
    wired: list[Wired]
    """Every link, in the order the stack declares them."""


type WiringSettled = (
    WiringSettledOutright
    | WiringSettledEach
    | WiringSettledContested
    | WiringSettledChosen
    | WiringSettledUnfilled
)
"""How an ask was settled."""


class WiringSettledChosen(typing.TypedDict):
    """Several claimants, and a choice is recorded."""

    over: list[str]
    """The ones not chosen, so the choice reads as a choice."""
    settled: typing.Literal["chosen"]
    whose: Whose
    """Who chose."""
    why: typing.NotRequired[str | None]
    """Why, where the chooser said."""


class WiringSettledContested(typing.TypedDict):
    """Several claimants and the link asked for one. Refused until somebody chooses:
    install order, precedence and recency are each a way of being right most of
    the time, and the times they are wrong are somebody's stack answering to the
    wrong software.
    """

    claimants: list[str]
    """Every candidate, named, so a choice is made from a list."""
    settled: typing.Literal["contested"]


class WiringSettledEach(typing.TypedDict):
    """Every claimant, because the link asked for all of them rather than one."""

    settled: typing.Literal["each"]


class WiringSettledOutright(typing.TypedDict):
    """One claimant, and nothing to settle."""

    settled: typing.Literal["outright"]


class WiringSettledUnfilled(typing.TypedDict):
    """Nothing claims it. What asked is named beside this, which is the point."""

    settled: typing.Literal["unfilled"]


class WizardReport(typing.TypedDict):
    """Where a setup run stands, and what it is still asking for.

    The answer to every step of setup driven from outside this process: a surface
    asks where the walk is, submits one answer, and is told where the walk is now.
    Nothing here is a copy of the wizard's own state — it is read off the wizard
    each time, so a surface cannot hold a stale one and act on it.

    **The answers themselves are never in it.** Setup gathers an indexer key and a
    provider password, and this report is one a script can log, so it says what was
    *decided* and never what was *entered* — the same line [`SetupReport`] holds.
    What will be written is in `plan`, with every credential withheld exactly as
    `config show` withholds one.
    """

    asks: bool
    """Whether that step asks a question, as opposed to only informing."""
    at: WizardStep
    """The step the operator is on."""
    offered: bool
    """Whether this machine has setup left to do. False once configuration
    exists and nothing is part-way through, which is when a surface directs
    the operator to reconfiguration instead of asking the first question again.
    """
    phase: Phase
    """Where this run stands in its lifecycle. `applying` read back here means an
    apply stopped part-way, because an apply that is still running is one this
    answer is waiting on.
    """
    plan: list[SettingReport]
    """What applying will write, in the order it will be written, with any value
    nobody has argued for showing withheld.
    """
    proof: typing.NotRequired[Validation | None]
    """What proving the credential just given came to, where one was given.

    Setup tests an indexer key and a Usenet login against their live services as
    they are entered, and this is what the service answered — never what was
    entered. Absent for every other answer, and for a step that gave none.
    """
    ready_for_review: bool
    """Whether every applicable question is answered, so the plan can be applied."""
    rehearsed: Ran
    """Whether this was a rehearsal: what would have happened, with none of it done.

    Said in a field of its own so that a rehearsal is never told from the real run by
    its wording alone.
    """
    unanswered: list[WizardStep]
    """Every question that applies on this machine and has no answer yet, in the
    order they are put.
    """
    written: list[str]
    """What an apply that stopped part-way had already written, each said plainly.

    The partial state a recovery is chosen about, so whoever chooses has seen it.
    Empty for every other phase, and empty too for an apply that stopped before
    it wrote anything.
    """


type WizardStep = typing.Literal[
    "welcome",
    "preflight",
    "prerequisites",
    "protocols",
    "vpn",
    "data-location",
    "credentials",
    "provider",
    "service-user",
    "library",
    "household",
    "notifications",
    "autostart",
    "review",
]
"""A step of setup, in the order the operator meets it.

Some steps only inform (they detect and state, and the operator acknowledges);
others ask a question whose answer the wizard records. The apply-and-onward
steps — writing config, pulling images, wiring services — are not modelled
here yet: they arrive with the features they drive, and this machine covers
the read-only phase that precedes them.
"""


ConfigChange = typing.TypedDict(
    "ConfigChange",
    {
        "cost": Cost,
        "from": typing.NotRequired[str | None],
        "key": str,
        "to": str,
    },
)
"""The difference between the configuration in force and the one proposed.

One setting, because one call changes one setting. What makes it a diff rather than
a value is `from`: an operator deciding whether to go ahead is deciding between two
things, and a report that showed only the new one would be asking them to remember
the old one correctly.
"""


Contribution = typing.TypedDict(
    "Contribution",
    {
        "action": typing.NotRequired[str | None],
        "at": str,
        "category": typing.NotRequired[str | None],
        "detail": typing.NotRequired[str | None],
        "expect": typing.NotRequired[Expect | None],
        "expected": typing.NotRequired[list[PluginExpectedFailure]],
        "fixture": typing.NotRequired[str | None],
        "for": typing.NotRequired[str | None],
        "id": str,
        "request": typing.NotRequired[PluginRequest | None],
        "service": typing.NotRequired[str | None],
        "timeout_s": typing.NotRequired[int | None],
        "title": typing.NotRequired[str | None],
        "why": typing.NotRequired[str | None],
    },
)
"""A row in a register lemonfiber already runs.

The fields beyond `at` and `id` are the row its point declares, and the point is
published — so the required set, the optional set, the closed sets and the bounds
are read from `extension-points.json` rather than restated here. What this type
fixes is that a contribution is declared in this block and nowhere else, and that
it carries nothing outside the union of the rows the published points take.
"""


CredentialHeld = typing.TypedDict(
    "CredentialHeld",
    {
        "advisory": typing.NotRequired[str | None],
        "consumers": list[str],
        "fingerprint": typing.NotRequired[str | None],
        "from": ValueOrigin,
        "location": str,
        "name": str,
        "origin": Origin,
        "setting": str,
        "state": CredentialState,
    },
)
"""One credential, described without being disclosed.

There is deliberately no value here, and no field a value could be put in later
without the change being visible in review.
"""


FreshnessAsOf = typing.TypedDict(
    "FreshnessAsOf",
    {
        "as": typing.Literal["as_of"],
        "at": int,
    },
)
"""Read across a network share, which answers with what it was last told —
carrying the moment it was taken, in seconds since the epoch, so a figure
nobody can refresh is at least dated.
"""


FreshnessLive = typing.TypedDict(
    "FreshnessLive",
    {
        "as": typing.Literal["live"],
    },
)
"""Read off a local disk, so it is true as of now."""


HouseholdRemoval = typing.TypedDict(
    "HouseholdRemoval",
    {
        "asks-through-the-request-service": bool,
        "confirmed": bool,
        "findings": list[str],
        "name": str,
        "rehearsed": bool,
        "requests": int,
        "revoked": Revoked,
    },
)
"""What removing somebody costs, and what it did.

Read before anything is written: the whole point of the unconfirmed run is that every
figure here is knowable without removing anybody.
"""


LimitAbsolute = typing.TypedDict(
    "LimitAbsolute",
    {
        "as": typing.Literal["absolute"],
        "at": int,
    },
)
"""A figure in bytes a second, as it was given."""


LimitShare = typing.TypedDict(
    "LimitShare",
    {
        "as": typing.Literal["share"],
        "at": int,
    },
)
"""A proportion of what the line was measured to carry, in whole per cent."""


LimitUnlimited = typing.TypedDict(
    "LimitUnlimited",
    {
        "as": typing.Literal["unlimited"],
    },
)
"""Nothing holds it back."""


MovedReport = typing.TypedDict(
    "MovedReport",
    {
        "from": int,
        "service": str,
        "to": int,
    },
)
"""Where one service would listen to run beside what is already here."""


PluginSource = typing.TypedDict(
    "PluginSource",
    {
        "from": str,
        "plugin": str,
        "standing": PluginSourceStanding,
    },
)
"""Whether one installed plugin's source can still be fetched."""


PluginUpdate = typing.TypedDict(
    "PluginUpdate",
    {
        "from": str,
        "install": PluginInstall,
        "interrupts": list[str],
        "plugin": str,
        "restored": typing.NotRequired[PluginRestored | None],
        "stopped": typing.NotRequired[str | None],
        "to": str,
        "went_back": UndoReversal,
    },
)
"""What updating a plugin came to, or would come to, as one account.

**One account, because it is one operation.** An update is the version installed
going back and another coming on, and a report that gave those as a removal and an
install side by side would invite reading them as two things that might each have
happened. What an operator has to be able to read off this is which version the
machine is on, and there are exactly two answers: the new one, where
`install.recorded` is true, or the one it replaced, which `restored` says the state
of.
"""


ResolvedAt = typing.TypedDict(
    "ResolvedAt",
    {
        "bytes_per_second": int,
        "is": typing.Literal["at"],
    },
)
"""This many bytes a second."""


ResolvedUnlimited = typing.TypedDict(
    "ResolvedUnlimited",
    {
        "is": typing.Literal["unlimited"],
    },
)
"""Nothing holds it back."""


ResolvedUnmeasured = typing.TypedDict(
    "ResolvedUnmeasured",
    {
        "is": typing.Literal["unmeasured"],
    },
)
"""A proportion was asked for and nothing has measured the line.

Deliberately not folded into [`Self::Unlimited`]. \"Half of an unknown
number\" resolving to \"no limit at all\" is the shape of a setting an
operator believes is in force while the stack takes the whole line.
"""


Rhythm = typing.TypedDict(
    "Rhythm",
    {
        "from": str,
        "to": str,
    },
)
"""The hours the household is awake, declared once for every download client."""


UpdateApplied = typing.TypedDict(
    "UpdateApplied",
    {
        "detail": typing.NotRequired[str | None],
        "ending": Ending,
        "from": str,
        "reversal": UpdateReversal,
        "service": str,
        "to": str,
    },
)
"""What one service's update came to."""


ValueReplaced = typing.TypedDict(
    "ValueReplaced",
    {
        "from": ValueOrigin,
        "value": typing.NotRequired[str | None],
        "withheld": bool,
    },
)
"""The value a plugin's change replaced, and where that value came from.

Its own origin rather than assumed to be this build's default: before a plugin
set a value, the operator may have, or another plugin, and calling that value
*bundled* would tell somebody putting it back that they are returning to a
default when they are returning to a choice.
"""


PluginInstalled = typing.TypedDict(
    "PluginInstalled",
    {
        "adapters": typing.NotRequired[list[PluginServiceAdapter]],
        "contributions": typing.NotRequired[list[Contribution]],
        "declared": typing.NotRequired[PluginDeclaration],
        "description": typing.NotRequired[str | None],
        "from": typing.NotRequired[str],
        "installed_at": typing.NotRequired[str],
        "name": typing.NotRequired[str | None],
        "plugin": str,
        "provides": typing.NotRequired[list[str]],
        "recipes": typing.NotRequired[list[PluginRecipe]],
        "revision": typing.NotRequired[str],
        "services": list[PluginPlaced],
        "signed": typing.NotRequired[str],
        "version": str,
    },
)
"""One plugin's install, as it was decided."""


class AdmissionEnvelope(typing.TypedDict):
    """The envelope carrying `admission`."""

    api_version: int
    data: Admitted
    host: typing.NotRequired[str | None]
    kind: typing.Literal["admission"]


class AdoptionEnvelope(typing.TypedDict):
    """The envelope carrying `adoption`."""

    api_version: int
    data: AdoptReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["adoption"]


class AlertsEnvelope(typing.TypedDict):
    """The envelope carrying `alerts`."""

    api_version: int
    data: AlertReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["alerts"]


class ArchivesEnvelope(typing.TypedDict):
    """The envelope carrying `archives`."""

    api_version: int
    data: Listing
    host: typing.NotRequired[str | None]
    kind: typing.Literal["archives"]


class BackupEnvelope(typing.TypedDict):
    """The envelope carrying `backup`."""

    api_version: int
    data: BackupReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["backup"]


class BandwidthEnvelope(typing.TypedDict):
    """The envelope carrying `bandwidth`."""

    api_version: int
    data: Sharing
    host: typing.NotRequired[str | None]
    kind: typing.Literal["bandwidth"]


class BesideEnvelope(typing.TypedDict):
    """The envelope carrying `beside`."""

    api_version: int
    data: BesideReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["beside"]


class BundleEnvelope(typing.TypedDict):
    """The envelope carrying `bundle`."""

    api_version: int
    data: Bundle
    host: typing.NotRequired[str | None]
    kind: typing.Literal["bundle"]


class CapabilitiesEnvelope(typing.TypedDict):
    """The envelope carrying `capabilities`."""

    api_version: int
    data: Capabilities
    host: typing.NotRequired[str | None]
    kind: typing.Literal["capabilities"]


class CatalogueEnvelope(typing.TypedDict):
    """The envelope carrying `catalogue`."""

    api_version: int
    data: CatalogueReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["catalogue"]


class CertificateEnvelope(typing.TypedDict):
    """The envelope carrying `certificate`."""

    api_version: int
    data: CertificateReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["certificate"]


class ClientsEnvelope(typing.TypedDict):
    """The envelope carrying `clients`."""

    api_version: int
    data: Guidance
    host: typing.NotRequired[str | None]
    kind: typing.Literal["clients"]


class ConfigEnvelope(typing.TypedDict):
    """The envelope carrying `config`."""

    api_version: int
    data: ConfigReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["config"]


class CredentialsEnvelope(typing.TypedDict):
    """The envelope carrying `credentials`."""

    api_version: int
    data: Inventory
    host: typing.NotRequired[str | None]
    kind: typing.Literal["credentials"]


class DashboardEnvelope(typing.TypedDict):
    """The envelope carrying `dashboard`."""

    api_version: int
    data: Snapshot
    host: typing.NotRequired[str | None]
    kind: typing.Literal["dashboard"]


class DoctorEnvelope(typing.TypedDict):
    """The envelope carrying `doctor`."""

    api_version: int
    data: DoctorReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["doctor"]


class ErrorEnvelope(typing.TypedDict):
    """The envelope carrying `error`."""

    api_version: int
    data: Problem
    host: typing.NotRequired[str | None]
    kind: typing.Literal["error"]


class FormsEnvelope(typing.TypedDict):
    """The envelope carrying `forms`."""

    api_version: int
    data: FormsReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["forms"]


class FrontDoorEnvelope(typing.TypedDict):
    """The envelope carrying `front-door`."""

    api_version: int
    data: FrontDoorReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["front-door"]


class GlossaryEnvelope(typing.TypedDict):
    """The envelope carrying `glossary`."""

    api_version: int
    data: Vocabulary
    host: typing.NotRequired[str | None]
    kind: typing.Literal["glossary"]


class HandoffEnvelope(typing.TypedDict):
    """The envelope carrying `handoff`."""

    api_version: int
    data: HandoffReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["handoff"]


class HeldEnvelope(typing.TypedDict):
    """The envelope carrying `held`."""

    api_version: int
    data: HeldReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["held"]


class HistoryEnvelope(typing.TypedDict):
    """The envelope carrying `history`."""

    api_version: int
    data: HistoryReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["history"]


class HostingEnvelope(typing.TypedDict):
    """The envelope carrying `hosting`."""

    api_version: int
    data: HostingReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["hosting"]


class HouseholdEnvelope(typing.TypedDict):
    """The envelope carrying `household`."""

    api_version: int
    data: HouseholdReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["household"]


class ImportEnvelope(typing.TypedDict):
    """The envelope carrying `import`."""

    api_version: int
    data: ImportReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["import"]


class InvitationEnvelope(typing.TypedDict):
    """The envelope carrying `invitation`."""

    api_version: int
    data: Invitation
    host: typing.NotRequired[str | None]
    kind: typing.Literal["invitation"]


class JobEnvelope(typing.TypedDict):
    """The envelope carrying `job`."""

    api_version: int
    data: Started
    host: typing.NotRequired[str | None]
    kind: typing.Literal["job"]


class KeysEnvelope(typing.TypedDict):
    """The envelope carrying `keys`."""

    api_version: int
    data: KeyListing
    host: typing.NotRequired[str | None]
    kind: typing.Literal["keys"]


class LifecycleEnvelope(typing.TypedDict):
    """The envelope carrying `lifecycle`."""

    api_version: int
    data: LifecycleReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["lifecycle"]


class LogEnvelope(typing.TypedDict):
    """The envelope carrying `log`."""

    api_version: int
    data: LogLine
    host: typing.NotRequired[str | None]
    kind: typing.Literal["log"]


class MigrationEnvelope(typing.TypedDict):
    """The envelope carrying `migration`."""

    api_version: int
    data: MigrationReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["migration"]


class MintedKeyEnvelope(typing.TypedDict):
    """The envelope carrying `minted-key`."""

    api_version: int
    data: MintedKey
    host: typing.NotRequired[str | None]
    kind: typing.Literal["minted-key"]


class MusicEnvelope(typing.TypedDict):
    """The envelope carrying `music`."""

    api_version: int
    data: MusicReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["music"]


class NewsEnvelope(typing.TypedDict):
    """The envelope carrying `news`."""

    api_version: int
    data: Newest
    host: typing.NotRequired[str | None]
    kind: typing.Literal["news"]


class NewsItemsEnvelope(typing.TypedDict):
    """The envelope carrying `news-items`."""

    api_version: int
    data: News
    host: typing.NotRequired[str | None]
    kind: typing.Literal["news-items"]


class OutboundEnvelope(typing.TypedDict):
    """The envelope carrying `outbound`."""

    api_version: int
    data: Leaving
    host: typing.NotRequired[str | None]
    kind: typing.Literal["outbound"]


class PairingEnvelope(typing.TypedDict):
    """The envelope carrying `pairing`."""

    api_version: int
    data: Pairing
    host: typing.NotRequired[str | None]
    kind: typing.Literal["pairing"]


class PausingEnvelope(typing.TypedDict):
    """The envelope carrying `pausing`."""

    api_version: int
    data: PausingReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["pausing"]


class PluginsEnvelope(typing.TypedDict):
    """The envelope carrying `plugins`."""

    api_version: int
    data: PluginInstalls
    host: typing.NotRequired[str | None]
    kind: typing.Literal["plugins"]


class PreviewEnvelope(typing.TypedDict):
    """The envelope carrying `preview`."""

    api_version: int
    data: Plan
    host: typing.NotRequired[str | None]
    kind: typing.Literal["preview"]


class ProvenanceEnvelope(typing.TypedDict):
    """The envelope carrying `provenance`."""

    api_version: int
    data: ProvenanceReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["provenance"]


class PullEnvelope(typing.TypedDict):
    """The envelope carrying `pull`."""

    api_version: int
    data: str
    host: typing.NotRequired[str | None]
    kind: typing.Literal["pull"]


class QualityEnvelope(typing.TypedDict):
    """The envelope carrying `quality`."""

    api_version: int
    data: QualityReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["quality"]


class RemovalEnvelope(typing.TypedDict):
    """The envelope carrying `removal`."""

    api_version: int
    data: HouseholdRemoval
    host: typing.NotRequired[str | None]
    kind: typing.Literal["removal"]


class RepairEnvelope(typing.TypedDict):
    """The envelope carrying `repair`."""

    api_version: int
    data: RepairReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["repair"]


class ReplacementEnvelope(typing.TypedDict):
    """The envelope carrying `replacement`."""

    api_version: int
    data: ReplaceReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["replacement"]


class ResetEnvelope(typing.TypedDict):
    """The envelope carrying `reset`."""

    api_version: int
    data: ResetReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["reset"]


class RestoreEnvelope(typing.TypedDict):
    """The envelope carrying `restore`."""

    api_version: int
    data: Restoration
    host: typing.NotRequired[str | None]
    kind: typing.Literal["restore"]


class SeedEnvelope(typing.TypedDict):
    """The envelope carrying `seed`."""

    api_version: int
    data: SeedReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["seed"]


class SelfUpdateEnvelope(typing.TypedDict):
    """The envelope carrying `self-update`."""

    api_version: int
    data: UpdateReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["self-update"]


class SetupEnvelope(typing.TypedDict):
    """The envelope carrying `setup`."""

    api_version: int
    data: SetupReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["setup"]


class SpaceEnvelope(typing.TypedDict):
    """The envelope carrying `space`."""

    api_version: int
    data: Reckoning
    host: typing.NotRequired[str | None]
    kind: typing.Literal["space"]


class StartEnvelope(typing.TypedDict):
    """The envelope carrying `start`."""

    api_version: int
    data: str
    host: typing.NotRequired[str | None]
    kind: typing.Literal["start"]


class StatusEnvelope(typing.TypedDict):
    """The envelope carrying `status`."""

    api_version: int
    data: StatusReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["status"]


class StepEnvelope(typing.TypedDict):
    """The envelope carrying `step`."""

    api_version: int
    data: Line
    host: typing.NotRequired[str | None]
    kind: typing.Literal["step"]


class StopSeedingEnvelope(typing.TypedDict):
    """The envelope carrying `stop-seeding`."""

    api_version: int
    data: Letting
    host: typing.NotRequired[str | None]
    kind: typing.Literal["stop-seeding"]


class StoredEnvelope(typing.TypedDict):
    """The envelope carrying `stored`."""

    api_version: int
    data: Stored
    host: typing.NotRequired[str | None]
    kind: typing.Literal["stored"]


class StuckEnvelope(typing.TypedDict):
    """The envelope carrying `stuck`."""

    api_version: int
    data: StuckReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["stuck"]


class SubstitutionEnvelope(typing.TypedDict):
    """The envelope carrying `substitution`."""

    api_version: int
    data: SubstitutionReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["substitution"]


class TraceEnvelope(typing.TypedDict):
    """The envelope carrying `trace`."""

    api_version: int
    data: TraceReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["trace"]


class UndoEnvelope(typing.TypedDict):
    """The envelope carrying `undo`."""

    api_version: int
    data: UndoReversal
    host: typing.NotRequired[str | None]
    kind: typing.Literal["undo"]


class UninstallEnvelope(typing.TypedDict):
    """The envelope carrying `uninstall`."""

    api_version: int
    data: Uninstall
    host: typing.NotRequired[str | None]
    kind: typing.Literal["uninstall"]


class UpdateEnvelope(typing.TypedDict):
    """The envelope carrying `update`."""

    api_version: int
    data: StackUpdateReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["update"]


class UpgradeEnvelope(typing.TypedDict):
    """The envelope carrying `upgrade`."""

    api_version: int
    data: UpgradeReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["upgrade"]


class VersionEnvelope(typing.TypedDict):
    """The envelope carrying `version`."""

    api_version: int
    data: VersionReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["version"]


class WalkthroughEnvelope(typing.TypedDict):
    """The envelope carrying `walkthrough`."""

    api_version: int
    data: WalkthroughReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["walkthrough"]


class WatchEnvelope(typing.TypedDict):
    """The envelope carrying `watch`."""

    api_version: int
    data: SupervisionReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["watch"]


class WiringEnvelope(typing.TypedDict):
    """The envelope carrying `wiring`."""

    api_version: int
    data: WiringReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["wiring"]


class WizardEnvelope(typing.TypedDict):
    """The envelope carrying `wizard`."""

    api_version: int
    data: WizardReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["wizard"]


class WordEnvelope(typing.TypedDict):
    """The envelope carrying `word`."""

    api_version: int
    data: Term
    host: typing.NotRequired[str | None]
    kind: typing.Literal["word"]


type Kind = typing.Literal[
    "admission",
    "adoption",
    "alerts",
    "archives",
    "backup",
    "bandwidth",
    "beside",
    "bundle",
    "capabilities",
    "catalogue",
    "certificate",
    "clients",
    "config",
    "credentials",
    "dashboard",
    "doctor",
    "error",
    "forms",
    "front-door",
    "glossary",
    "handoff",
    "held",
    "history",
    "hosting",
    "household",
    "import",
    "invitation",
    "job",
    "keys",
    "lifecycle",
    "log",
    "migration",
    "minted-key",
    "music",
    "news",
    "news-items",
    "outbound",
    "pairing",
    "pausing",
    "plugins",
    "preview",
    "provenance",
    "pull",
    "quality",
    "removal",
    "repair",
    "replacement",
    "reset",
    "restore",
    "seed",
    "self-update",
    "setup",
    "space",
    "start",
    "status",
    "step",
    "stop-seeding",
    "stored",
    "stuck",
    "substitution",
    "trace",
    "undo",
    "uninstall",
    "update",
    "upgrade",
    "version",
    "walkthrough",
    "watch",
    "wiring",
    "wizard",
    "word",
]
"""The name of every kind the server may send."""

KINDS: typing.Final[frozenset[Kind]] = frozenset(
    (
        "admission",
        "adoption",
        "alerts",
        "archives",
        "backup",
        "bandwidth",
        "beside",
        "bundle",
        "capabilities",
        "catalogue",
        "certificate",
        "clients",
        "config",
        "credentials",
        "dashboard",
        "doctor",
        "error",
        "forms",
        "front-door",
        "glossary",
        "handoff",
        "held",
        "history",
        "hosting",
        "household",
        "import",
        "invitation",
        "job",
        "keys",
        "lifecycle",
        "log",
        "migration",
        "minted-key",
        "music",
        "news",
        "news-items",
        "outbound",
        "pairing",
        "pausing",
        "plugins",
        "preview",
        "provenance",
        "pull",
        "quality",
        "removal",
        "repair",
        "replacement",
        "reset",
        "restore",
        "seed",
        "self-update",
        "setup",
        "space",
        "start",
        "status",
        "step",
        "stop-seeding",
        "stored",
        "stuck",
        "substitution",
        "trace",
        "undo",
        "uninstall",
        "update",
        "upgrade",
        "version",
        "walkthrough",
        "watch",
        "wiring",
        "wizard",
        "word",
    )
)
"""Every kind the server may send."""

type Envelope = (
    AdmissionEnvelope
    | AdoptionEnvelope
    | AlertsEnvelope
    | ArchivesEnvelope
    | BackupEnvelope
    | BandwidthEnvelope
    | BesideEnvelope
    | BundleEnvelope
    | CapabilitiesEnvelope
    | CatalogueEnvelope
    | CertificateEnvelope
    | ClientsEnvelope
    | ConfigEnvelope
    | CredentialsEnvelope
    | DashboardEnvelope
    | DoctorEnvelope
    | ErrorEnvelope
    | FormsEnvelope
    | FrontDoorEnvelope
    | GlossaryEnvelope
    | HandoffEnvelope
    | HeldEnvelope
    | HistoryEnvelope
    | HostingEnvelope
    | HouseholdEnvelope
    | ImportEnvelope
    | InvitationEnvelope
    | JobEnvelope
    | KeysEnvelope
    | LifecycleEnvelope
    | LogEnvelope
    | MigrationEnvelope
    | MintedKeyEnvelope
    | MusicEnvelope
    | NewsEnvelope
    | NewsItemsEnvelope
    | OutboundEnvelope
    | PairingEnvelope
    | PausingEnvelope
    | PluginsEnvelope
    | PreviewEnvelope
    | ProvenanceEnvelope
    | PullEnvelope
    | QualityEnvelope
    | RemovalEnvelope
    | RepairEnvelope
    | ReplacementEnvelope
    | ResetEnvelope
    | RestoreEnvelope
    | SeedEnvelope
    | SelfUpdateEnvelope
    | SetupEnvelope
    | SpaceEnvelope
    | StartEnvelope
    | StatusEnvelope
    | StepEnvelope
    | StopSeedingEnvelope
    | StoredEnvelope
    | StuckEnvelope
    | SubstitutionEnvelope
    | TraceEnvelope
    | UndoEnvelope
    | UninstallEnvelope
    | UpdateEnvelope
    | UpgradeEnvelope
    | VersionEnvelope
    | WalkthroughEnvelope
    | WatchEnvelope
    | WiringEnvelope
    | WizardEnvelope
    | WordEnvelope
)
"""The envelope of any kind, told apart by its `kind`."""


class KindNarrowing(typing.Protocol):
    """Narrows an envelope to the one kind it is expected to be."""

    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["admission"], /) -> AdmissionEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["adoption"], /) -> AdoptionEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["alerts"], /) -> AlertsEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["archives"], /) -> ArchivesEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["backup"], /) -> BackupEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["bandwidth"], /) -> BandwidthEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["beside"], /) -> BesideEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["bundle"], /) -> BundleEnvelope: ...
    @typing.overload
    def __call__(
        self, envelope: Envelope, kind: typing.Literal["capabilities"], /
    ) -> CapabilitiesEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["catalogue"], /) -> CatalogueEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["certificate"], /) -> CertificateEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["clients"], /) -> ClientsEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["config"], /) -> ConfigEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["credentials"], /) -> CredentialsEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["dashboard"], /) -> DashboardEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["doctor"], /) -> DoctorEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["error"], /) -> ErrorEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["forms"], /) -> FormsEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["front-door"], /) -> FrontDoorEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["glossary"], /) -> GlossaryEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["handoff"], /) -> HandoffEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["held"], /) -> HeldEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["history"], /) -> HistoryEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["hosting"], /) -> HostingEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["household"], /) -> HouseholdEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["import"], /) -> ImportEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["invitation"], /) -> InvitationEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["job"], /) -> JobEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["keys"], /) -> KeysEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["lifecycle"], /) -> LifecycleEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["log"], /) -> LogEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["migration"], /) -> MigrationEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["minted-key"], /) -> MintedKeyEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["music"], /) -> MusicEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["news"], /) -> NewsEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["news-items"], /) -> NewsItemsEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["outbound"], /) -> OutboundEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["pairing"], /) -> PairingEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["pausing"], /) -> PausingEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["plugins"], /) -> PluginsEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["preview"], /) -> PreviewEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["provenance"], /) -> ProvenanceEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["pull"], /) -> PullEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["quality"], /) -> QualityEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["removal"], /) -> RemovalEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["repair"], /) -> RepairEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["replacement"], /) -> ReplacementEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["reset"], /) -> ResetEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["restore"], /) -> RestoreEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["seed"], /) -> SeedEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["self-update"], /) -> SelfUpdateEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["setup"], /) -> SetupEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["space"], /) -> SpaceEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["start"], /) -> StartEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["status"], /) -> StatusEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["step"], /) -> StepEnvelope: ...
    @typing.overload
    def __call__(
        self, envelope: Envelope, kind: typing.Literal["stop-seeding"], /
    ) -> StopSeedingEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["stored"], /) -> StoredEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["stuck"], /) -> StuckEnvelope: ...
    @typing.overload
    def __call__(
        self, envelope: Envelope, kind: typing.Literal["substitution"], /
    ) -> SubstitutionEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["trace"], /) -> TraceEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["undo"], /) -> UndoEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["uninstall"], /) -> UninstallEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["update"], /) -> UpdateEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["upgrade"], /) -> UpgradeEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["version"], /) -> VersionEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["walkthrough"], /) -> WalkthroughEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["watch"], /) -> WatchEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["wiring"], /) -> WiringEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["wizard"], /) -> WizardEnvelope: ...
    @typing.overload
    def __call__(self, envelope: Envelope, kind: typing.Literal["word"], /) -> WordEnvelope: ...


type RefusalCode = typing.Literal[
    "ADMIT-10",
    "ADMIT-11",
    "ADMIT-12",
    "ADMIT-4",
    "ADMIT-5",
    "ADMIT-6",
    "ADMIT-7",
    "ADMIT-8",
    "ADMIT-9",
    "ASK-1",
    "ASK-10",
    "ASK-11",
    "ASK-2",
    "ASK-3",
    "ASK-4",
    "ASK-5",
    "ASK-6",
    "ASK-7",
    "ASK-8",
    "ASK-9",
    "GONE-2",
    "MIGRATE-1",
    "PLUGIN-10",
    "PLUGIN-11",
    "PLUGIN-12",
    "PLUGIN-13",
    "PLUGIN-14",
    "PLUGIN-15",
    "PLUGIN-16",
    "PLUGIN-17",
    "PLUGIN-18",
    "PLUGIN-19",
    "PLUGIN-2",
    "PLUGIN-20",
    "PLUGIN-21",
    "PLUGIN-22",
    "PLUGIN-23",
    "PLUGIN-24",
    "PLUGIN-25",
    "PLUGIN-26",
    "PLUGIN-27",
    "PLUGIN-28",
    "PLUGIN-29",
    "PLUGIN-3",
    "PLUGIN-30",
    "PLUGIN-31",
    "PLUGIN-32",
    "PLUGIN-4",
    "PLUGIN-5",
    "PLUGIN-6",
    "PLUGIN-7",
    "PLUGIN-8",
    "PLUGIN-9",
    "READ-1",
    "READ-10",
    "READ-11",
    "READ-12",
    "READ-13",
    "READ-14",
    "READ-15",
    "READ-16",
    "READ-2",
    "READ-3",
    "READ-4",
    "READ-5",
    "READ-6",
    "READ-7",
    "READ-8",
    "READ-9",
    "REPAIR-1",
    "RESTORE-11",
    "SERVE-6",
    "SERVE-7",
    "SPACE-6",
    "STACK-1",
    "STACK-2",
    "STACK-3",
    "STACK-4",
    "STACK-5",
    "STACK-6",
    "STACK-7",
    "STACK-8",
    "STACK-9",
    "WIRE-1",
    "WIRE-2",
    "WIRE-3",
    "WIRE-4",
    "WIRE-5",
    "WIRE-6",
]
"""Every code a refusal may carry."""


class ListedRefusal(typing.NamedTuple):
    """What the contract says of one refusal code."""

    name: str
    """The code's name in the core's registry."""
    status: int
    """The one status the refusal is answered with."""
    description: str
    """The registry's own line about it."""


REFUSAL_CODES: typing.Final[typing.Mapping[RefusalCode, ListedRefusal]] = types.MappingProxyType(
    {
        "ADMIT-10": ListedRefusal(
            "NOT_A_PASSWORD", 400, "Raised when what was offered at the door is not a password."
        ),
        "ADMIT-11": ListedRefusal(
            "KEY_IN_THE_CLEAR",
            403,
            "Raised when a key arrived from another machine over a connection its pin does not verify.",
        ),
        "ADMIT-12": ListedRefusal(
            "NOT_FOR_A_KEY", 403, "Raised when a key asked for something its scope does not reach."
        ),
        "ADMIT-4": ListedRefusal(
            "NOT_ADMITTED", 403, "Raised when a request carried no token, session or key this run admits."
        ),
        "ADMIT-5": ListedRefusal(
            "ELSEWHERE", 403, "Raised when a request said it came from somewhere this server is not."
        ),
        "ADMIT-6": ListedRefusal(
            "NOT_YOURS", 403, "Raised when an account asked for something that is not its to ask for."
        ),
        "ADMIT-7": ListedRefusal(
            "UNCONFIRMED", 403, "Raised when the media server could not say whether an account is still one."
        ),
        "ADMIT-8": ListedRefusal(
            "NOT_THE_PASSWORD", 401, "Raised when the password offered at the door was wrong, or none is set."
        ),
        "ADMIT-9": ListedRefusal(
            "TOO_MANY_ATTEMPTS", 429, "Raised when the door has been given too many wrong passwords lately."
        ),
        "ASK-1": ListedRefusal(
            "NO_SUCH_ACTION", 404, "Raised where no action goes by the name that was asked for."
        ),
        "ASK-10": ListedRefusal(
            "WRONG_METHOD", 405, "Raised where an endpoint was asked with a method it does not answer."
        ),
        "ASK-11": ListedRefusal(
            "NOT_A_KEY_REQUEST",
            400,
            "Raised where the body of a mint is not a key's name, scope, purpose and the password.",
        ),
        "ASK-2": ListedRefusal(
            "MISSING_ARGUMENT", 400, "Raised where an action was not given an argument it needs."
        ),
        "ASK-3": ListedRefusal(
            "UNRECOGNISED_ARGUMENT", 400, "Raised where an argument was given a value that names nothing."
        ),
        "ASK-4": ListedRefusal(
            "UNWANTED_ARGUMENT",
            400,
            "Raised where an action was given an argument its command has nowhere to put.",
        ),
        "ASK-5": ListedRefusal(
            "ARGUMENTS_TOGETHER",
            400,
            "Raised where two arguments that each name a different request arrived together.",
        ),
        "ASK-6": ListedRefusal(
            "NOT_ARGUMENTS", 400, "Raised where the body of an action is not arguments it can read."
        ),
        "ASK-7": ListedRefusal(
            "NO_SUCH_JOB", 404, "Raised where a job was asked about that this run did not start."
        ),
        "ASK-8": ListedRefusal(
            "NOT_AN_ANSWER", 400, "Raised where the body of a setup step is not an answer it can read."
        ),
        "ASK-9": ListedRefusal(
            "NO_ENDPOINT", 404, "Raised where a path under the endpoints is one no endpoint answers."
        ),
        "GONE-2": ListedRefusal(
            "ANOTHER_READING",
            400,
            "Raised when an agreement names a reading of this machine that is not the one standing now.",
        ),
        "MIGRATE-1": ListedRefusal(
            "OFFER_MOVED",
            400,
            "Raised when a replacement was agreed to for an offer that is not the one standing now.",
        ),
        "PLUGIN-10": ListedRefusal(
            "NOTHING_TO_REMOVE", 404, "Nothing by that name is installed on this machine."
        ),
        "PLUGIN-11": ListedRefusal(
            "NOTHING_TO_UPDATE", 404, "Nothing by that id is installed, so there is no version to replace."
        ),
        "PLUGIN-12": ListedRefusal(
            "STUCK", 500, "The version installed would not come off, so nothing else was touched."
        ),
        "PLUGIN-13": ListedRefusal(
            "ANSWERED",
            400,
            "Raised when a plugin's service would answer on a label another plugin's already does.",
        ),
        "PLUGIN-14": ListedRefusal(
            "TWO_SOURCES",
            400,
            "Raised when a plugin is installed from a source other than the one its name is already installed from.",
        ),
        "PLUGIN-15": ListedRefusal(
            "SOURCE_OFF",
            400,
            "Raised when a plugin is named from a git source and fetching from one is switched off.",
        ),
        "PLUGIN-16": ListedRefusal(
            "UNFETCHED",
            500,
            "Raised when a git source could not be reached or would not hand over a revision.",
        ),
        "PLUGIN-17": ListedRefusal(
            "NO_REVISION", 404, "Raised when a git source holds no branch, tag or commit by the name given."
        ),
        "PLUGIN-18": ListedRefusal(
            "CATALOGUE_OFF",
            400,
            "Raised when a plugin is installed by name and asking the catalogue is switched off.",
        ),
        "PLUGIN-19": ListedRefusal(
            "CATALOGUE_UNREACHABLE",
            500,
            "Raised when the catalogue's index or its signature could not be fetched.",
        ),
        "PLUGIN-2": ListedRefusal("UNREADABLE", 404, "The source names no plugin this build can read."),
        "PLUGIN-20": ListedRefusal(
            "SIGNATURE_UNVERIFIED",
            500,
            "Raised when the catalogue's index has no signature, one that does not verify, or none this build carries a key to check.",
        ),
        "PLUGIN-21": ListedRefusal(
            "CATALOGUE_UNREADABLE",
            500,
            "Raised when the catalogue's index verified and is not one this build reads.",
        ),
        "PLUGIN-22": ListedRefusal(
            "NOT_CATALOGUED", 404, "Raised when the catalogue holds no plugin by the name given."
        ),
        "PLUGIN-23": ListedRefusal(
            "NOT_AS_REVIEWED",
            500,
            "Raised when what the catalogue's origin served is not what the catalogue reviewed.",
        ),
        "PLUGIN-24": ListedRefusal(
            "SPELLED_ALIKE",
            400,
            "Raised when a plugin's service would be named, where lemonfiber keeps what a service holds, as another installed plugin's service already is.",
        ),
        "PLUGIN-25": ListedRefusal(
            "PLUGIN_OFFER_MOVED",
            400,
            "Raised when an install, an update or a removal answers an offer that was read against a plugin, a stack or a record that has since moved.",
        ),
        "PLUGIN-26": ListedRefusal(
            "UNAPPROVED",
            400,
            "Raised when a value a recipe would carry to a destination was not approved as itself, or an approval names a pair the recipe does not carry.",
        ),
        "PLUGIN-27": ListedRefusal(
            "ANOTHER_PLUGIN",
            400,
            "Raised when the source an update names holds a different plugin from the one it was asked to update.",
        ),
        "PLUGIN-28": ListedRefusal(
            "OCCUPIED",
            400,
            "Raised when a plugin's service would take a name, a port or a label something already on this machine holds: a service of the stack or of the operator's overlay, another plugin's port, or a site in the proxy's live configuration.",
        ),
        "PLUGIN-29": ListedRefusal(
            "CATALOGUE_REPLACED",
            500,
            "Raised when the catalogue's index verifies and is older than the newest one this machine has verified.",
        ),
        "PLUGIN-3": ListedRefusal(
            "REFUSED", 400, "The manifest is read and this build refuses what it declares."
        ),
        "PLUGIN-30": ListedRefusal(
            "NEWEST_UNKEPT",
            500,
            "Raised when the record of the newest catalogue index this machine verified cannot be read or written.",
        ),
        "PLUGIN-31": ListedRefusal(
            "SCHEME_REFUSED",
            400,
            "Raised when a git source is named over a transport other than https, before anything is asked of it.",
        ),
        "PLUGIN-32": ListedRefusal(
            "ADDRESS_REFUSED",
            400,
            "Raised when a git source's host is, or stands for, an address on this machine or on a network of its own: loopback, private, link-local or unspecified.",
        ),
        "PLUGIN-4": ListedRefusal("UNRECORDED", 500, "The record of what is installed cannot be read."),
        "PLUGIN-5": ListedRefusal("ALREADY", 400, "The plugin is installed already."),
        "PLUGIN-6": ListedRefusal(
            "NOWHERE", 500, "There is no stack on this machine to put a plugin's container in."
        ),
        "PLUGIN-7": ListedRefusal(
            "UNWRITABLE", 500, "A directory or a document the install decided on would not land."
        ),
        "PLUGIN-8": ListedRefusal(
            "UNRECORDABLE", 500, "The wiring went down and the record of what is installed did not."
        ),
        "PLUGIN-9": ListedRefusal(
            "UNPROVED", 500, "The plugin's own service would not start, so nothing about it could be proved."
        ),
        "READ-1": ListedRefusal(
            "UNWANTED", 400, "Raised where a read was given a parameter its answer has nowhere to put."
        ),
        "READ-10": ListedRefusal(
            "TOO_MANY_AT_ONCE", 400, "Raised where more holdings were asked for than one read answers with."
        ),
        "READ-11": ListedRefusal(
            "NO_SUCH_GROUP", 400, "Raised where a diagnosis was narrowed to a group or check that is not one."
        ),
        "READ-12": ListedRefusal(
            "NO_SUCH_REMOVAL", 400, "Raised where a removal was named that is none of the four there are."
        ),
        "READ-13": ListedRefusal(
            "NO_UPDATE_OBJECT",
            400,
            "Raised where moving forward was asked about and neither stack nor self named.",
        ),
        "READ-14": ListedRefusal(
            "NOT_A_LINE_COUNT",
            400,
            "Raised where how many log lines to begin with is not a number within the ceiling.",
        ),
        "READ-15": ListedRefusal(
            "NOT_A_CHOICE",
            400,
            "Raised where a parameter that takes a yes or a no is neither true nor false.",
        ),
        "READ-16": ListedRefusal(
            "MEMBER_AND_DEFAULTS",
            400,
            "Raised where a household read named a member and asked for the household's defaults as well.",
        ),
        "READ-2": ListedRefusal(
            "REPEATED", 400, "Raised where a parameter carrying one value was given more than once."
        ),
        "READ-3": ListedRefusal(
            "NO_SUCH_READ", 404, "Raised where no read goes by the name that was asked for."
        ),
        "READ-4": ListedRefusal(
            "NO_TERM", 400, "Raised where a trace was asked for and named nothing to follow."
        ),
        "READ-5": ListedRefusal(
            "NOT_A_SEASON", 400, "Raised where the season to narrow a trace to is not a number."
        ),
        "READ-6": ListedRefusal("NO_SETTING", 400, "Raised where a setting was asked for by an empty name."),
        "READ-7": ListedRefusal(
            "NO_MEMBER", 400, "Raised where a household member was asked for by an empty name."
        ),
        "READ-8": ListedRefusal(
            "NO_SHELF_WITHOUT_A_MEMBER",
            400,
            "Raised where a shelf was asked for and nobody was named whose it is.",
        ),
        "READ-9": ListedRefusal(
            "NOT_A_COUNT", 400, "Raised where how many holdings to answer with is not a whole number."
        ),
        "REPAIR-1": ListedRefusal(
            "STALE", 400, "Raised when consent was given for an offer that no longer stands."
        ),
        "RESTORE-11": ListedRefusal(
            "MOVED_ON", 400, "Raised when consent was given for a listing that no longer stands."
        ),
        "SERVE-6": ListedRefusal("UNRENDERABLE", 500, "Raised when an answer could not be rendered."),
        "SERVE-7": ListedRefusal(
            "NO_JOB_NAME", 500, "Raised when this machine will not supply the randomness a job is named with."
        ),
        "SPACE-6": ListedRefusal(
            "ANOTHER_OFFER", 400, "Raised when an agreement names an offer that is not the one standing now."
        ),
        "STACK-1": ListedRefusal(
            "STACK_UNREADABLE", 500, "Raised when a stack directory holds no readable manifest."
        ),
        "STACK-2": ListedRefusal(
            "STACK_UNUSABLE", 500, "Raised when a manifest is readable and this build cannot use it."
        ),
        "STACK-3": ListedRefusal("STACK_NOT_EMBEDDED", 500, "Raised when the embedded stack is not intact."),
        "STACK-4": ListedRefusal(
            "STACK_NOT_SET_UP", 500, "Raised when lemonfiber has nowhere to write the stack."
        ),
        "STACK-5": ListedRefusal(
            "STACK_NOT_WRITTEN", 500, "Raised when the stack could not be written to disk."
        ),
        "STACK-6": ListedRefusal(
            "STACK_INVALID", 500, "Raised when a manifest parses and breaks the contract."
        ),
        "STACK-7": ListedRefusal("STACK_MALFORMED", 500, "Raised when a manifest is not TOML at all."),
        "STACK-8": ListedRefusal(
            "STACK_UNRECOGNISED", 500, "Raised when a manifest declares names this build does not know."
        ),
        "STACK-9": ListedRefusal(
            "STACK_NEEDS_NEWER", 500, "Raised when a stack names a newer lemonfiber than the one running."
        ),
        "WIRE-1": ListedRefusal(
            "NO_SUCH_FILLER", 404, "A capability was named that no service in this stack provides."
        ),
        "WIRE-2": ListedRefusal(
            "CANNOT_FILL", 400, "The service named cannot do the thing it was asked to fill."
        ),
        "WIRE-3": ListedRefusal(
            "NOTHING_ASKS",
            400,
            "Nothing in this stack asks for the capability, so a choice would change nothing.",
        ),
        "WIRE-4": ListedRefusal(
            "CHOICE_UNWRITABLE", 500, "The setting recording the choice could not be written."
        ),
        "WIRE-5": ListedRefusal(
            "WIRING_MOVED",
            400,
            "Raised when a choice answers an offer that was read against a wiring that has since moved.",
        ),
        "WIRE-6": ListedRefusal(
            "UNREASONABLE",
            400,
            "Raised when the reason given for a choice is longer than a reason may be, or holds a line break or another control character.",
        ),
    }
)
"""What the contract says of each refusal code."""


def is_refusal_code(value: str) -> typing.TypeIs[RefusalCode]:
    """Tell whether a code is one the contract lists as a refusal's."""
    return value in REFUSAL_CODES


type KeyCallableAction = typing.Literal[
    "restart", "diagnose", "update", "downloads-pause", "downloads-resume"
]
"""Every action a key may call; any other is refused to a key, naming its scope."""


class KeyCallable(typing.NamedTuple):
    """What the contract says of one action a key may call."""

    disturbs: bool
    """Whether calling it disturbs the running system."""
    rehearsal: bool
    """Whether it takes `dry_run`, so it can be rehearsed before the real call is offered."""


KEY_CALLABLE: typing.Final[typing.Mapping[KeyCallableAction, KeyCallable]] = types.MappingProxyType(
    {
        "restart": KeyCallable(True, True),
        "diagnose": KeyCallable(True, False),
        "update": KeyCallable(True, True),
        "downloads-pause": KeyCallable(False, True),
        "downloads-resume": KeyCallable(False, True),
    }
)
"""What the contract says of each action a key may call, in the order it lists them."""


def is_key_callable(value: str) -> typing.TypeIs[KeyCallableAction]:
    """Tell whether an action is one the contract says a key may call."""
    return value in KEY_CALLABLE


__all__ = [
    "Action",
    "ActionDelete",
    "ActionReconfigure",
    "ActionReinstate",
    "ActionRemove",
    "ActionRepin",
    "ActionRestore",
    "ActionRevoke",
    "ActionWithdraw",
    "Active",
    "Address",
    "AdmissionEnvelope",
    "Admitted",
    "AdoptReport",
    "AdoptionEnvelope",
    "Affected",
    "Alert",
    "AlertReport",
    "AlertsEnvelope",
    "Answer",
    "AnswerHeld",
    "AnswerSilent",
    "Api",
    "ApiKind",
    "ArchivesEnvelope",
    "AskingStanding",
    "Assessment",
    "Awaiting",
    "BackupEnvelope",
    "BackupManifest",
    "BackupReport",
    "BandwidthEnvelope",
    "BandwidthHeld",
    "BandwidthReading",
    "BandwidthVerdict",
    "BesideEnvelope",
    "BesideReport",
    "Beyond",
    "Bundle",
    "BundleEnvelope",
    "CONTRACT_API_VERSION",
    "Candidate",
    "Cap",
    "Capabilities",
    "CapabilitiesEnvelope",
    "CapabilityState",
    "Capacity",
    "CarryingReport",
    "CatalogueEnvelope",
    "CatalogueReport",
    "CataloguedService",
    "Cause",
    "CertificateEnvelope",
    "CertificateReport",
    "ChangeReport",
    "ChangeReversal",
    "Changed",
    "ChangelogState",
    "Chosen",
    "ChosenDerived",
    "ChosenNamed",
    "ChosenRefused",
    "ClientsEnvelope",
    "Code",
    "Coming",
    "Condition",
    "ConfigChange",
    "ConfigEnvelope",
    "ConfigReport",
    "ConflictReport",
    "Consumption",
    "Contents",
    "Contribution",
    "Cost",
    "Counted",
    "Coverage",
    "CredentialHeld",
    "CredentialReach",
    "CredentialReachFailed",
    "CredentialReachPending",
    "CredentialReachUpdated",
    "CredentialState",
    "CredentialsEnvelope",
    "Criticality",
    "DashboardEnvelope",
    "DashboardProtocol",
    "DashboardReading",
    "DashboardReadingKnown",
    "DashboardReadingStale",
    "DashboardReadingUnknown",
    "Device",
    "Disposition",
    "Disturbances",
    "DoctorCategory",
    "DoctorEnvelope",
    "DoctorReport",
    "DoctorVerdict",
    "DoctorVerdictFail",
    "DoctorVerdictPass",
    "DoctorVerdictSkipped",
    "DoctorVerdictUnverified",
    "DoctorVerdictWarn",
    "Dropped",
    "Duration",
    "Edited",
    "Elsewhere",
    "Ending",
    "Entry",
    "Envelope",
    "ErrorEnvelope",
    "Estimate",
    "ExceptionReport",
    "Expect",
    "Expected",
    "ExpectedKind",
    "Facing",
    "Filenames",
    "Filtered",
    "Finding",
    "Findings",
    "Footprint",
    "Foreign",
    "FormReport",
    "FormsEnvelope",
    "FormsReport",
    "Freshness",
    "FreshnessAsOf",
    "FreshnessLive",
    "FrontDoorBeside",
    "FrontDoorEnvelope",
    "FrontDoorReport",
    "FrontDoorStanding",
    "GlossaryEnvelope",
    "Gone",
    "Group",
    "Guidance",
    "HandoffClient",
    "HandoffEnvelope",
    "HandoffRemedy",
    "HandoffReport",
    "HandoffSession",
    "HandoffState",
    "Handover",
    "Hardlink",
    "HealthStanding",
    "HealthSummary",
    "Held",
    "HeldEnvelope",
    "HeldReport",
    "HistoryEnvelope",
    "HistoryReport",
    "Holding",
    "HostedCommand",
    "Hosting",
    "HostingEnvelope",
    "HostingReport",
    "HouseholdEnvelope",
    "HouseholdMember",
    "HouseholdRemoval",
    "HouseholdReport",
    "ImportEnvelope",
    "ImportReport",
    "Installed",
    "Interrupted",
    "Inventory",
    "Invitation",
    "InvitationApplied",
    "InvitationEnvelope",
    "InvitationStanding",
    "Item",
    "JobEnvelope",
    "Jump",
    "KEY_CALLABLE",
    "KINDS",
    "Kept",
    "KeyCallable",
    "KeyCallableAction",
    "KeyListing",
    "KeyPurpose",
    "KeySource",
    "KeyState",
    "KeysEnvelope",
    "Kind",
    "KindNarrowing",
    "Leaving",
    "Letting",
    "Level",
    "LibraryPath",
    "LifecycleEnvelope",
    "LifecycleReport",
    "Limit",
    "LimitAbsolute",
    "LimitShare",
    "LimitUnlimited",
    "Line",
    "Link",
    "Linked",
    "LinkingReport",
    "ListedKey",
    "ListedRefusal",
    "Listing",
    "LogEnvelope",
    "LogLevel",
    "LogLine",
    "Manager",
    "Medium",
    "Member",
    "MemberAccess",
    "MemberAsking",
    "MemberRequest",
    "MemberStanding",
    "Mended",
    "Metered",
    "MigrationEnvelope",
    "MigrationReport",
    "MintedKey",
    "MintedKeyEnvelope",
    "ModeReport",
    "Moment",
    "MovedReport",
    "MusicChoice",
    "MusicEnvelope",
    "MusicReport",
    "Newest",
    "News",
    "NewsCheck",
    "NewsEnvelope",
    "NewsItemsEnvelope",
    "NewsKind",
    "NewsProblem",
    "NewsRequest",
    "NewsUpdate",
    "Next",
    "Notes",
    "OccupantReport",
    "Opening",
    "Origin",
    "Outbound",
    "OutboundEnvelope",
    "OutboundReach",
    "Outside",
    "Outsized",
    "Overall",
    "Pace",
    "Pairing",
    "PairingEnvelope",
    "PairingMaterial",
    "PanelArray_of_Queue",
    "PanelArray_of_QueueReady",
    "PanelArray_of_QueueUnavailable",
    "PanelArray_of_QueueUnavailableData",
    "PanelArray_of_Service",
    "PanelArray_of_ServiceReady",
    "PanelArray_of_ServiceUnavailable",
    "PanelArray_of_ServiceUnavailableData",
    "PanelArray_of_Transfer",
    "PanelArray_of_TransferReady",
    "PanelArray_of_TransferUnavailable",
    "PanelArray_of_TransferUnavailableData",
    "PanelFrontDoorReport",
    "PanelFrontDoorReportReady",
    "PanelFrontDoorReportUnavailable",
    "PanelFrontDoorReportUnavailableData",
    "PanelHouseholdReport",
    "PanelHouseholdReportReady",
    "PanelHouseholdReportUnavailable",
    "PanelHouseholdReportUnavailableData",
    "PanelStorage",
    "PanelStorageReady",
    "PanelStorageUnavailable",
    "PanelStorageUnavailableData",
    "PanelVpn",
    "PanelVpnReady",
    "PanelVpnUnavailable",
    "PanelVpnUnavailableData",
    "Part",
    "Passed",
    "PausedClient",
    "Pausing",
    "PausingEnvelope",
    "PausingReport",
    "Period",
    "Phase",
    "Piece",
    "Plan",
    "PluginAdapterOwner",
    "PluginChange",
    "PluginChangedCheck",
    "PluginConstraint",
    "PluginDeclaration",
    "PluginDeclaredVerdict",
    "PluginEvidence",
    "PluginExpectedFailure",
    "PluginFailingAsDeclared",
    "PluginInstall",
    "PluginInstalled",
    "PluginInstalls",
    "PluginOverriding",
    "PluginPair",
    "PluginPlaced",
    "PluginProving",
    "PluginPuts",
    "PluginReached",
    "PluginReachedHousehold",
    "PluginReachedLoopback",
    "PluginRecipe",
    "PluginRemoval",
    "PluginRequest",
    "PluginRestored",
    "PluginSecret",
    "PluginServiceAdapter",
    "PluginSource",
    "PluginSourceStanding",
    "PluginSourceStandingReachable",
    "PluginSourceStandingUnasked",
    "PluginSourceStandingUnreachable",
    "PluginStep",
    "PluginStepAdapter",
    "PluginSubstituted",
    "PluginUnfilled",
    "PluginUpdate",
    "PluginVerdict",
    "PluginVerdictFailed",
    "PluginVerdictFailingAsDeclared",
    "PluginVerdictPassed",
    "PluginVerdictUnproven",
    "PluginVerification",
    "PluginsEnvelope",
    "Policy",
    "PresetChoice",
    "Preview",
    "PreviewEnvelope",
    "Problem",
    "ProblemSeverity",
    "ProblemState",
    "Propagation",
    "Protection",
    "Protocols",
    "ProvenanceEnvelope",
    "ProvenanceReport",
    "PullEnvelope",
    "Pulling",
    "QualityEnvelope",
    "QualityReport",
    "Queue",
    "REFUSAL_CODES",
    "Ran",
    "Rated",
    "Reached",
    "Reaches",
    "ReachesAsked",
    "ReachesByName",
    "Reason",
    "Reckoning",
    "Reclaim",
    "Reclaimed",
    "RecordReport",
    "Refusal",
    "RefusalCode",
    "Refused",
    "Release",
    "ReleaseSummary",
    "Relocation",
    "Remedy",
    "RemovalEnvelope",
    "RemovedService",
    "Repair",
    "RepairEnvelope",
    "RepairOutcome",
    "RepairOutcomeDeclined",
    "RepairOutcomeFixFailed",
    "RepairOutcomeFixed",
    "RepairOutcomeStopped",
    "RepairOutcomeUnmanaged",
    "RepairOutcomeWouldOverwrite",
    "RepairReport",
    "ReplaceReport",
    "ReplacementEnvelope",
    "RequestState",
    "Requirement",
    "ResetEnvelope",
    "ResetReport",
    "Resolved",
    "ResolvedAt",
    "ResolvedUnlimited",
    "ResolvedUnmeasured",
    "RespiteStanding",
    "RespiteStandingExpired",
    "RespiteStandingInForce",
    "RespiteStandingNone",
    "Restoration",
    "RestoreEnvelope",
    "RestoreReport",
    "Restraint",
    "Restriction",
    "Revealed",
    "Review",
    "Revoked",
    "Rhythm",
    "Role",
    "Root",
    "Rotation",
    "Scope",
    "ScopeExisting",
    "ScopeService",
    "ScopeWholeStack",
    "SeasonCoverage",
    "Secret",
    "SeedEnvelope",
    "SeedReport",
    "SeedSeverity",
    "SeedSeverityInformational",
    "SeedSeverityWarning",
    "SeedState",
    "SeedStateAdopted",
    "SeedStateAlreadyWired",
    "SeedStateConflicted",
    "SeedStateDrifted",
    "SeedStateFailed",
    "SeedStateObserved",
    "SeedStateRefused",
    "SeedStateSkipped",
    "SeedStateStale",
    "SeedStateUnmanaged",
    "SeedStateUnmatched",
    "SeedStateWired",
    "SeedStateWouldAdopt",
    "SeedStateWouldWire",
    "SeedingStanding",
    "SeedingStandingLeftAlone",
    "SeedingStandingNeverImported",
    "SeedingStandingSeeding",
    "SelfUpdateEnvelope",
    "SelfUpdateStanding",
    "Service",
    "ServiceProvenance",
    "ServiceState",
    "SettingReport",
    "Settled",
    "SettledElsewhere",
    "SettledRefused",
    "SettledRehearsed",
    "SettledReplaced",
    "SettledReplacedUnproven",
    "SettledUnknown",
    "SettledUnproven",
    "SetupEnvelope",
    "SetupOutcome",
    "SetupReport",
    "Shape",
    "Sharing",
    "Snapshot",
    "Sort",
    "Source",
    "SpaceCategory",
    "SpaceCategoryExtracted",
    "SpaceCategoryLanding",
    "SpaceCategoryOrphaned",
    "SpaceCategorySeeding",
    "SpaceCategoryServices",
    "SpaceCategoryTree",
    "SpaceCategoryUnmanaged",
    "SpaceEnvelope",
    "SpaceLeft",
    "StackEdit",
    "StackProtocol",
    "StackUpdateReport",
    "Stage",
    "Stall",
    "Stance",
    "StandingReport",
    "StartEnvelope",
    "Started",
    "StatusEnvelope",
    "StatusReport",
    "StepEnvelope",
    "StopSeedingEnvelope",
    "Stopped",
    "Storage",
    "Stored",
    "StoredBeside",
    "StoredEnvelope",
    "StoredLeft",
    "StoredRemoval",
    "StoredRemovalDone",
    "StoredRemovalNotAsked",
    "StoredRemovalUnconfirmed",
    "Straining",
    "Stream",
    "Stuck",
    "StuckEntry",
    "StuckEnvelope",
    "StuckReport",
    "Substitution",
    "SubstitutionEnvelope",
    "SubstitutionReport",
    "SupervisionReport",
    "Support",
    "Switched",
    "Taken",
    "TakesAway",
    "TakesAwayBounded",
    "TakesAwayOpenEnded",
    "Tally",
    "Telemetry",
    "Term",
    "Terms",
    "Tier",
    "TraceConfidence",
    "TraceEnvelope",
    "TraceMoment",
    "TraceOutcome",
    "TraceReport",
    "TraceStage",
    "Transfer",
    "Tree",
    "Triggered",
    "TriggeredFailed",
    "TriggeredNotStarted",
    "TriggeredStarted",
    "Trouble",
    "Undeclared",
    "Undo",
    "UndoEnvelope",
    "UndoLeft",
    "UndoNoted",
    "UndoReversal",
    "Unfilled",
    "Uninstall",
    "UninstallConfidence",
    "UninstallEnvelope",
    "UninstallLeft",
    "UninstallManifest",
    "UninstallRemoval",
    "UninstallRemovalComplete",
    "UninstallRemovalConfirmed",
    "UninstallRemovalPartial",
    "UninstallRemovalSurveyed",
    "Unrated",
    "UnsupportedReport",
    "UpdateApplied",
    "UpdateChange",
    "UpdateEnvelope",
    "UpdateReport",
    "UpdateReversal",
    "UpdateState",
    "UpgradeEnvelope",
    "UpgradeMedia",
    "UpgradeReport",
    "Validation",
    "ValidationDegraded",
    "ValidationRejected",
    "ValidationUnreachable",
    "ValidationValid",
    "ValueOrigin",
    "ValueOriginBundled",
    "ValueOriginOperator",
    "ValueOriginOrphaned",
    "ValueOriginOverridden",
    "ValueOriginPlugin",
    "ValueOriginUnknown",
    "ValueReplaced",
    "VersionEnvelope",
    "VersionReport",
    "Vigil",
    "Vocabulary",
    "Volume",
    "Vpn",
    "WalkthroughEnvelope",
    "WalkthroughReport",
    "WalkthroughState",
    "WalkthroughStep",
    "WatchEnvelope",
    "WhenExceeded",
    "Whose",
    "Wired",
    "Wiring",
    "WiringContest",
    "WiringEnvelope",
    "WiringReport",
    "WiringSettled",
    "WiringSettledChosen",
    "WiringSettledContested",
    "WiringSettledEach",
    "WiringSettledOutright",
    "WiringSettledUnfilled",
    "WizardEnvelope",
    "WizardReport",
    "WizardStep",
    "WordEnvelope",
    "is_key_callable",
    "is_refusal_code",
]
