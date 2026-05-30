# Topic Map Example: Small Team

This public-safe example shows how a small team can coordinate agent work while keeping approvals, engineering changes, documentation, releases, and incidents separate.

Telegram group: `<TELEGRAM_GROUP_ID>`
OpenClaw workspace: `<OPENCLAW_WORKSPACE>`
Hermes workspace: `<HERMES_WORKSPACE>`
Default model: `<MODEL_PROVIDER/MODEL_NAME>`

## Control Topic

Topic name: Control
Topic ID: `<TOPIC_ID>`

Purpose: team-level operating decisions and scope control.

Allowed work:

- approve one bounded outcome;
- assign a reviewer;
- confirm whether a pass is scout, patch, audit, or validation.

Forbidden work:

- storing credentials or private identifiers;
- merging unrelated decisions into one approval;
- changing runtime behavior from a coordination message.

Memory/context note: decisions should be summarized in the relevant pull request or release note.

Validation note: each control decision should name the validation evidence required before merge.

## Engineering Topic

Topic name: Engineering
Topic ID: `<TOPIC_ID>`

Purpose: repository changes, lightweight tools, and engineering review.

Allowed work:

- discuss scoped code or documentation patches;
- review test output;
- plan follow-up issues.

Forbidden work:

- touching runtime configuration;
- handling private deployment details;
- expanding into broad cleanup without control approval.

Memory/context note: engineering topic history is helpful context, but the repository is the source of truth.

Validation note: report branch, changed files, tests, scanner status, commit hash, and pull request URL.

## Documentation Topic

Topic name: Documentation
Topic ID: `<TOPIC_ID>`

Purpose: public docs, examples, prompts, and templates.

Allowed work:

- draft public-safe docs;
- verify placeholder-only examples;
- review prompt boundaries.

Forbidden work:

- copying private workspace text;
- including real IDs;
- publishing unvalidated instructions.

Memory/context note: documentation decisions should be captured in the docs themselves or in release notes.

Validation note: run the public safety scanner and confirm that warnings, if any, are reviewed before release.

## Release Topic

Topic name: Release
Topic ID: `<TOPIC_ID>`

Purpose: release readiness, tag decisions, and final publication notes.

Allowed work:

- apply the release validation checklist;
- confirm workflow status;
- record final go/no-go decision.

Forbidden work:

- tagging before validation;
- releasing from an unreviewed commit;
- claiming delivery without confirmed evidence.

Memory/context note: release topic context should reference immutable commits, not loose summaries.

Validation note: record commit, scanner result, tests, workflow result, reviewer, and final decision.

## Incidents Topic

Topic name: Incidents
Topic ID: `<TOPIC_ID>`

Purpose: public-safe incident triage and follow-up planning.

Allowed work:

- document sanitized impact;
- create follow-up tasks;
- review boundary failures.

Forbidden work:

- copying raw operational output;
- exposing private environment details;
- running recovery actions from the topic map.

Memory/context note: incident context must be reviewed for freshness before reuse.

Validation note: close incident follow-ups with what changed, what was validated, and what remains blocked.

## Approvals Topic

Topic name: Approvals
Topic ID: `<TOPIC_ID>`

Purpose: separate owner approval from execution.

Allowed work:

- record approval request IDs;
- approve or reject risky actions;
- define one-time permission boundaries.

Forbidden work:

- treating silence as approval;
- approving broad access;
- storing credential material.

Memory/context note: approval context expires after the named action or time window.

Validation note: every approved action needs a matching result report and delivery or event evidence when applicable.
