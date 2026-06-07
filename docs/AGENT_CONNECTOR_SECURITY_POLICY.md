# Agent Connector Security Policy

This policy applies to public-safe reference connectors in ServerDi Topic OS.

## Secret handling

Public repositories must not include:

- real provider tokens or app passwords;
- real `.env` files;
- real email addresses used by the maintainer;
- real phone numbers;
- real calendar names;
- private message bodies;
- Telegram chat or topic identifiers;
- private server paths, logs, backups, cache, or session data.

Only sanitized placeholders are allowed:

```text
work@example.com
personal@example.com
Work Calendar
Personal Calendar
replace-with-app-password
```

## Preview/confirm rule

Any operation that sends data, creates data, edits data, deletes data, or calls a paid/risky provider must be split into two phases:

1. `preview` returns what would happen and a one-time confirmation id;
2. `confirm` executes only the previously previewed action.

Confirm ids must not be reusable.

## Work-calendar rule

Work-calendar writes require explicit owner confirmation because work calendars may be shared with teammates. A generic request such as "add this to the calendar" is not enough.

## Testing rule

CI tests must not call real IMAP, SMTP, CalDAV, Telegram, paid model APIs, or private infrastructure. Use fake backends and fixtures.

## Publication rule

Before publishing:

```bash
python tools/public_safety_scan.py . --strict
git diff --check
```

Maintainers should also grep for known private markers before pushing.
