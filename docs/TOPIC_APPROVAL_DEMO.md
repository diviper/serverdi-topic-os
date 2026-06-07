# Topic-Based Approval Demo

This public-safe demo shows how topic lanes can control agent write actions without exposing private chat identifiers or real mail/calendar data.

It implements roadmap issue #15 for the Yandex Agent Tools reference package.

## Actors

| Actor | Public-safe placeholder |
| --- | --- |
| Agent | `serverdi-demo-agent` |
| Owner | `owner-placeholder` |
| Approval topic | `topic-demo-approvals` |
| Work account | `work@example.com` |
| Personal account | `personal@example.com` |
| Work calendar | `Work Calendar` |
| Personal calendar | `Personal Calendar` |

No real Telegram group ids, topic ids, user ids, screenshots, private chat transcripts, emails, or calendar data are used.

## Safety rules

1. Preview is not permission to execute.
2. The agent must call a `*_preview` endpoint before any write.
3. The preview must be posted to the approval topic in sanitized form.
4. The owner must reply with an explicit approval phrase.
5. The agent may call `*_confirm` only with the one-time confirmation id from the preview.
6. Reusing a confirmation id must fail.
7. Work-calendar writes require an explicit work-calendar approval phrase.

## Mail send demo

### Step 1: agent creates preview

```json
{
  "tool": "yat_mail_send_preview",
  "account_id": "personal",
  "to": ["reader@example.org"],
  "subject": "Public-safe demo note",
  "body_text": "This is a synthetic demo message."
}
```

### Step 2: connector returns sanitized preview

```json
{
  "requires_confirmation": true,
  "confirmation_id": "demo-confirm-mail-1",
  "preview": {
    "from": "Personal Agent <personal@example.com>",
    "to": ["reader@example.org"],
    "subject": "Public-safe demo note",
    "body_text": "This is a synthetic demo message."
  }
}
```

### Step 3: agent posts to approval topic

```text
Approval requested in topic-demo-approvals

Action: send mail
Account: personal
To: reader@example.org
Subject: Public-safe demo note
Confirmation id: demo-confirm-mail-1

Reply with: confirm demo-confirm-mail-1
```

### Step 4: owner approves

```text
confirm demo-confirm-mail-1
```

### Step 5: agent confirms

```json
{
  "tool": "yat_mail_send_confirm",
  "confirmation_id": "demo-confirm-mail-1"
}
```

### Step 6: agent reports result

```text
Completed: mail send confirmed.
Not changed: calendar.
Safety: no confirmation id was reused.
```

## Work-calendar create demo

Work calendar writes need stronger language because work calendars can be shared.

### Preview request

```json
{
  "tool": "yat_calendar_create_preview",
  "account_id": "work",
  "summary": "Public-safe approval demo",
  "start": "2026-01-06T09:00:00Z",
  "end": "2026-01-06T09:30:00Z",
  "description": "Synthetic event used for approval-flow documentation."
}
```

### Preview response

```json
{
  "requires_confirmation": true,
  "requires_explicit_work_calendar_confirmation": true,
  "confirmation_id": "demo-confirm-calendar-1"
}
```

### Approval topic message

```text
Approval requested in topic-demo-approvals

Action: create calendar event
Account: work
Calendar: Work Calendar
Summary: Public-safe approval demo
Time: 2026-01-06T09:00:00Z to 2026-01-06T09:30:00Z
Confirmation id: demo-confirm-calendar-1

Because this is a work calendar, reply with:
confirm work calendar write demo-confirm-calendar-1
```

### Owner approval

```text
confirm work calendar write demo-confirm-calendar-1
```

### Confirm call

```json
{
  "tool": "yat_calendar_create_confirm",
  "confirmation_id": "demo-confirm-calendar-1",
  "explicit_confirm_text": "confirm work calendar write demo-confirm-calendar-1"
}
```

## Failure demo: repeated confirmation

If the agent repeats the same confirmation id, the connector should reject it:

```json
{
  "confirmation_id": "already-used-confirmation-id",
  "status": "rejected",
  "reason": "confirmation id was already used"
}
```

## Related files

- `packages/yandex-agent-tools`
- `docs/ROADMAP.md`
- `docs/AGENT_CONNECTOR_SECURITY_POLICY.md`
- `docs/YANDEX_AGENT_TOOLS_FAKE_FIXTURES.md`
