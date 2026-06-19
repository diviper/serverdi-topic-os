# Yandex Agent Tools reference package

Public-safe reference implementation for connecting self-hosted agents to mail and calendar systems through explicit safety boundaries.

This package intentionally uses fake in-memory backends in tests. It does not include real credentials, real email addresses, real message bodies, real calendar names, Telegram IDs, or private deployment details.

## Why it exists

Self-hosted agents need productive tools, but mail and calendar writes are risky. This reference package demonstrates a safer pattern:

- account registry with `work` and `personal` accounts;
- private contact aliases that expose only alias/display metadata in lists;
- sanitized placeholder configuration;
- read/list/search interfaces separated from write flows;
- decoded MIME mail headers for Telegram-readable summaries;
- calendar list range filters;
- preview/confirm before sending mail or creating events;
- outgoing mail attachment previews with metadata-only display and one-time confirmation payloads;
- extra explicit confirmation for work-calendar writes;
- fake backends for tests so CI never touches real networks.

## Package layout

```text
packages/yandex-agent-tools/
├── Dockerfile
├── docker-compose.example.yml
├── pyproject.toml
├── src/yandex_agent_tools/
└── tests/
```

## Quick local test

```bash
python -m pytest packages/yandex-agent-tools/tests -q
```

## Safe configuration example

Use the placeholder configuration example as a template only in private deployments. Never commit runtime configuration files.

The public configuration example uses only placeholders:

```text
work@example.com
personal@example.com
teammate.alpha@example.com
Work Calendar
Personal Calendar
```

Contact aliases are optional. List responses expose alias metadata only and do not return raw contact emails. Private Telegram/Hermes deployments should expose contact creation as a separate tool/action (for example `yandex_contacts action=add`) instead of trying to write to the read-only `/contacts` endpoint. Calendar create previews can use those aliases in `attendees` so users can say “invite teammate_alpha” without pasting an email into chat.


## Mail attachment previews

Outgoing mail previews may address multiple recipient fields. `to`, `cc`, and `bcc` accept either lists or comma/semicolon-separated strings; configured account/contact aliases are resolved before the preview is stored:

```json
{
  "to": ["reader@example.org"],
  "cc": "copy@example.org; work",
  "bcc": ["teammate_alpha"]
}
```

Outgoing mail previews may also include attachment payload objects:

```json
{
  "filename": "report.pdf",
  "content_type": "application/pdf",
  "content_base64": "<base64 bytes>"
}
```

The preview response exposes recipient fields and attachment metadata only:

```json
{
  "to": ["reader@example.org"],
  "cc": ["copy@example.org", "work@example.com"],
  "bcc": ["teammate.alpha@example.com"],
  "attachments": [{"filename": "report.pdf", "content_type": "application/pdf", "size": 12345}]
}
```

The public API must not return raw bytes or base64 in a preview. The connector keeps the decoded bytes inside the one-time in-memory confirmation payload so `send_confirm` sends exactly the draft the owner previewed. Tests use tiny fake byte strings and fake in-memory backends only; CI never contacts real SMTP/IMAP services.

## Tool flow

1. Agent asks for a read operation: list/search/read mail or list calendar events.
2. Service returns safe summaries or requested content.
3. Agent asks for a write operation: send/reply/create event.
4. Service returns a preview and a one-time confirmation id; attachment previews show metadata only.
5. Agent shows the preview to the owner.
6. Owner confirms.
7. Service executes the write action.

Work-calendar writes require an additional explicit owner confirmation phrase because work calendars may be visible to teammates.
