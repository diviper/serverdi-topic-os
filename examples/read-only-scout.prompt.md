# Read-Only Scout Prompt

```text
Task: read-only scout for one bounded outcome.

Repository/worktree:
<YOUR_AGENT_STACK_PATH>

Question:
<Write the one question to answer>

Context lane:
- Telegram group: <TELEGRAM_GROUP_ID>
- Topic: <TOPIC_ID>
- Model: <MODEL_PROVIDER/MODEL_NAME>

Rules:
- Do not edit files.
- Do not run package managers.
- Do not touch Docker, OpenClaw runtime, Hermes runtime, Telegram runtime, secrets, sessions, memory, backups, generated media, or system config.
- Do not use paid tools without explicit approval.
- Do not copy private data into the report.

Output:
1. Answer
2. Evidence
3. Risks
4. Recommended next bounded pass
```
