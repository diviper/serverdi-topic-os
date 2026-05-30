# Telegram Topic OS

Telegram forum topics can work as lightweight operational lanes for AI agent work. The goal is not to make Telegram the source of truth for infrastructure. The goal is to keep human-visible context, session references, and pass reports organized.

## Topic-Based Operations

A topic should represent one stable lane:

- documentation;
- validation;
- model routing;
- incident review;
- ingestion planning;
- release preparation;
- maintenance requests.

Avoid using one topic for unrelated work. Mixed topics create stale context and make final reports harder to trust.

## Topic, Session, and Model Maps

Maintain a small public-safe map with placeholders:

```text
Topic: <TOPIC_ID>
Purpose: documentation validation
Agent workspace: <OPENCLAW_WORKSPACE>
Model: <MODEL_PROVIDER/MODEL_NAME>
Current pass: read-only scout
```

Maps should avoid private IDs, real paths, live session filenames, raw logs, and runtime state.

## Active State Docs

Each active lane should have a current state document that records:

- current bounded outcome;
- last validated result;
- pending approval request such as `<APPROVAL_REQUEST_ID>`;
- known blockers;
- next recommended pass.

The active state document should be updated only after validation.

## Stale Context Risks

Telegram history is useful, but old messages can be wrong. Risks include:

- a previous model decision becoming outdated;
- an old topic ID being reused incorrectly;
- a local generated file being treated as delivered;
- a cancelled task appearing active;
- a private detail being copied into a public prompt.

Mitigation:

- quote only the minimum relevant context;
- validate state with current files or event results;
- use placeholders in public examples;
- close each pass with a final report.

## Placeholder Example

```text
Telegram group: <TELEGRAM_GROUP_ID>
Topic: <TOPIC_ID>
Pass: validation
Model: <MODEL_PROVIDER/MODEL_NAME>
Workspace: <YOUR_AGENT_STACK_PATH>
Result:
- Checked public docs.
- No real Telegram IDs included.
- Next pass: patch README quick start.
```
