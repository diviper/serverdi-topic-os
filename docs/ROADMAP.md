# Roadmap

This roadmap tracks public-safe work for ServerDi Topic OS. It intentionally excludes private runtime plans, secrets, internal deployment details, personal data, and environment-specific operations.

## Done

- Initial public documentation kit.
- Public safety scanner with strict CI workflow.
- Release validation checklist.
- Public-safe topic map examples for solo maintainers, small teams, and documentation-heavy workspaces.
- Project maintenance pack with changelog, roadmap, OpenAI Codex OSS application notes, and local-only journal ignore support.

## Active Build Track: Agent Tool Connectors

This track turns the playbook into a small public-safe reference implementation. The goal is not to publish private runtime automation. The goal is to show reusable OSS patterns for bounded agent tools, secret isolation, and human confirmation gates.

- Add a public-safe Yandex Agent Tools reference package under `packages/yandex-agent-tools/`.
- Keep all fixtures fake: `work@example.com`, `personal@example.com`, `Work Calendar`, and `Personal Calendar`.
- Demonstrate mail list/search/read plus send/reply preview-confirm flows.
- Demonstrate calendar list plus create preview-confirm flows.
- Require additional explicit confirmation for work-calendar writes.
- Add Docker and compose examples for private self-hosted deployment.
- Add Hermes and OpenClaw integration guides.
- Run package tests and the public-safety scanner in CI.

## Near-Term

- Add more focused prompt templates for release review, stale context cleanup, and incident follow-up.
- Improve scanner guidance for maintainers reviewing warnings and blockers.
- Add more public-safe examples for small open-source maintainers.
- Keep README navigation current as the project grows.

## Mid-Term

- Add checklist variants for documentation-only releases, lightweight tool releases, and template-only releases.
- Expand examples for approval gates and final reports.
- Document how maintainers can adapt the playbook without exposing private operations.
- Add scanner fixtures for common public-safe and unsafe examples.

## Long-Term

- Explore a public-safe document ingestion gateway concept.
- Add more release discipline around tags, changelog entries, and validation evidence.
- Build a mature open-source handbook for self-hosted agent operations.
- Keep the project useful without depending on any private deployment.

## Public-Safe Scope Note

The roadmap covers only public documentation, examples, prompt templates, validation tools, and maintainer process. It does not include private runtime plans, credentials, internal deployment details, private infrastructure, account-specific records, raw operational output, sessions, memory dumps, backups, or personal data.
