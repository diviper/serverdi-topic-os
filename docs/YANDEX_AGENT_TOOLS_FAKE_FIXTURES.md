# Fake Connector Fixtures

This document describes the richer fake fixtures used by the public-safe Yandex Agent Tools reference package.

The goal is to let contributors test agent behavior without real IMAP, SMTP, CalDAV, mailboxes, calendars, tokens, logs, or private message content.

## Fixture principles

- Use obvious placeholders such as `work@example.com` and `personal@example.com`.
- Keep message bodies short, synthetic, and non-personal.
- Return full bodies only from explicit read fixtures.
- Return snippets or headers from list/search fixtures.
- Attachments are metadata only: filename, content type, size.
- CalDAV examples use synthetic `.ics` text and fake hrefs.
- Failed confirmation fixtures document one-time confirmation behavior.

## Mail fixtures

The fixture module exposes:

```python
from yandex_agent_tools.fixtures import (
    fake_multipart_mail,
    fake_mail_with_attachment_metadata,
    fake_search_result_fixture,
)
```

Use `fake_multipart_mail()` when testing mail parsing behavior:

```python
message = fake_multipart_mail()
```

It includes:

- a plain text part;
- an HTML-present marker;
- attachment metadata;
- no binary attachment bytes.

Use `fake_search_result_fixture()` to test search behavior. It intentionally contains a `snippet`, not a full body.

## Calendar fixtures

Use:

```python
from yandex_agent_tools.fixtures import fake_caldav_event_fixture
```

The returned event includes public-safe CalDAV-like fields:

- `uid`;
- `href`;
- `etag`;
- `ics`;
- `calendar_name`.

The `.ics` text is synthetic and contains no real calendar data.

## Confirmation fixtures

Use:

```python
from yandex_agent_tools.fixtures import fake_failed_confirmation_fixture
```

This fixture documents the expected shape of a rejected repeated confirmation:

```json
{
  "confirmation_id": "already-used-confirmation-id",
  "status": "rejected",
  "reason": "confirmation id was already used"
}
```

## Test command

```bash
PYTHONPATH=packages/yandex-agent-tools/src python -m pytest packages/yandex-agent-tools/tests -q
```

## Safety check

Before publishing fixture changes:

```bash
python tools/public_safety_scan.py . --strict
git diff --check
```
