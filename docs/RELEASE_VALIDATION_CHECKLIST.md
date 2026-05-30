# Release Validation Checklist

Use this checklist before publishing ServerDi Topic OS documentation, examples, prompt templates, or lightweight tools. The goal is to make every release reviewable, public-safe, and tied to a clear human decision.

Record the final decision in the release notes, pull request, or maintainer handoff comment.

## 1. Scope Check

Verify:

- the release has one clear purpose;
- changed files match the release purpose;
- no unrelated cleanup, runtime work, dependency work, or broad rewrites are included;
- any tool changes are lightweight and documented.

Why it matters: narrow releases are easier to review and safer to publish.

Blockers:

- the release mixes unrelated docs, prompts, tools, and operational changes;
- the release includes private runtime details;
- the release cannot be explained as one bounded outcome.

Can be fixed later:

- minor wording improvements;
- follow-up examples that are useful but not required for this release.

## 2. Public-Safety Check

Verify:

- all examples use placeholders such as `<TELEGRAM_GROUP_ID>`, `<TOPIC_ID>`, `<OPENCLAW_WORKSPACE>`, `<HERMES_WORKSPACE>`, `<YOUR_AGENT_STACK_PATH>`, and `<MODEL_PROVIDER/MODEL_NAME>`;
- no real identifiers, credentials, env values, private paths, raw logs, sessions, memory dumps, backups, personal data, medical data, billing data, or internal deployment details are present;
- safety warnings describe classes of risk without exposing real values.

Why it matters: this repository is public and should never reveal private operations or sensitive data.

Blockers:

- any real private value or private path;
- any raw operational output copied into public docs;
- any private deployment detail that would help reconstruct a real environment.

Can be fixed later:

- adding more placeholder examples;
- improving wording after the unsafe content has been removed.

## 3. Examples Check

Verify:

- examples are copyable but not environment-specific;
- placeholders are clearly visible;
- examples avoid live IDs, real model routing, private workspaces, and operational state;
- example outputs do not imply that local generation equals successful delivery.

Why it matters: examples are often copied directly into real workflows.

Blockers:

- real IDs or private paths in examples;
- example prompts that authorize broad or unsafe access;
- examples that skip validation for risky actions.

Can be fixed later:

- more examples for additional roles or teams;
- formatting improvements that do not affect safety.

## 4. Prompt-Template Check

Verify:

- each prompt has one bounded outcome;
- read-only prompts forbid edits and risky tool use;
- patch prompts define allowed files and validation;
- prompts stop on approval, privacy, or scope ambiguity;
- prompt language does not ask agents to continue old unrelated tasks.

Why it matters: prompt templates are operational controls, not just documentation.

Blockers:

- prompt language that allows unbounded work;
- prompts that permit access to private runtime state;
- prompts that bypass approval for risky or paid actions.

Can be fixed later:

- adding optional report fields;
- improving tone while preserving the safety boundary.

## 5. Scanner Check

Verify:

- the public safety scanner runs from the repository root;
- normal mode reports no blockers;
- strict mode passes before release;
- any warning is inspected and explained before publishing.

Run:

```bash
python tools/public_safety_scan.py .
python tools/public_safety_scan.py . --strict
```

Why it matters: automated checks catch common disclosure markers before manual review.

Blockers:

- scanner blockers;
- strict scanner failure before a public release;
- unexplained warnings in release-critical files.

Can be fixed later:

- scanner rule tuning for lower-noise warnings;
- richer machine-readable reports.

## 6. GitHub Actions Check

Verify:

- the public safety scan workflow is present;
- the workflow runs on `push` and `pull_request`;
- the workflow uses standard Python;
- required checks pass before merge or release.

Why it matters: release safety should not depend only on local commands.

Blockers:

- failing release-critical workflow;
- workflow disabled or removed without review;
- workflow no longer runs the scanner in strict mode.

Can be fixed later:

- optional matrix expansion;
- badge or reporting polish.

## 7. Release Notes Check

Verify:

- release notes describe what changed;
- validation commands are listed;
- privacy and sanitization status is recorded;
- known limitations are explicit;
- no private details are copied into the notes.

Why it matters: maintainers need a clean audit trail after publication.

Blockers:

- release notes hide validation failure;
- release notes include sensitive content;
- release notes claim delivery or safety that was not verified.

Can be fixed later:

- grammar cleanup;
- additional context links to public docs.

## 8. Version/Tag Check

Verify:

- the version or tag name matches the release scope;
- the tag points to the reviewed commit;
- the tag is created after validation, not before;
- release artifacts come from the same commit that was reviewed.

Why it matters: users need to know exactly what was validated.

Blockers:

- tag points to the wrong commit;
- release artifacts were generated from an unreviewed state;
- version notes do not match the actual content.

Can be fixed later:

- additional metadata;
- clearer tag naming rules for future releases.

## 9. Manual Review Check

Verify:

- at least one maintainer reviews the diff;
- scanner output is not treated as the only review;
- the reviewer checks examples, prompts, and tool behavior;
- the reviewer confirms no private runtime details were touched.

Why it matters: automated checks cannot understand every disclosure or operational risk.

Blockers:

- no human review for a public release;
- unresolved privacy concern;
- unresolved mismatch between release notes and actual changes.

Can be fixed later:

- non-blocking copy edits;
- future checklist refinements.

## 10. Final Go/No-Go Decision

Record:

```text
Release:
Commit:
Scope:
Scanner result:
GitHub Actions result:
Manual reviewer:
Privacy/sanitization result:
Known limitations:
Decision: GO / NO-GO
Reason:
Next action:
```

Go when:

- scope is bounded;
- scanner and release-critical checks pass;
- manual review is complete;
- release notes are public-safe;
- no blockers remain.

No-go when:

- any blocker remains;
- validation is incomplete;
- privacy status is unclear;
- the release includes unrelated operational changes.

If the decision is no-go, create one bounded follow-up task and do not publish until it is resolved.
