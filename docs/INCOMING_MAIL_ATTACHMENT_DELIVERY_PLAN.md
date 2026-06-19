# Incoming Mail Attachment Delivery Plan

This plan documents a future public-safe workflow for delivering inbound mail attachments from a private connector to an owner-controlled chat or operator channel.

The current reference package supports mail list/search/read, incoming attachment metadata, and outgoing attachment preview/confirm. It does not yet download inbound attachment bytes. This plan describes how to add that capability without exposing private mail content, chat identifiers, provider credentials, local paths, or binary payloads in public docs or tests.

## Target operator workflow

A private deployment should support this bounded flow:

1. The owner asks the agent to find mail from a known sender or contact alias.
2. The agent searches the mailbox and returns safe message summaries.
3. The owner selects one message.
4. The agent lists that message's attachment metadata: `attachment_id`, filename, content type, and size.
5. The owner asks to deliver one or more attachments.
6. The connector returns a preview with delivery metadata and a one-time confirmation id.
7. The owner confirms.
8. The private adapter downloads the attachment bytes, stores them in a short-lived private temp location, and sends them to the owner-controlled chat as files.
9. The adapter reports a delivery receipt and deletes or expires temporary files.

## Proposed connector surface

The public reference package should model the flow with fake backends only:

```text
POST /tools/mail/attachments/list
POST /tools/mail/attachments/deliver/preview
POST /tools/mail/attachments/deliver/confirm
```

### Attachment list request

```json
{
  "account_id": "personal",
  "message_id": "message-1"
}
```

### Attachment list response

```json
{
  "account_id": "personal",
  "message_id": "message-1",
  "attachments": [
    {
      "attachment_id": "attachment-1",
      "filename": "report.pdf",
      "content_type": "application/pdf",
      "size": 12345
    }
  ]
}
```

### Delivery preview request

```json
{
  "account_id": "personal",
  "message_id": "message-1",
  "attachment_ids": ["attachment-1"],
  "delivery_target": "owner_chat"
}
```

### Delivery preview response

```json
{
  "requires_confirmation": true,
  "confirmation_id": "one-time-id",
  "preview": {
    "account_id": "personal",
    "message_id": "message-1",
    "delivery_target": "owner_chat",
    "attachments": [
      {
        "attachment_id": "attachment-1",
        "filename": "report.pdf",
        "content_type": "application/pdf",
        "size": 12345
      }
    ]
  }
}
```

### Delivery confirm response

```json
{
  "status": "delivered",
  "delivery_target": "owner_chat",
  "delivered_count": 1,
  "attachments": [
    {
      "attachment_id": "attachment-1",
      "filename": "report.pdf",
      "content_type": "application/pdf",
      "size": 12345
    }
  ]
}
```

## Safety rules

- Search and list operations must stay metadata-first.
- The public package must use fake attachment bytes only.
- Preview responses must never include raw bytes, base64, provider URLs, local temp paths, chat ids, tokens, or message bodies.
- Confirmation ids must be one-time-use.
- Attachment ids must be scoped to the selected message and account.
- Filenames must be sanitized before storage or chat delivery.
- Content types must be validated and treated as advisory, not trusted.
- Per-file and total delivery size limits must be enforced.
- A private deployment should use short-lived temp files and delete them after delivery or expiry.
- The chat delivery adapter must target an owner-controlled destination configured outside the public repository.
- Delivery receipts should report metadata and status only.

## Implementation tasks

1. Add fake inbound attachment bytes to fixture objects while keeping read/list responses metadata-only.
2. Add `MailTool.list_attachments(account_id, message_id)`.
3. Add `MailTool.deliver_attachments_preview(account_id, message_id, attachment_ids, delivery_target)`.
4. Add `MailTool.deliver_attachments_confirm(confirmation_id)` with one-time confirmation semantics.
5. Add FastAPI request/response models and endpoints for list, preview, and confirm.
6. Add tests for metadata-only list responses.
7. Add tests that preview responses never expose bytes/base64/temp paths.
8. Add tests for repeated confirmation rejection.
9. Add tests for invalid attachment ids, unsafe filenames, invalid content types, per-file size, and total size limits.
10. Add docs for private Telegram/chat adapter responsibilities without including any real chat identifiers.
11. Run package tests, public safety scanner strict mode, private-marker grep, and `git diff --check` before PR.

## Out of scope for the public repository

- Real IMAP attachment download implementation.
- Real Telegram Bot API calls.
- Real chat ids, topic ids, user ids, or delivery logs.
- Real mailbox contents or provider message ids.
- Real temp directories, server paths, or uploaded files.
- Antivirus or DLP integrations beyond documenting private deployment hooks.

## Validation commands

```bash
PYTHONPATH=packages/yandex-agent-tools/src python -m pytest packages/yandex-agent-tools/tests -q
python tools/public_safety_scan.py . --strict
git grep -n -E 'CHAT_ID|THREAD_ID|PRIVATE_PATH|TOKEN|SECRET' -- . ':!tools/public_safety_scan.py' || true
git diff --check
```
