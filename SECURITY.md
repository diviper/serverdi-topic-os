# Security Policy

ServerDi Topic OS is a documentation-first repository. It must stay public-safe.

## Supported Scope

Security reports should focus on repository content, documentation examples, prompt templates, and process recommendations.

This repository does not contain production runtime configuration, live agent sessions, deployment inventories, credentials, or private operational data.

## Public-Safe Requirement

Do not submit examples that include:

- real Telegram group IDs or topic IDs;
- secrets, tokens, API keys, cookies, passwords, or private keys;
- env values or auth files;
- personal data, health data, medication data, billing data, family data, or relationship data;
- server IPs, VPN details, firewall details, raw logs, sessions, memory dumps, backups, runtime state, generated media, or private server paths.

Use placeholders such as `<TELEGRAM_GROUP_ID>`, `<TOPIC_ID>`, `<OPENCLAW_WORKSPACE>`, `<HERMES_WORKSPACE>`, `<YOUR_AGENT_STACK_PATH>`, and `<MODEL_PROVIDER/MODEL_NAME>`.

## Reporting Issues

Open a GitHub issue for documentation safety concerns, unclear boundary rules, missing validation steps, or risky prompt language.

If a report might contain sensitive information, remove the sensitive content first and describe the class of issue without exposing the data.

## Operator Guidance

- Keep public docs separate from private operations.
- Review every contribution for accidental disclosure.
- Treat generated examples as untrusted until inspected.
- Prefer small, bounded changes with clear validation evidence.
