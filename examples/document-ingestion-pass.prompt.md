# Document Ingestion Pass Prompt

```text
Task: document ingestion pass for one bounded outcome.

Document source:
<Describe source without private path>

Context lane:
- Telegram group: <TELEGRAM_GROUP_ID>
- Topic: <TOPIC_ID>
- Model: <MODEL_PROVIDER/MODEL_NAME>

Rules:
- Classify the document before summarizing.
- Do not ingest secrets, tokens, auth files, cookies, env values, personal data, health data, medication data, billing data, family data, relationship data, raw logs, sessions, memory dumps, backups, generated media, runtime state, or private paths into public output.
- Use placeholders only.
- Stop and request owner review if classification is private or unknown.
- Confirm external delivery by event/result, not by local file creation.

Output:
1. Classification
2. Public-safe summary
3. Redactions applied
4. Validation checklist
5. Blockers
```
