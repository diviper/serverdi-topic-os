# Topic Map Example: Documentation-Heavy Workspace

This public-safe example shows how a documentation-heavy workspace can separate intake, parsing, review, approved knowledge, stale context cleanup, and release notes.

Telegram group: `<TELEGRAM_GROUP_ID>`
Documentation workspace: `<YOUR_AGENT_STACK_PATH>`
Default model: `<MODEL_PROVIDER/MODEL_NAME>`

## Intake Topic

Topic name: Intake
Topic ID: `<TOPIC_ID>`

Purpose: receive documentation requests and classify whether they are public-safe.

Allowed work:

- capture a short request summary;
- assign a classification;
- define the next bounded pass.

Forbidden work:

- pasting private source material;
- accepting unclassified input as public;
- starting parsing before the source is approved for public handling.

Memory/context note: intake summaries are temporary. Promote only reviewed, public-safe context to the next topic.

Validation note: each intake item should end with a classification and a next pass decision.

## Parsing Topic

Topic name: Parsing
Topic ID: `<TOPIC_ID>`

Purpose: plan extraction or transformation of approved public-safe documents.

Allowed work:

- define parser scope;
- identify expected output shape;
- record placeholder requirements.

Forbidden work:

- parsing private source material;
- publishing extracted text without review;
- storing intermediate files as public artifacts.

Memory/context note: parser notes should not become approved knowledge until reviewed.

Validation note: verify that generated output uses placeholders and does not include source-only metadata.

## Review Topic

Topic name: Review
Topic ID: `<TOPIC_ID>`

Purpose: human review of drafted docs, examples, prompts, and templates.

Allowed work:

- review public-safety scanner output;
- check placeholder use;
- confirm clarity and scope.

Forbidden work:

- approving content without reading changed files;
- accepting broad agent authority in templates;
- moving drafts to release without validation.

Memory/context note: review comments are not final documentation until merged into the repository.

Validation note: record reviewer, files reviewed, scanner result, and required changes.

## Approved Knowledge Topic

Topic name: Approved Knowledge
Topic ID: `<TOPIC_ID>`

Purpose: track public-safe knowledge that has passed review and can be reused.

Allowed work:

- link approved docs;
- record reusable public patterns;
- identify next maintenance date.

Forbidden work:

- adding unreviewed drafts;
- storing private context;
- using old approval for new content.

Memory/context note: approved knowledge should reference repository files and commits.

Validation note: each entry should include source file, commit, reviewer, and date of approval.

## Stale Context Cleanup Topic

Topic name: Stale Context Cleanup
Topic ID: `<TOPIC_ID>`

Purpose: review old topic context and decide what should be archived, refreshed, or discarded.

Allowed work:

- identify stale summaries;
- mark outdated assumptions;
- create scoped cleanup tasks.

Forbidden work:

- deleting source-of-truth repository content without review;
- treating old topic history as current state;
- copying obsolete private context into public docs.

Memory/context note: stale context is expected. Refresh from repository files, current issues, and reviewed release notes.

Validation note: record what was marked stale, why, and what replacement source should be used.

## Release Notes Topic

Topic name: Release Notes
Topic ID: `<TOPIC_ID>`

Purpose: prepare public-safe release notes for documentation and lightweight tool releases.

Allowed work:

- summarize changes from reviewed commits;
- include validation commands;
- record privacy and sanitization status.

Forbidden work:

- claiming validation that was not run;
- including private operational details;
- publishing notes before final go/no-go.

Memory/context note: release notes should point to commits, pull requests, and public docs rather than topic-only claims.

Validation note: final release notes should match the release validation checklist and include scanner and test results.
