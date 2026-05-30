# Model Priority Map Example

This example documents model selection without exposing private provider details.

| Task Type | Preferred Model | Fallback Model | Approval Required | Notes |
| --- | --- | --- | --- | --- |
| Read-only scout | `<MODEL_PROVIDER/MODEL_NAME>` | `<MODEL_PROVIDER/MODEL_NAME>` | no | No paid or risky tools. |
| Patch pass | `<MODEL_PROVIDER/MODEL_NAME>` | `<MODEL_PROVIDER/MODEL_NAME>` | maybe | Approval required if scope expands. |
| Validation pass | `<MODEL_PROVIDER/MODEL_NAME>` | `<MODEL_PROVIDER/MODEL_NAME>` | maybe | Confirm checks before final report. |
| Paid delivery action | `<MODEL_PROVIDER/MODEL_NAME>` | none | yes | Requires `<APPROVAL_REQUEST_ID>`. |
| Private document ingestion | none | none | yes | Stop until owner review. |

Rules:

- Do not include real API keys, tokens, auth files, env values, or billing details.
- Do not document private fallback chains.
- Treat ambiguous approval as no approval.
