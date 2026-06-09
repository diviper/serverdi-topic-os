# ServerDi Topic OS

ServerDi Topic OS is a safety-first open-source playbook for building and maintaining self-hosted AI agent systems with OpenClaw, Hermes, Codex, Docker, and Telegram forum topics. It turns messy agent workflows into bounded, auditable micro-passes so maintainers can use AI agents without handing them uncontrolled access to production, secrets, paid APIs, or private data.

## Why This Exists

Self-hosted AI agents are useful in real engineering work, but they can become risky when every task has the same permissions, context, and operational scope. A small documentation fix should not have the same authority as a production restart. A model investigation should not inherit stale Telegram context. A patch pass should not silently become a cleanup pass.

This repository documents a practical operating model for making agent work smaller, safer, and easier to review.

## Who It Is For

- Engineers running self-hosted AI tools around real infrastructure.
- Open-source maintainers who want agent help without uncontrolled repository changes.
- Small teams using Telegram topics, Codex, OpenClaw, Hermes, and Docker as an operational layer.
- Builders who need repeatable prompts, review gates, and public-safe documentation patterns.

## What Problem It Solves

AI agent systems often fail at boundaries:

- unclear task scope;
- stale or mixed context;
- accidental access to production runtime state;
- paid API calls without owner approval;
- local files mistaken for delivered results;
- patches created without validation;
- public docs contaminated with private data.

ServerDi Topic OS gives operators a shared vocabulary and workflow for handling these failure modes before they become incidents.

## Core Concepts

- **One bounded outcome:** each task has one clear deliverable.
- **Micro-pass:** a narrow agent pass such as scout, patch, validation, audit, or final report.
- **Topic OS:** Telegram forum topics act as operational lanes for sessions, decisions, and reports.
- **Boundary contour:** OpenClaw, Hermes, Codex, Docker, and Telegram have separate responsibilities.
- **CostGate:** risky or paid tool use requires explicit owner approval.
- **Validation-first delivery:** success is proven by checks, events, or delivered artifacts, not by claims.
- **Public-safe documentation:** examples use placeholders and never include private deployment data.

## Safety Principles

- Keep scout passes read-only.
- Never mix unrelated runtime changes.
- Do not expose secrets, tokens, private keys, cookies, or env values.
- Do not publish real Telegram IDs, thread IDs, personal data, billing data, or private infrastructure details.
- Do not restart production services without explicit approval.
- Prefer smallest safe patch over broad cleanup.
- Validate before commit.
- Report exactly what changed and what was not touched.

## Quick Start

1. Pick one bounded outcome.
2. Choose the pass type: scout, patch, validation, audit, or documentation-only.
3. Copy a template from `examples/`.
4. Replace placeholders such as `<TELEGRAM_GROUP_ID>`, `<TOPIC_ID>`, and `<MODEL_PROVIDER/MODEL_NAME>`.
5. Run the pass with the minimum required permissions.
6. Validate the result.
7. Write a final report before moving to the next task.

## Repository Structure

```text
.
|-- README.md
|-- LICENSE
|-- CHANGELOG.md
|-- SECURITY.md
|-- CONTRIBUTING.md
|-- CODE_OF_CONDUCT.md
|-- .github/workflows/public-safety-scan.yml
|-- docs/
|   |-- SERVERDI_AGENT_OPERATING_MANUAL.md
|   |-- CODEX_MICRO_PASS_TEMPLATES.md
|   |-- OPENCLAW_HERMES_BOUNDARIES.md
|   |-- TELEGRAM_TOPIC_OS.md
|   |-- COSTGATE_APPROVAL_POLICY.md
|   |-- DOCUMENT_INGESTION_ROADMAP.md
|   |-- SELF_HOSTED_AGENT_OS.md
|   |-- RELEASE_VALIDATION_CHECKLIST.md
|   |-- ROADMAP.md
|   |-- OPENAI_CODEX_OSS_APPLICATION.md
|   |-- AI_ASSISTED_MAINTENANCE.md
|   |-- HERMES_TELEGRAM_OPERATOR_GUIDE.md
|   |-- YANDEX_AGENT_TOOLS_FAKE_FIXTURES.md
|   `-- TOPIC_APPROVAL_DEMO.md
|-- tools/
|   `-- public_safety_scan.py
|-- tests/
|   `-- test_public_safety_scan.py
`-- examples/
    |-- topic-map.example.md
    |-- topic-map.solo-maintainer.example.md
    |-- topic-map.small-team.example.md
    |-- topic-map.documentation-workspace.example.md
    |-- model-priority-map.example.md
    |-- read-only-scout.prompt.md
    |-- patch-pass.prompt.md
    |-- final-report-template.md
    `-- document-ingestion-pass.prompt.md
