# Maintainer support notes

This page keeps public-safe language for describing ServerDi Topic OS to reviewers, maintainers, and potential sponsors. It is intentionally generic: no private runtime details, no private logs, no account data, and no tool-use transcript.

## Project summary

ServerDi Topic OS is an Apache-2.0 playbook and reference toolkit for safer self-hosted agent operations. It documents bounded passes, public-safe prompt templates, release validation, topic maps, a disclosure scanner, and a small reference implementation for mail/calendar connectors.

## Why the repository matters

Agent tooling is useful in maintenance and documentation work, but it needs clear boundaries. Without them, a small documentation task can drift into unsafe automation, unclear approvals, or accidental data exposure. This repository gives maintainers practical patterns for keeping work narrow, auditable, and reviewable.

## Public value

The project helps open-source maintainers and small teams:

- define one bounded outcome per pass;
- separate scout, patch, audit, validation, and release work;
- use topic maps without publishing real chat identifiers;
- validate public docs before release;
- keep private runtime details out of public repositories;
- study a concrete connector package with fake backends, tests, and explicit write confirmation gates.

## What support would improve

Maintainer support would go toward public repository work only:

- clearer documentation and examples;
- scanner rule refinement;
- prompt-template review;
- fake connector fixtures;
- validation recipes for release and PR review;
- public-safe reference connector work.

Support must not be used for private runtime access, private data processing, personal mail/calendar content, production logs, or secrets.

## Safety and privacy stance

ServerDi Topic OS is documentation-first and public-safe. Examples use placeholders such as `<TELEGRAM_GROUP_ID>`, `<TOPIC_ID>`, `<OPENCLAW_WORKSPACE>`, `<HERMES_WORKSPACE>`, `<YOUR_AGENT_STACK_PATH>`, and `<MODEL_PROVIDER/MODEL_NAME>`.

The repository excludes real identifiers, credentials, env values, private infrastructure, raw operational output, sessions, memory dumps, backups, and personal data.

## Maintainer context

The project comes from practical self-hosted operations, documentation workflows, maintenance tasks, and open-source release discipline. The public version keeps the reusable patterns and removes the private runtime details.
