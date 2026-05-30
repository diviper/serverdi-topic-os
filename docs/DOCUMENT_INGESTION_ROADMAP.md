# Document Ingestion Roadmap

Document ingestion is useful, but it is also one of the easiest ways to leak private data. This roadmap describes public-safe patterns for future ingestion workflows.

## Safe Document Intake

Before ingestion, classify the document:

- public;
- internal but non-sensitive;
- private;
- contains secrets or credentials;
- contains personal, health, medication, billing, family, or relationship data;
- unknown.

Unknown documents should be treated as private until reviewed.

## LiteParse-Style Adapter Concept

A lightweight adapter can normalize documents before agent use:

1. accept a document reference;
2. extract text into a temporary review buffer;
3. classify sensitivity;
4. redact unsafe data;
5. produce a bounded summary;
6. discard temporary buffers according to policy.

The adapter should not publish raw extracted text by default.

## Document Classification

Recommended labels:

```text
PUBLIC_SAFE
PUBLIC_SAFE_WITH_PLACEHOLDERS
PRIVATE_DO_NOT_EXPORT
NEEDS_OWNER_REVIEW
REJECTED_CONTAINS_SECRETS
```

Classification should be visible in the final report.

## Public Examples

Public examples must not include:

- secrets, tokens, API keys, cookies, passwords, or private keys;
- real IDs;
- private workspace paths;
- server IPs;
- raw logs;
- sessions, memory dumps, backups, or runtime state;
- personal, health, medication, billing, family, or relationship data.

Use placeholders such as `<TELEGRAM_GROUP_ID>`, `<TOPIC_ID>`, `<OPENCLAW_WORKSPACE>`, `<HERMES_WORKSPACE>`, and `<MODEL_PROVIDER/MODEL_NAME>`.

## Validation Checklist

- [ ] The source document classification is recorded.
- [ ] Unsafe data is removed before public output.
- [ ] Public examples use placeholders only.
- [ ] The final output is reviewed for dangerous terms.
- [ ] Delivery is confirmed when an external action is required.
- [ ] Temporary review buffers are not committed.

## Future Ingestion Gateway

A future ingestion gateway could provide:

- document type detection;
- sensitivity scoring;
- redaction suggestions;
- owner approval workflow;
- event-based delivery confirmation;
- public-safe export mode.

The gateway should favor human approval over blind automation.
