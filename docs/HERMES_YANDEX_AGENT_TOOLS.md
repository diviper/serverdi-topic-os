# Hermes Integration: Yandex Agent Tools Reference

This guide shows how Hermes-style agents can call the public-safe Yandex Agent Tools reference package without direct access to mail/calendar secrets.

## Boundary

Hermes should treat the connector as a narrow tool service:

```text
Hermes agent → HTTP/MCP adapter → yandex-agent-tools service → private mail/calendar provider
```

The public repository includes only fake backends and placeholders. A private deployment may replace fake backends with real IMAP/SMTP/CalDAV implementations, but secrets must stay in private `.env` files or deployment secret stores.

## Tool mapping

Suggested Hermes tool names:

```text
yat_accounts_list
yat_contacts_list
yat_contacts_add_preview
yat_contacts_add
yat_mail_list
yat_mail_search
yat_mail_read
yat_mail_send_preview
yat_mail_send_confirm
yat_mail_reply_preview
yat_mail_reply_confirm
yat_calendar_list
yat_calendar_create_preview
yat_calendar_create_confirm
```

## Required behavior

Hermes must never turn a user request into a write action directly. The safe flow is:

1. call `*_preview`;
2. show sender/account/calendar/recipients/body/event time to the owner;
3. wait for explicit owner approval;
4. call `*_confirm` with the returned confirmation id.

Work-calendar writes require an additional explicit owner phrase because such calendars may be shared with teammates.

Contact aliases are a separate Hermes tool boundary, not a backend `POST /contacts` operation. Route natural-language requests such as “add contact”, “добавь контакт”, “добавь техдира”, or “remember this email for calendar invites” to `yat_contacts_add_preview` / `yat_contacts_add`. The public `/contacts` endpoint remains read-only and should expose only alias/display/kind/has_email metadata. Calendar create previews should accept aliases in `attendees` and report `attendee_aliases_resolved` so Telegram can say which alias was used without printing raw emails.

## Public-safe local check

```bash
python -m pytest packages/yandex-agent-tools/tests -q
python tools/public_safety_scan.py . --strict
```

## Private deployment note

Do not publish real Hermes config, Telegram identifiers, account emails, calendar names, tokens, message bodies, or logs. Keep public examples generic and use placeholders only.
