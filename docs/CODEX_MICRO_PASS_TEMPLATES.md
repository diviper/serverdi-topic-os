# Codex Micro-Pass Templates

These templates are designed for narrow, auditable agent work. Replace placeholders before use.

## Read-Only Scout

```text
Task: read-only scout for one bounded question.

Scope:
- Repository/worktree: <YOUR_AGENT_STACK_PATH>
- Telegram topic: <TELEGRAM_GROUP_ID>/<TOPIC_ID>
- Model: <MODEL_PROVIDER/MODEL_NAME>

Rules:
- Do not edit files.
- Do not call paid tools.
- Do not inspect secrets, sessions, memory, backups, raw logs, or runtime state.
- Do not restart or reconfigure services.

Output:
1. Findings
2. Risks
3. Missing information
4. Recommended next bounded pass
```

## Patch Pass

```text
Task: make one scoped patch.

Bounded outcome:
<Describe the single expected outcome>

Allowed files:
<List files or directories>

Rules:
- Edit only the allowed files.
- Do not touch runtime config or private data.
- Validate before final report.
- Stop if the task requires secrets, paid tools, production access, or unrelated cleanup.

Final report:
- Changed files
- Validation commands/results
- Sanitization result
- What was not touched
- Remaining blockers
```

## Validation Pass

```text
Task: validate one completed change.

Inputs:
- Commit or working tree change: <APPROVAL_REQUEST_ID>
- Expected outcome: <Describe expected behavior>

Rules:
- Do not edit files unless explicitly requested.
- Inspect relevant outputs only.
- Treat local generation as incomplete until delivery or event success is confirmed.

Output:
1. Validation checks performed
2. Pass/fail result
3. Evidence
4. Residual risk
```

## Rollback Check

```text
Task: decide whether rollback is required.

Context:
- Change under review: <APPROVAL_REQUEST_ID>
- Affected contour: OpenClaw / Hermes / Codex / Docker / Telegram / docs

Rules:
- Prefer rollback when scope was exceeded or private data was exposed.
- Prefer a follow-up patch when the issue is narrow and public-safe.
- Do not perform rollback without explicit approval.

Output:
1. Rollback required: yes/no
2. Reason
3. Safer next action
```

## Final Report

```text
Task: write final report for one pass.

Report:
1. Outcome
2. Changed files
3. Validation
4. Sanitization
5. Commit hash
6. Push result
7. What was not touched
8. Blockers
9. Next recommended pass
```

## Documentation-Only Pass

```text
Task: create or update public-safe documentation.

Rules:
- Use placeholders only.
- Do not include raw logs, private paths, server IPs, env values, sessions, memory dumps, backups, personal data, or billing data.
- Mention risky terms only as safety warnings.
- Validate with a recursive text scan before commit.

Output:
- Files changed
- Scan result
- Terms reviewed and why they are safe
```
