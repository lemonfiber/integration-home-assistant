# lemonfiber for Home Assistant

A Home Assistant integration for [lemonfiber](https://github.com/lemonfiber/lemonfiber), the
tool that sets up and runs a self-hosted media stack. It shows the stack's health, downloads,
disk space, doctor findings and alerts in Home Assistant, and gives you a few controls: running
the doctor, restarting services, updating them, and pausing downloads.

It reaches the stack only through [sdk-python](https://github.com/lemonfiber/sdk-python), with
an integration key the operator mints on the stack. It never asks for the operator password.

**Status:** installed from this repository as a HACS custom repository; it is not in HACS's
default list.

## Requirements

- Home Assistant 2026.10 or newer, with [HACS](https://hacs.xyz).
- A lemonfiber stack on [v0.17.0](https://github.com/lemonfiber/lemonfiber/releases/tag/v0.17.0)
  or newer, the first release with `lemonfiber key`, whose web API is served over https on
  your network, on a fixed port, reachable from the machine Home Assistant runs on.

## Installing it

1. On the stack's machine, serve the web API on your network, encrypted, on a fixed port, and
   leave it running. The integration can reach the stack only while this runs:

   ```console
   $ lemonfiber ui --lan --tls --port 8443 --set-password
   ```

   `--lan` is refused until a password is set; `--set-password` asks for one at the keyboard.
   Leave it out on later runs.

2. On the stack, in another terminal, mint a key for Home Assistant. Use `--scope read` for
   sensors only, or `--scope act` for the controls as well:

   ```console
   $ lemonfiber key mint home-assistant --scope read --purpose home-assistant
   ```

   The reply shows the stack's address, the key and the certificate pin. The key is shown
   once; if you lose it, mint another.

3. In HACS, add `https://github.com/lemonfiber/integration-home-assistant` as a custom
   repository of the type *Integration*. Install **lemonfiber** and restart Home Assistant.
4. In Home Assistant, go to **Settings → Devices & services → Add integration**, choose
   **lemonfiber**, and paste the three:

| Field | What to paste |
|---|---|
| Address | The https address from the mint reply, with its port |
| Key | The integration key, starting with `lfk_` |
| Certificate pin | The 64 hexadecimal characters naming the stack's certificate |

The three are checked against the stack before anything is added. A failure names the field to
change: an address nothing answers at, a pin the stack's certificate does not match, or a key
the stack does not admit. Nothing is sent to a stack whose certificate does not match the pin.

## What appears

What appears is what the key's scope reaches, as the stack's own capabilities say on every connection.

With a `read` or `act` key, one device for the stack, carrying:

| Entity | What it shows |
|---|---|
| Health | The stack's standing: healthy, stopped, not set up, advisory, degraded, broken or critical, with the worst thing wrong as an attribute |
| Needs attention | On while the stack counts anything wrong |
| Download queue | How many items wait in every queue together |
| Download speed | What every active download comes to |
| Data disk free | The bytes free on the data volume |
| VPN | Whether downloads leave through the tunnel; present only where the stack has a VPN |
| Advisory, warning, error and critical findings | How many of the doctor's findings carry each severity, with what each says happened as an attribute. Advisory findings are advice rather than anything wrong, and their entity is off until enabled |
| Stack update | Every service that is off its pin, by its id, at the version it stands on and the version it would move to, with what each step means as the release notes. Where nothing would move, both versions are the version of lemonfiber the stack runs |
| Update of each service | The version a service stands on and the version this build of lemonfiber pins it at, for every service the dashboard names, with what the step means as the release summary. Off until enabled; the stack update covers them all |
| Alerts | The last alert the stack raised or resolved: the event type is `onset` or `resolved`, and the attributes say what happened, what it means, what to do, its severity, its kind, the checks it speaks for and the alert's identity |

With an `act` key, where the stack says the key may call the action, also:

| Entity | What it does |
|---|---|
| Run the doctor | Runs every check, follows the run to its end, and reads the findings again |
| Restart the stack | Restarts every service the stack runs. Shown under the device's configuration |
| Restart each service | Restarts the one service, leaving the rest of the stack alone, for every service the dashboard names. Shown under the device's configuration, and off until enabled |
| Install, on the stack update and on each service's update | Updates the stack, or the one service, to the versions this build of lemonfiber pins. Pressing install agrees to what the step costs. A step the stack refuses to take offers no install |
| Downloads paused | Pauses every download client when turned on, and resumes them when turned off. The stack does not report whether they are paused, so the switch shows what it last asked for |

A control follows the job it started to its end. A failure is shown in the stack's own words, and every outcome is fired as a `lemonfiber_job` event carrying the entry, the action, the job's name where it started one, the outcome (`finished`, `ended` or `failed`) and, for a failure, the stack's sentence.

A member's key adds the entry and no entity.

Every alert is also fired as a `lemonfiber_alert` event, at its onset and at its resolution, carrying the entry, the alert's identity (the same on an onset and on the resolution that ends it), `moment` (`onset` or `resolved`), `severity`, `kind`, `check`, `affected`, `summary` (what happened), `meaning` (what it means), `remedies` (what to do) and, where the stack gave one, `exit`. Neither the event nor the entity carries the key, the address or the pin.

## What it is for

- Seeing at a glance, beside the rest of the house, whether the stack is healthy and what is wrong when it is not.
- Being told when the stack needs attention, the disk is filling or downloads stop leaving through the VPN, wherever Home Assistant already reaches you.
- Keeping downloads off the line while the household streams, with an `act` key.
- Knowing which services this build of lemonfiber would update, and updating them, with an `act` key.
- Hearing about an alert, and its resolution, with what to do about it.

## Examples

Each example names entities as an entry titled `nas.local` names them; use the ids your entry shows.

Tell the operator when the stack needs attention, and what the worst of it is:

```yaml
automation:
  - alias: "lemonfiber needs attention"
    triggers:
      - trigger: state
        entity_id: binary_sensor.nas_local_needs_attention
        to: "on"
    actions:
      - action: notify.notify
        data:
          message: "lemonfiber: {{ state_attr('sensor.nas_local_health', 'worst') }}"
```

Pause downloads for the evening and resume them at night, with an `act` key:

```yaml
automation:
  - alias: "Downloads off the line in the evening"
    triggers:
      - trigger: time
        at: "19:00:00"
    actions:
      - action: switch.turn_on
        target:
          entity_id: switch.nas_local_downloads_paused
  - alias: "Downloads back at night"
    triggers:
      - trigger: time
        at: "23:30:00"
    actions:
      - action: switch.turn_off
        target:
          entity_id: switch.nas_local_downloads_paused
```

Pass each alert on with what to do about it, and say when it is over:

```yaml
automation:
  - alias: "lemonfiber alert"
    triggers:
      - trigger: event
        event_type: lemonfiber_alert
    actions:
      - action: notify.notify
        data:
          message: >-
            {% if trigger.event.data.moment == 'onset' %}{{ trigger.event.data.summary }}
            {{ trigger.event.data.meaning }} {{ trigger.event.data.remedies | first }}{% else %}Resolved: {{ trigger.event.data.summary }}{% endif %}
```

Say when a control's action failed, in the stack's words:

```yaml
automation:
  - alias: "A lemonfiber control failed"
    triggers:
      - trigger: event
        event_type: lemonfiber_job
        event_data:
          outcome: failed
    actions:
      - action: notify.notify
        data:
          message: "{{ trigger.event.data.action }}: {{ trigger.event.data.sentence }}"
```

## How it stays current

The health, the downloads, the disk, the VPN and the alerts come from the stack's event stream as the stack sends them. When the stream breaks, every one of them shows unavailable until the stream says what it is now; a value from before the break is never shown as current. A figure the stack itself cannot read at the moment shows unknown.

Every entity shows unavailable while the stream has a gap, including the doctor's findings and the services' versions, which are read rather than streamed.

The doctor's findings are read when the entry starts, every hour, and whenever the stream says the stack's health moved. The services' versions are read when the entry starts and every hour.

When the key is refused, Home Assistant asks for a new one; only the key is asked for. When the stack cannot be reached, the entry is set up again with Home Assistant's own retry. The address and pin can be changed from the entry's **Reconfigure** without removing it.

## Known limitations

- Disk free is shown for the data volume, the one the event stream carries.
- There is no entity for active streams.
- The stack does not report whether the download clients are paused, so the downloads switch shows what it last asked for.

## Troubleshooting

A changed certificate, something other than lemonfiber answering at the address, and a stack speaking another version of lemonfiber's interface are also raised under **Settings → Repairs** until the entry next reaches the stack.

| Said | What to do |
|---|---|
| Nothing answered at this address | Check the address and port from Home Assistant's machine, and that `lemonfiber ui --lan --tls` is still running on the stack. If it was started without `--lan`, it is reachable from the stack's own machine only. |
| The stack presented a certificate other than the one this pin names | Copy the pin again from the mint reply. If the stack's certificate changed, give the new pin through **Reconfigure**. |
| The stack does not admit this key | The key was revoked or mistyped. Mint a new one and give it when Home Assistant asks. |
| The stack refuses a key that arrives without the encryption its pin verifies | Use the https address the mint reply gave. |

**Settings → Devices & services → lemonfiber → Download diagnostics** hands over the key's scope, the stack's capabilities and what it last said, with the key, the address and the pin withheld.

## Removing it

Delete the entry under **Settings → Devices & services → lemonfiber**, then remove the integration in HACS and restart Home Assistant. Revoke the key on the stack once nothing uses it.

## Contributing

```sh
uv sync
uv run just ci      # lint, strict types, the suite at 100% line and branch coverage
```

The client sits under `custom_components/lemonfiber/_vendor/` at the sdk-python commit its
`REVISION` names, written by `uv run just vendor <commit>` or by the `sdk-bump` workflow, never
by hand. Mutation testing, `hassfest`, HACS's validation and the client's drift check run in CI.
Every change cites a requirement in the [specification](https://github.com/lemonfiber/spec),
which describes this integration as feature
[F12](https://github.com/lemonfiber/spec/blob/main/10-functional/features/f-extensibility/f12-home-assistant.md);
start with the
[contributing guide](https://github.com/lemonfiber/spec/blob/main/50-governance/contributing.md).

## Security

Report a vulnerability privately, as the
[security policy](https://github.com/lemonfiber/.github/blob/main/SECURITY.md) describes. Do
not open a public issue.

## Licence

[Hippocratic License 3.0](LICENSE): source-available and ethical-source, not OSI-approved. The
[licence rationale](https://github.com/lemonfiber/spec/blob/main/90-appendix/license-rationale.md)
explains what that means for you. Made by NightWorksIO.