```

## Reference Implementation: Yandex Agent Tools

ServerDi Topic OS now includes a public-safe reference implementation for agent tool connectors:

```text
packages/yandex-agent-tools/
```

The package demonstrates how self-hosted agents can interact with mail and calendar systems without giving every agent direct secret access or unrestricted write authority. It includes:

- a sanitized `work` / `personal` account registry using placeholder addresses only;
- fake IMAP/SMTP/CalDAV-like backends for tests;
- mail list/search/read interfaces;
- contact aliases with alias-only public listing;
- MIME-decoded mail headers for readable agent summaries;
- mail send and reply preview/confirm flows;
- calendar list and create preview/confirm flows with contact-alias attendee resolution;
- calendar list range filtering;
- explicit protection for work-calendar writes;
- Docker and compose examples for private deployments;
- Hermes and OpenClaw integration guides;
- richer fake connector fixtures for mail, attachment metadata, search snippets, CalDAV-like events, and repeated-confirmation failures;
- a topic-based approval demo for public-safe write gating.

The implementation is intentionally public-safe. It contains no real credentials, phone numbers, private calendar names, Telegram IDs, private message bodies, or deployment logs. See [Yandex Agent Tools README](packages/yandex-agent-tools/README.md), [fake fixture guide](docs/YANDEX_AGENT_TOOLS_FAKE_FIXTURES.md), [topic approval demo](docs/TOPIC_APPROVAL_DEMO.md), [Hermes integration](docs/HERMES_YANDEX_AGENT_TOOLS.md), [Hermes/Telegram operator guide](docs/HERMES_TELEGRAM_OPERATOR_GUIDE.md), [OpenClaw integration](docs/OPENCLAW_YANDEX_AGENT_TOOLS.md), [AI-assisted maintenance notes](docs/AI_ASSISTED_MAINTENANCE.md), and [connector security policy](docs/AGENT_CONNECTOR_SECURITY_POLICY.md).

## Public Safety Scan

This repository includes a dependency-free Python scanner for catching public-disclosure risk markers before commit or release. It is meant to catch likely real values, private paths, and unsafe literals while allowing maintainers to review documentation-only safety warnings.

Run it from the repository root:

```bash
python tools/public_safety_scan.py .
```

Use JSON output for automation:

```bash
python tools/public_safety_scan.py . --json
```

Use strict mode in CI when warnings should fail the check:

```bash
python tools/public_safety_scan.py . --strict
```

Exit codes:

- `0`: no blockers were found.
- `1`: blockers were found, or warnings were found in `--strict` mode.

The scanner is a guardrail, not a replacement for manual review. Maintainers should still inspect changes before publishing public documentation.

## Project Maintenance

Use these public maintenance files to track project direction and release readiness:

- [Changelog](CHANGELOG.md)
- [Roadmap](docs/ROADMAP.md)
- [OpenAI Codex for Open Source application notes](docs/OPENAI_CODEX_OSS_APPLICATION.md)

## Release Validation

Before publishing docs, examples, prompts, templates, or lightweight tools, use the [release validation checklist](docs/RELEASE_VALIDATION_CHECKLIST.md). It covers scope, public safety, examples, prompt templates, scanner output, GitHub Actions, release notes, version or tag checks, manual review, and the final go/no-go decision.

## Topic Map Examples

Use the public-safe topic map examples when structuring agent operations for different maintainer shapes:

- [Solo maintainer](examples/topic-map.solo-maintainer.example.md)
- [Small team](examples/topic-map.small-team.example.md)
- [Documentation-heavy workspace](examples/topic-map.documentation-workspace.example.md)

## Example Workflows

### Read-Only Scout

Use a scout pass to inspect a repository, topic, or architecture question without changing files or calling paid tools. The output is a short report with findings, risks, and a recommended next bounded task.

### Patch Pass

Use a patch pass when the target is clear. The agent edits only the required files, validates the result, and reports the exact files changed.

### Validation Pass

Use a validation pass after a patch, release, ingestion run, or delivery event. Validation checks should be concrete: tests, file diffs, event receipts, delivered messages, or rendered artifacts.

### Documentation-Only Pass

Use this pass when the desired outcome is public documentation. The agent must avoid private paths, logs, session data, and real identifiers.

## How This Helps OSS Maintainers

Maintainers can accept useful agent contributions while keeping changes reviewable:

- narrow prompts reduce unrelated edits;
- validation reports make review faster;
- boundary rules prevent agents from wandering into runtime systems;
- public-safe examples lower the risk of accidental disclosure;
- final reports document what was done and what remains.

## How This Helps Self-Hosted AI Operators

Operators get a practical control plane for agent work:

- Telegram topics become operational lanes;
- model choice is documented per task type;
- approvals are separated from execution;
- OpenClaw and Hermes responsibilities stay distinct;
- risky operations require a human decision;
- stale context is visible instead of implicit.

## Roadmap

- Add more micro-pass templates for incident review, release notes, and dependency audits.
- Add public-safe checklists for model fallback and tool approval.
- Expand document ingestion patterns with classification and redaction gates.
- Add example topic maps for small teams and solo maintainers.
- Add validation recipes for common documentation and repository tasks.

## Author Note

Created by a smart home automation engineer building a self-hosted AI operating layer for real-world engineering, maintenance, documentation, and personal workflows.

## License

Apache-2.0. See [LICENSE](LICENSE).
