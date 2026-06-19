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

### Telegram natural-language contact creation

A Telegram runtime should expose a first-class contact-alias write action, for example `yandex_contacts action=add` or `contact_alias_add`. Do not infer from `POST /contacts`: the reference `/contacts` endpoint is intentionally read-only list output.

Recommended routing contract:

```text
User says: add contact <name> <email>
User says: add the technical director <name> <email>
User says: remember <name> for calendar invites
User says: добавь контакт <имя> <email>
User says: добавь техдира <имя> <email>
User says: запомни <имя>, чтобы звать в календарь
```

The agent should:

1. normalize a short alias such as `teammate_alpha` or `tech_director`;
2. validate the provided email privately;
3. write only private runtime contact configuration;
4. return alias/display/kind/has_email only;
5. reload the private connector if the deployment requires it;
6. never print the raw email back into Telegram.

This flow is for calendar attendee UX first. After the alias exists, calendar tools should pass the alias in `attendees` instead of asking the user to paste the email again.

## Mail flow

Read-only example:

```text
User: show the latest work mail headers
Agent: calls mail list/search and returns sanitized headers
```

Write example:

```text
User: send teammate_alpha a note from personal mail and copy work
Agent: creates a send preview
Agent: shows sender, normalized To/Cc/Bcc, subject, body, attachment metadata, and confirmation id
User: confirms
Agent: executes send_confirm
```

Mail runtimes should normalize comma/semicolon-separated recipient strings before previewing, so a chat phrase like `reader@example.org, teammate_alpha; work` becomes distinct recipients rather than one malformed address. The implementation should decode MIME-encoded mail headers before returning them to the agent, so subjects and display names are readable in Telegram.

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

Calendar create previews may include `attendees`. Runtimes should resolve configured contact aliases before sending the event to the private backend:

```json
{
  "account_id": "work",
  "summary": "Project sync",
  "start": "2026-01-04T10:00:00Z",
  "end": "2026-01-04T10:30:00Z",
  "attendees": ["teammate_alpha"]
}
```

A safe preview response can include `attendee_aliases_resolved: ["teammate_alpha"]` while redacting raw emails in Telegram-visible output.

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
