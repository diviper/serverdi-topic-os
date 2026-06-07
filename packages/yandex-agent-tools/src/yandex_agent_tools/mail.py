from __future__ import annotations

from dataclasses import dataclass, field
from email.utils import formataddr

from .accounts import AccountRegistry
from .safety import ConfirmationStore


@dataclass
class FakeMailBackend:
    """Fake backend для CI: никакой реальной сети, только in-memory сообщения."""

    messages: dict[str, list[dict[str, object]]] = field(default_factory=dict)
    sent: list[dict[str, object]] = field(default_factory=list)

    def list_messages(self, account_id: str, limit: int = 10) -> list[dict[str, object]]:
        return [self._headers_only(message) for message in self.messages.get(account_id, [])[:limit]]

    def search_messages(self, account_id: str, query: str, limit: int = 10) -> list[dict[str, object]]:
        query_lower = query.lower()
        found = []
        for message in self.messages.get(account_id, []):
            haystack = " ".join(str(message.get(key, "")) for key in ["from", "subject", "text_body", "snippet"]).lower()
            if query_lower in haystack:
                found.append(self._headers_only(message, include_snippet=True))
        return found[:limit]

    @staticmethod
    def _headers_only(message: dict[str, object], include_snippet: bool = False) -> dict[str, object]:
        allowed = {"id", "from", "to", "subject", "date", "message_id", "attachments", "html_body_present"}
        if include_snippet:
            allowed.add("snippet")
        return {key: value for key, value in message.items() if key in allowed}

    def read_message(self, account_id: str, message_id: str) -> dict[str, object]:
        for message in self.messages.get(account_id, []):
            if str(message.get("id")) == str(message_id):
                return dict(message)
        raise KeyError(f"Message not found: {message_id}")

    def send_message(self, payload: dict[str, object]) -> dict[str, object]:
        self.sent.append(dict(payload))
        return {"status": "sent", "saved_to_sent": True, "sent_count": len(self.sent)}


def default_fake_mail_backend() -> FakeMailBackend:
    return FakeMailBackend(
        messages={
            "work": [
                {
                    "id": "w1",
                    "from": "maintainer@example.org",
                    "to": ["work@example.com"],
                    "subject": "Reference implementation review",
                    "date": "2026-01-01T10:00:00Z",
                    "text_body": "Please review the public-safe connector example.",
                    "message_id": "<w1@example.org>",
                }
            ],
            "personal": [
                {
                    "id": "p1",
                    "from": "friend@example.org",
                    "to": ["personal@example.com"],
                    "subject": "Demo calendar note",
                    "date": "2026-01-01T11:00:00Z",
                    "text_body": "This fake fixture contains no private data.",
                    "message_id": "<p1@example.org>",
                }
            ],
        }
    )


class MailTool:
    """Mail tools with preview/confirm write safety."""

    def __init__(
        self,
        registry: AccountRegistry | None = None,
        backend: FakeMailBackend | None = None,
        confirmations: ConfirmationStore | None = None,
    ) -> None:
        self.registry = registry or AccountRegistry()
        self.backend = backend or default_fake_mail_backend()
        self.confirmations = confirmations or ConfirmationStore()

    def list(self, account_id: str, limit: int = 10) -> dict[str, object]:
        self.registry.get(account_id)
        return {"account_id": account_id, "messages": self.backend.list_messages(account_id, limit)}

    def search(self, account_id: str, query: str, limit: int = 10) -> dict[str, object]:
        self.registry.get(account_id)
        return {"account_id": account_id, "messages": self.backend.search_messages(account_id, query, limit)}

    def read(self, account_id: str, message_id: str) -> dict[str, object]:
        self.registry.get(account_id)
        return {"account_id": account_id, "message": self.backend.read_message(account_id, message_id)}

    def send_preview(self, account_id: str, to: list[str], subject: str, body_text: str) -> dict[str, object]:
        account = self.registry.get(account_id)
        body_with_signature = self._append_signature(body_text, account.mail_signature_text)
        payload = {
            "account_id": account_id,
            "from": formataddr((account.mail_display_name, account.mail_address)),
            "to": list(to),
            "subject": subject,
            "body_text": body_with_signature,
            "signature_applied": bool(account.mail_signature_text),
        }
        confirmation_id = self.confirmations.create("mail_send", payload)
        return {"requires_confirmation": True, "confirmation_id": confirmation_id, "preview": payload}

    def send_confirm(self, confirmation_id: str) -> dict[str, object]:
        action = self.confirmations.pop(confirmation_id)
        if action.action_type != "mail_send":
            raise ValueError("confirmation_id does not belong to mail_send")
        return self.backend.send_message(action.payload)

    def reply_preview(self, account_id: str, message_id: str, body_text: str) -> dict[str, object]:
        original = self.backend.read_message(account_id, message_id)
        subject = str(original.get("subject", ""))
        if not subject.lower().startswith("re:"):
            subject = f"Re: {subject}"
        preview = self.send_preview(account_id, [str(original.get("from"))], subject, body_text)
        preview["preview"]["in_reply_to"] = original.get("message_id")
        return preview

    def reply_confirm(self, confirmation_id: str) -> dict[str, object]:
        return self.send_confirm(confirmation_id)

    @staticmethod
    def _append_signature(body_text: str, signature_text: str) -> str:
        if not signature_text:
            return body_text
        return f"{body_text.rstrip()}\n\n-- \n{signature_text.strip()}"
