# Maintenance workflow notes

This document describes how ServerDi Topic OS keeps repository maintenance reviewable. It is public-safe: examples use fake accounts, fake connector fixtures, and sanitized approval workflows only.

## Project summary

ServerDi Topic OS is an Apache-2.0 playbook and reference toolkit for safer self-hosted agent operations.

The project focuses on practical boundaries for tools that inspect repositories, prepare patches, call connector services, and request human approval before write actions.

## Current public artifacts

- Public repository: `diviper/serverdi-topic-os`
- Reference package: `packages/yandex-agent-tools`
- Safety policy: `docs/AGENT_CONNECTOR_SECURITY_POLICY.md`
- Hermes guide: `docs/HERMES_YANDEX_AGENT_TOOLS.md`
- OpenClaw guide: `docs/OPENCLAW_YANDEX_AGENT_TOOLS.md`
- Fake fixture guide: `docs/YANDEX_AGENT_TOOLS_FAKE_FIXTURES.md`
- Topic approval demo: `docs/TOPIC_APPROVAL_DEMO.md`
- Roadmap: `docs/ROADMAP.md`

## Why this maintenance model works

The repository is code-and-test heavy in small pieces:

1. Add or refine connector fixtures.
2. Expand tests for preview/confirm safety behavior.
3. Improve docs for bounded workflows.
4. Keep public-safety scanner rules accurate.
5. Review pull requests for accidental private-data exposure.
6. Keep examples small enough for maintainers to audit.

## Safety model

The repository demonstrates these rules:

- read operations may return headers, snippets, sanitized text, and attachment metadata;
- write operations must use preview/confirm;
- preview is not permission to execute;
- confirmation ids are one-time use;
- work-calendar writes require explicit owner confirmation;
- tests must not call real IMAP, SMTP, CalDAV, Telegram, paid model APIs, or private infrastructure;
- examples must not include real emails, phone numbers, Telegram ids, server paths, tokens, logs, or message bodies.

## Recent implementation highlights

The public reference package includes:

- a FastAPI HTTP adapter;
- fake mail/calendar backends;
- fake mail and CalDAV-style fixtures;
- mail send/reply preview-confirm examples;
- outgoing mail attachment preview-confirm examples with metadata-only previews;
- calendar create preview-confirm examples;
- Docker and Docker Compose examples;
- Hermes and OpenClaw integration guides;
- a topic-based approval demo;
- CI tests;
- strict public-safety scan guidance.

## Good next maintenance tasks

These tasks are public-safe and suitable for incremental PRs:

1. Add more fake provider error fixtures.
2. Add structured JSON schemas for connector responses.
3. Add CLI examples for local fixture inspection.
4. Add tests that assert list/search never expose full bodies.
5. Add markdown linting for docs examples.
6. Improve `tools/public_safety_scan.py` docs and fixtures.
7. Add a small static architecture diagram for the connector boundary.

## What should stay private

The public repository must not include:

- real provider credentials;
- real account addresses;
- real calendar names;
- private chat identifiers;
- private server paths;
- production logs;
- real mail bodies;
- deployment secret files.

Private deployments may replace fake backends with real connectors, but those changes must keep secrets outside this repository.

## Verification commands

Before submitting public changes:

```bash
PYTHONPATH=packages/yandex-agent-tools/src python -m pytest packages/yandex-agent-tools/tests tests -q
python tools/public_safety_scan.py . --strict
git diff --check
```

Maintainers should also grep for known private markers before publishing.
