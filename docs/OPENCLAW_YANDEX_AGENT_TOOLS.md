# OpenClaw Integration: Yandex Agent Tools Reference

This guide describes how OpenClaw-style server agents can use the Yandex Agent Tools reference package as a bounded connector.

## Intent

OpenClaw should not hold provider credentials directly in arbitrary task sessions. It should call a narrow connector that owns the provider-specific implementation and safety policy.

```text
OpenClaw task → connector API → preview/confirm gate → private provider backend
```

## Suggested endpoints

A private deployment may expose these endpoints on an internal Docker network:

```text
GET  /health
GET  /accounts
POST /tools/mail/list
POST /tools/mail/search
POST /tools/mail/read
POST /tools/mail/send/preview
POST /tools/mail/send/confirm
POST /tools/mail/reply/preview
POST /tools/mail/reply/confirm
POST /tools/calendar/list
POST /tools/calendar/create/preview
POST /tools/calendar/create/confirm
```

## Docker boundary

Bind the service to localhost or an internal agent network. Do not expose it directly to the public internet.

```yaml
ports:
  - "8080:8080"
```

## Confirmation policy

- Read operations may return summaries or requested content.
- Send/reply/create operations must return preview first.
- Mail attachment previews must show metadata only and keep raw bytes out of task logs.
- Confirm ids are one-time use.
- Work-calendar writes require explicit owner confirmation.
- Agents must report exactly what was executed and what was not executed.

## Public-safe contribution rule

Pull requests must use fake addresses and fake fixtures only. Never include private account data, customer data, Telegram IDs, runtime logs, backups, sessions, or cache artifacts.
