# CostGate Approval Policy

CostGate is a simple approval model for paid or risky AI agent actions. It separates request, approval, execution, and delivery confirmation.

## When Approval Is Required

Require explicit owner approval before:

- paid API calls;
- high-cost model runs;
- external delivery actions;
- production changes;
- service restarts;
- model fallback changes;
- auth or credential changes;
- private document ingestion;
- actions that may expose sensitive data.

## Pending Request Concept

An agent may create a pending request:

```text
Approval request: <APPROVAL_REQUEST_ID>
Action: use <MODEL_PROVIDER/MODEL_NAME> for validation
Reason: confirm delivery result
Estimated risk: paid tool call
Owner decision: pending
```

Pending means no execution yet. The agent must wait for owner approval.

## Owner Approval Requirement

Approval should be explicit and specific:

- who approved;
- what was approved;
- affected contour;
- budget or risk limit;
- expiration or one-time scope;
- validation method.

Ambiguous approval should be treated as no approval.

## Direct Bypass Risk

Bypassing the approval path creates several risks:

- paid calls without consent;
- untracked operational changes;
- hidden delivery failures;
- weak audit trail;
- accidental exposure of private data.

Agents should stop and report when a tool path would bypass approval.

## No Paid Calls Without Explicit Approval

No paid calls should be made just because a local file can be generated or a prompt appears ready. Approval must happen before the paid action.

## Confirm Delivery, Not Just Generation

Success must be confirmed by delivery or event result when the task depends on an external action.

Examples of insufficient proof:

- a local message file exists;
- a draft prompt was created;
- a media file was rendered locally.

Examples of stronger proof:

- API response confirms delivery;
- event log confirms accepted action;
- target system shows the expected update;
- recipient topic contains the delivered message.

Public documentation should describe these patterns without including private logs or real identifiers.
