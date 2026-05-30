# OpenClaw and Hermes Boundaries

OpenClaw and Hermes should be treated as separate operational contours. A documentation task may describe both at an architecture level, but it should not mix their runtime changes.

## Why Separate Contours Matter

Separate contours reduce accidental authority:

- OpenClaw can manage agent interaction and workspace tasks.
- Hermes can manage another automation or orchestration layer.
- Codex can operate on repository files.
- Docker can host services.
- Telegram topics can coordinate human-visible work.

When these concerns blend, a small agent request can unintentionally become a runtime change, model change, or production operation.

## No Mixed Runtime Changes

Do not change OpenClaw and Hermes runtime behavior in the same pass. Use separate tasks, separate reports, and separate validation.

Examples:

- A Codex documentation patch should not change OpenClaw runtime config.
- An OpenClaw model fallback review should not restart Hermes.
- A Telegram topic cleanup should not alter Docker services.

## Model, Auth, and Fallback Caution

Model routing, auth configuration, and fallback behavior are high-risk areas. Treat them as owner-approved tasks only.

Safe public docs may discuss:

- model priority maps with `<MODEL_PROVIDER/MODEL_NAME>`;
- approval requirements;
- validation patterns;
- architecture-level boundaries.

Public docs must not include real tokens, auth files, env values, endpoint credentials, or private fallback chains.

## Telegram Boundary Rules

Telegram topics are coordination lanes, not proof of runtime state.

- Use `<TELEGRAM_GROUP_ID>` and `<TOPIC_ID>` in examples.
- Do not publish real chat IDs or thread IDs.
- Do not assume an old topic contains current state.
- Link each topic to a current state document when possible.
- Confirm delivery or event success instead of trusting local generation.

## Production Restart Rule

No production restart without explicit owner approval.

Approval should state:

- affected contour;
- reason for restart;
- expected impact;
- rollback plan;
- validation method;
- approval request ID such as `<APPROVAL_REQUEST_ID>`.

If any of these are missing, stop and request clarification.
