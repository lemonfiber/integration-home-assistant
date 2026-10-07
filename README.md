# lemonfiber for Home Assistant

A Home Assistant integration for [lemonfiber](https://github.com/lemonfiber/lemonfiber), the
tool that sets up and runs a self-hosted media stack. It shows the stack's health, downloads,
disk space and doctor findings in Home Assistant, and gives you a few controls such as pausing
downloads.

It reaches the stack only through [sdk-python](https://github.com/lemonfiber/sdk-python), with
an integration key the operator mints on the stack. It never asks for the operator password.

**Status:** installed from this repository as a HACS custom repository; it is not in HACS's
default list. It needs `lemonfiber key`, which no lemonfiber release has yet: build lemonfiber
from its `main` branch.

## Requirements

- Home Assistant 2026.10 or newer, with [HACS](https://hacs.xyz).
- A lemonfiber stack whose web API is served over https on your network, on a fixed port,
  reachable from the machine Home Assistant runs on.

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
| Advisory, warning, error and critical findings | How many of the doctor's findings carry each severity, with what each says happened as an attribute |
| Update of each service | The version a service stands on and the version this build of lemonfiber pins it at, for every service the dashboard names |

With an `act` key, where the stack says the key may call the action, also:

| Entity | What it does |
|---|---|
| Run the doctor | Runs every check, follows the run to its end, and reads the findings again |
| Downloads paused | Pauses every download client when turned on, and resumes them when turned off. The stack does not report whether they are paused, so the switch shows what it last asked for |

A control follows the job it started to its end. A failure is shown in the stack's own words, and every outcome is fired as a `lemonfiber_job` event carrying the entry, the action, the job's name where it started one, the outcome (`finished`, `ended` or `failed`) and, for a failure, the stack's sentence.

A member's key adds the entry and no entity.

## How it stays current

The health, the downloads, the disk and the VPN come from the stack's event stream as the stack sends them. When the stream breaks, every one of them shows unavailable until the stream says what it is now; a value from before the break is never shown as current. A figure the stack itself cannot read at the moment shows unknown.

The doctor's findings are read when the entry starts, every hour, and whenever the stream says the stack's health moved. The services' versions are read when the entry starts and every hour.

When the key is refused, Home Assistant asks for a new one; only the key is asked for. When the stack cannot be reached, the entry is set up again with Home Assistant's own retry. The address and pin can be changed from the entry's **Reconfigure** without removing it.

## Known limitations

- Disk free is shown for the data volume, the one the event stream carries.
- There is no restart button and no alert events, an update entity shows an update without installing it, and there is no entity for active streams.

## Troubleshooting

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
`REVISION` names, written by `uv run just vendor <commit>` and never by hand. Mutation testing,
`hassfest`, HACS's validation and the client's drift check run in CI. Every change cites a
requirement in the [specification](https://github.com/lemonfiber/spec), which describes this
integration as feature
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
