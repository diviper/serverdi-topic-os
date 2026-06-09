# Hermes/Telegram Operator Guide for Yandex Agent Tools

This public-safe guide explains how a self-hosted Hermes-style Telegram bot can expose Yandex mail/calendar tools while keeping reads, previews, confirmations, and private contact aliases separated.

All examples use placeholders. Do not publish real app passwords, OAuth tokens, runtime `.env` values, private email addresses, calendar names, Telegram IDs, message bodies, or deployment paths.

## Safe mental model

```text
Telegram user
  -> Hermes bot
  -> Yandex Agent Tools HTTP adapter
  -> private mail/calendar provider
```

The public reference package uses fake in-memory backends. A private deployment can replace those backends, but should keep the same safety boundaries.

## Recommended tool boundaries

| Operation | Default policy |
| --- | --- |
| Health/status | Read-only |
| Account discovery | Read-only, placeholder/sanitized metadata only |
| Contact discovery | Read-only alias/display/kind metadata only; no raw emails |
| Mail list/search | Read-only headers/snippets |
| Mail read | Explicit user request; redact by default in agent UIs |
| Mail send/reply | Preview first, then confirm |
| Calendar list | Read-only and range-filtered |
| Personal calendar writes | Preview first, then confirm |
| Work calendar writes | Preview first plus explicit owner confirmation |

## Contact aliases

Contact aliases let an operator say `teammate_alpha` instead of pasting a private email into a chat. The raw email stays in private runtime configuration.

Example private configuration shape:

```env
YAT_CONTACT_ALIASES=teammate_alpha
YAT_CONTACT_TEAMMATE_ALPHA_EMAIL=teammate.alpha@example.com
YAT_CONTACT_TEAMMATE_ALPHA_DISPLAY_NAME=Teammate Alpha
YAT_CONTACT_TEAMMATE_ALPHA_KIND=colleague
```

Public list output should look like this:

```json
[
  {
    "alias": "teammate_alpha",
    "display_name": "Teammate Alpha",
    "kind": "colleague",
    "has_email": true
  }
]
```

It should not include `teammate.alpha@example.com`.

## Mail flow

Read-only example:

```text
User: show the latest work mail headers
Agent: calls mail list/search and returns sanitized headers
```

Write example:

```text
User: send teammate_alpha a note from personal mail
Agent: creates a send preview
Agent: shows sender, recipient alias, subject, body, and confirmation id
User: confirms
Agent: executes send_confirm
```

The implementation should decode MIME-encoded mail headers before returning them to the agent, so subjects and display names are readable in Telegram.

## Calendar flow

Calendar listing should accept a requested time range and pass it through to the backend. This prevents broad accidental calendar disclosure.

```json
{
  "account_id": "personal",
  "start": "2026-01-03T00:00:00Z",
  "end": "2026-01-03T23:59:59Z"
}
```

Work-calendar writes are higher risk because events may be visible to teammates. Keep them behind an explicit owner confirmation phrase in private deployments.

## Public-safety checklist

Before publishing docs, examples, or PRs around this connector:

- use only `example.com` / `example.org` addresses;
- use placeholder calendar names such as `Work Calendar` and `Personal Calendar`;
- do not include real Telegram IDs, thread IDs, private paths, tokens, or app passwords;
- keep contact list responses alias-only;
- run the repository public-safety scan and tests.

```bash
python tools/public_safety_scan.py .
PYTHONPATH=packages/yandex-agent-tools/src python -m pytest packages/yandex-agent-tools/tests tests -q
```
