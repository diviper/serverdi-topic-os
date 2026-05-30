# Self-Hosted Agent OS

A self-hosted AI agent OS is an operating layer for engineering, maintenance, documentation, and personal workflows. It coordinates tools, context, approvals, and validation without giving agents unlimited authority.

This document describes the architecture at a public level only.

## Architecture-Level Components

- **Docker:** hosts isolated services and supporting infrastructure.
- **OpenClaw:** coordinates agent interactions and workspace tasks.
- **Hermes:** supports automation or orchestration workflows.
- **Codex:** edits and validates repository files.
- **Telegram topics:** provide human-visible operational lanes.

These components should be documented as boundaries, not as private deployment instructions.

## Operating Pattern

1. A human defines one bounded outcome.
2. A Telegram topic records the lane and current pass.
3. Codex or another agent performs a scout, patch, audit, or validation pass.
4. Risky tools require approval.
5. Results are validated.
6. A final report records what changed and what was not touched.

## Why This Matters

Personal and small-team AI systems are becoming operationally powerful. Without boundaries, they can create fragile automation, hidden costs, and unclear accountability.

Safer self-hosted agent systems can help society by:

- making personal AI operations more maintainable;
- keeping humans in the approval path for risky actions;
- reducing blind automation;
- improving documentation around real engineering work;
- helping small maintainers use agents without exposing private data;
- turning tacit operational knowledge into auditable public practice.

## Public Documentation Rules

Public architecture docs may explain:

- roles of Docker, OpenClaw, Hermes, Codex, and Telegram topics;
- approval and validation patterns;
- placeholder-based examples;
- safety boundaries.

Public docs must not include private deployment details, real identifiers, secrets, logs, sessions, memory dumps, backups, runtime state, or private paths.
