# Topic Map Example: Solo Maintainer

This public-safe example shows how one maintainer can separate agent work into clear Telegram forum topics without publishing real IDs, private paths, runtime state, or account-specific material.

Telegram group: `<TELEGRAM_GROUP_ID>`
Agent workspace: `<YOUR_AGENT_STACK_PATH>`
Default model: `<MODEL_PROVIDER/MODEL_NAME>`

## Control Topic

Topic name: Control
Topic ID: `<TOPIC_ID>`

Purpose: owner decisions, pass approvals, scope changes, and final go/no-go calls.

Allowed work:

- approve or reject one bounded pass;
- record current operating priority;
- decide whether a pending action is allowed.

Forbidden work:

- storing credentials or account-specific values;
- running tool actions directly from approval notes;
- mixing implementation work into decision records.

Memory/context note: treat this topic as a decision lane, not a long-term memory store. Copy only public-safe decisions into docs.

Validation note: each approval should name the bounded outcome, affected files or docs, and expected validation command.

## Operations Topic

Topic name: Operations
Topic ID: `<TOPIC_ID>`

Purpose: routine maintenance planning and status reporting at an architecture level.

Allowed work:

- plan read-only scout passes;
- report public-safe validation results;
- track follow-up tasks for docs, examples, and lightweight tools.

Forbidden work:

- changing Docker, OpenClaw, Hermes, or Telegram runtime configuration;
- copying runtime output into public notes;
- escalating a scout pass into a patch pass without a new approval.

Memory/context note: old operation notes may be stale. Confirm current state from the repository before acting.

Validation note: close each operation pass with the command run, result, and next bounded outcome.

## Documents Topic

Topic name: Documents
Topic ID: `<TOPIC_ID>`

Purpose: public documentation drafting, review, and release preparation.

Allowed work:

- draft public-safe documentation;
- review placeholder use;
- check links and checklist coverage.

Forbidden work:

- adding private document contents;
- including account-specific identifiers;
- publishing unreviewed extracted text.

Memory/context note: summaries should be treated as drafts until reviewed against the source document.

Validation note: run the public safety scanner before moving document work to release review.

## Ideas/Backlog Topic

Topic name: Ideas/Backlog
Topic ID: `<TOPIC_ID>`

Purpose: collect future ideas without granting agents permission to implement them.

Allowed work:

- capture possible improvements;
- group ideas into small follow-up tasks;
- mark stale or rejected ideas.

Forbidden work:

- treating ideas as approvals;
- combining unrelated backlog items into one pass;
- storing private-life notes or account-specific material.

Memory/context note: backlog items are not active state. Promote only one item at a time into the Control topic.

Validation note: a backlog item is ready only when it has one bounded outcome and a public-safe acceptance check.

## Incident Topic

Topic name: Incident
Topic ID: `<TOPIC_ID>`

Purpose: coordinate public-safe incident review and lessons learned.

Allowed work:

- record sanitized symptoms;
- define a read-only audit pass;
- write public-safe follow-up tasks.

Forbidden work:

- copying raw operational output;
- exposing private infrastructure details;
- performing recovery actions without explicit approval.

Memory/context note: incident notes expire quickly. Re-check current repository and documented state before using old context.

Validation note: final incident notes should separate confirmed facts, assumptions, follow-up tasks, and no-go reasons.

## Personal/Private Boundary Note

Keep private-life material, account-specific material, and non-project records out of public topic maps. Use a separate private process for anything that cannot be shared in an open-source repository.
