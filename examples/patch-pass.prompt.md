# Patch Pass Prompt

```text
Task: patch pass for one bounded outcome.

Bounded outcome:
<Describe the exact expected change>

Allowed files:
<List files>

Context lane:
- Telegram group: <TELEGRAM_GROUP_ID>
- Topic: <TOPIC_ID>
- Model: <MODEL_PROVIDER/MODEL_NAME>

Rules:
- Work only inside <YOUR_AGENT_STACK_PATH>.
- Edit only the allowed files.
- Do not touch Docker, OpenClaw runtime, Hermes runtime, Telegram runtime, env files, secrets, sessions, memory, backups, generated media, or system config.
- Use placeholders for IDs and paths.
- Validate before commit.

Validation:
<List required checks>

Final report:
- Changed files
- Validation result
- Sanitization result
- Commit hash
- Push result
- What was not touched
```
