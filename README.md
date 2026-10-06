# integration-home-assistant

lemonfiber in Home Assistant: the stack's health, alerts, a short list of controls and a member's own library, through an integration key.

What this repository is and what it must meet is specified in [`spec/30-repos/integration-home-assistant.md`](https://github.com/lemonfiber/spec/blob/main/30-repos/integration-home-assistant.md), and what it does for the people using it in [F12](https://github.com/lemonfiber/spec/blob/main/10-functional/features/f-extensibility/f12-home-assistant.md).

## What it does

The integration follows one lemonfiber stack per entry. It reaches the stack only through [sdk-python](https://github.com/lemonfiber/sdk-python), and only with an integration key the operator minted on the stack. It never asks for the operator password.

Supported: any lemonfiber stack that serves its web API over https, reachable from the machine Home Assistant runs on, in Home Assistant 2026.10 or newer.

## Installing it

1. In HACS, add `https://github.com/lemonfiber/integration-home-assistant` as a custom repository of the type *Integration*.
2. Install **lemonfiber** from HACS and restart Home Assistant.
3. On the stack, mint an integration key. The reply shows three things: the stack's address, the key and the certificate pin.
4. In Home Assistant, go to **Settings → Devices & services → Add integration**, choose **lemonfiber**, and paste the three.

| Field | What to paste |
|---|---|
| Address | The https address from the mint reply, with its port |
| Key | The integration key, starting with `lfk_` |
| Certificate pin | The 64 hexadecimal characters naming the stack's certificate |

The three are checked against the stack before anything is added. A failure names the field to change: an address nothing answers at, a pin the stack's certificate does not match, or a key the stack does not admit. Nothing is sent to a stack whose certificate does not match the pin.

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

- A member's key yields no entity.
- Disk free is shown for the data volume, the one the event stream carries.
- There is no restart button and no alert events, an update entity shows an update without installing it, and there is no entity for active streams.

## Troubleshooting

| Said | What to do |
|---|---|
| Nothing answered at this address | Check the address and port from Home Assistant's machine. If lemonfiber's web surface is bound to loopback only, bind it beyond loopback on the stack and use the address and pin it shows. |
| The stack presented a certificate other than the one this pin names | Copy the pin again from the mint reply. If the stack's certificate changed, give the new pin through **Reconfigure**. |
| The stack does not admit this key | The key was revoked or mistyped. Mint a new one and give it when Home Assistant asks. |
| The stack refuses a key that arrives without the encryption its pin verifies | Use the https address the mint reply gave. |

**Settings → Devices & services → lemonfiber → Download diagnostics** hands over the key's scope, the stack's capabilities and what it last said, with the key, the address and the pin withheld.

## Removing it

Delete the entry under **Settings → Devices & services → lemonfiber**, then remove the integration in HACS and restart Home Assistant. Revoke the key on the stack once nothing uses it.

## Working on it

```sh
uv sync
uv run just ci      # lint, strict types, the suite at 100% line and branch coverage
```

The client sits under `custom_components/lemonfiber/_vendor/` at the sdk-python commit its `REVISION` names, written by `uv run just vendor <commit>` and never by hand. Mutation testing, `hassfest`, HACS's validation, the client's drift check and the organisation's shared workflows run in CI.

Hippocratic License 3.0. See [LICENSE](LICENSE).
