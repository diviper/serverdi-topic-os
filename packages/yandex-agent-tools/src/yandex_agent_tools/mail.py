from __future__ import annotations

import base64
import binascii
import mimetypes
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any
from email.header import decode_header, make_header
from email.utils import formataddr

from .accounts import AccountRegistry, ContactRegistry, normalize_alias
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
            headers = self._headers_only(message, include_snippet=True)
            haystack = " ".join(str(headers.get(key, "")) for key in ["from", "subject", "snippet"]).lower()
            haystack += " " + str(message.get("text_body", "")).lower()
            if query_lower in haystack:
                found.append(headers)
        return found[:limit]

    @classmethod
    def _headers_only(cls, message: dict[str, object], include_snippet: bool = False) -> dict[str, object]:
        allowed = {"id", "from", "to", "subject", "date", "message_id", "attachments", "html_body_present"}
        if include_snippet:
            allowed.add("snippet")
        headers = {key: value for key, value in message.items() if key in allowed}
        for key in ["from", "subject", "snippet"]:
            if key in headers:
                headers[key] = cls._decode_mime_header(str(headers[key]))
        if "to" in headers and isinstance(headers["to"], list):
            headers["to"] = [cls._decode_mime_header(str(value)) for value in headers["to"]]
        return headers

    @staticmethod
    def _decode_mime_header(value: str) -> str:
        try:
            return str(make_header(decode_header(value)))
        except Exception:
            return value

    def read_message(self, account_id: str, message_id: str) -> dict[str, object]:
        for message in self.messages.get(account_id, []):
            if str(message.get("id")) == str(message_id):
                return dict(message)
        raise KeyError(f"Message not found: {message_id}")

    def send_message(self, payload: dict[str, object]) -> dict[str, object]:
        self.sent.append(dict(payload))
        result: dict[str, object] = {"status": "sent", "saved_to_sent": True, "sent_count": len(self.sent)}
        attachments = attachment_metadata(payload.get("attachments", []))
        if attachments:
            result["attachments"] = attachments
        return result


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




def attachment_metadata(attachments: object) -> list[dict[str, object]]:
    if not isinstance(attachments, Sequence) or isinstance(attachments, (str, bytes, bytearray)):
        return []
    metadata: list[dict[str, object]] = []
    for attachment in attachments:
        if not isinstance(attachment, Mapping):
            continue
        metadata.append(
            {
                "filename": str(attachment.get("filename") or "attachment"),
                "content_type": str(attachment.get("content_type") or "application/octet-stream"),
                "size": int(attachment.get("size") or len(attachment.get("content_bytes") or b"")),
            }
        )
    return metadata

class MailTool:
    """Mail tools with preview/confirm write safety."""

    MAX_ATTACHMENT_BYTES = 20 * 1024 * 1024
    MAX_TOTAL_ATTACHMENT_BYTES = 20 * 1024 * 1024
    MAX_ATTACHMENTS = 10
    MIME_TYPE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9!#$&^_.+-]{0,126}/[A-Za-z0-9][A-Za-z0-9!#$&^_.+-]{0,126}$")

    def __init__(
        self,
        registry: AccountRegistry | None = None,
        contact_registry: ContactRegistry | None = None,
        backend: FakeMailBackend | None = None,
        confirmations: ConfirmationStore | None = None,
    ) -> None:
        self.registry = registry or AccountRegistry()
        self.contact_registry = contact_registry or ContactRegistry()
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

    def send_preview(
        self,
        account_id: str,
        to: list[str],
        subject: str,
        body_text: str,
        *,
        attachments: Sequence[Mapping[str, Any]] | None = None,
    ) -> dict[str, object]:
        account = self.registry.get(account_id)
        recipients, aliases = self._resolve_recipients(to)
        body_with_signature = self._append_signature(body_text, account.mail_signature_text)
        attachment_payloads = self._normalize_attachments(attachments)
        payload = {
            "account_id": account_id,
            "from": formataddr((account.mail_display_name, account.mail_address)),
            "to": recipients,
            "subject": subject,
            "body_text": body_with_signature,
            "signature_applied": bool(account.mail_signature_text),
            "attachments": attachment_payloads,
        }
        confirmation_id = self.confirmations.create("mail_send", payload)
        preview_payload = dict(payload)
        preview_payload["attachments"] = attachment_metadata(attachment_payloads)
        return {
            "requires_confirmation": True,
            "confirmation_id": confirmation_id,
            "preview": preview_payload,
            "recipient_aliases_resolved": aliases,
        }

    def send_confirm(self, confirmation_id: str) -> dict[str, object]:
        action = self.confirmations.pop(confirmation_id)
        if action.action_type != "mail_send":
            raise ValueError("confirmation_id does not belong to mail_send")
        return self.backend.send_message(action.payload)

    def reply_preview(
        self,
        account_id: str,
        message_id: str,
        body_text: str,
        *,
        attachments: Sequence[Mapping[str, Any]] | None = None,
    ) -> dict[str, object]:
        original = self.backend.read_message(account_id, message_id)
        subject = FakeMailBackend._decode_mime_header(str(original.get("subject", "")))
        if not subject.lower().startswith("re:"):
            subject = f"Re: {subject}"
        preview = self.send_preview(account_id, [str(original.get("from"))], subject, body_text, attachments=attachments)
        preview["preview"]["in_reply_to"] = original.get("message_id")
        return preview

    def reply_confirm(self, confirmation_id: str) -> dict[str, object]:
        return self.send_confirm(confirmation_id)


    @classmethod
    def _normalize_attachments(
        cls, attachments: Sequence[Mapping[str, Any]] | None
    ) -> list[dict[str, object]]:
        if not attachments:
            return []
        if len(attachments) > cls.MAX_ATTACHMENTS:
            raise ValueError(f"too many attachments; maximum is {cls.MAX_ATTACHMENTS}")
        normalized: list[dict[str, object]] = []
        total_size = 0
        for index, attachment in enumerate(attachments, start=1):
            if not isinstance(attachment, Mapping):
                raise ValueError(f"attachment {index} must be an object")
            filename = cls._safe_attachment_filename(str(attachment.get("filename") or f"attachment-{index}"))
            content_type = cls._safe_content_type(
                str(attachment.get("content_type") or "").strip(),
                filename=filename,
            )
            content_base64 = str(attachment.get("content_base64") or "")
            if not content_base64:
                raise ValueError(f"attachment {filename} is missing content_base64")
            if cls._decoded_base64_size_upper_bound(content_base64) > cls.MAX_ATTACHMENT_BYTES:
                raise ValueError(f"attachment {filename} is too large for the configured limit")
            try:
                content_bytes = base64.b64decode(content_base64.encode("ascii"), validate=True)
            except (UnicodeEncodeError, binascii.Error) as exc:
                raise ValueError(f"attachment {filename} has invalid base64 content") from exc
            if len(content_bytes) > cls.MAX_ATTACHMENT_BYTES:
                raise ValueError(
                    f"attachment {filename} is too large: {len(content_bytes)} bytes > {cls.MAX_ATTACHMENT_BYTES}"
                )
            total_size += len(content_bytes)
            if total_size > cls.MAX_TOTAL_ATTACHMENT_BYTES:
                raise ValueError(
                    f"attachments are too large in total: {total_size} bytes > {cls.MAX_TOTAL_ATTACHMENT_BYTES}"
                )
            normalized.append(
                {
                    "filename": filename,
                    "content_type": content_type,
                    "size": len(content_bytes),
                    "content_bytes": content_bytes,
                }
            )
        return normalized

    @classmethod
    def _safe_content_type(cls, content_type: str, *, filename: str) -> str:
        value = content_type or mimetypes.guess_type(filename)[0] or "application/octet-stream"
        if not cls.MIME_TYPE_RE.fullmatch(value):
            raise ValueError(f"attachment {filename} has invalid content_type")
        return value

    @staticmethod
    def _decoded_base64_size_upper_bound(content_base64: str) -> int:
        return ((len(content_base64.strip()) + 3) // 4) * 3

    @staticmethod
    def _safe_attachment_filename(filename: str) -> str:
        name = filename.replace("\x00", "").strip()
        name = name.replace("\\", "/").split("/")[-1]
        name = re.sub(r"[\x00-\x1f\x7f]", "_", name)
        name = name.strip(" .")
        return name or "attachment"

    def _resolve_recipients(self, recipients: list[str]) -> tuple[list[str], list[str]]:
        resolved: list[str] = []
        aliases: list[str] = []
        for raw in recipients:
            value = str(raw).strip()
            if not value:
                continue
            alias = normalize_alias(value)
            account = self.registry.maybe_get(alias)
            if account is not None:
                resolved.append(account.mail_address)
                aliases.append(alias)
                continue
            contact = self.contact_registry.maybe_get(alias)
            if contact is not None:
                resolved.append(contact.email)
                aliases.append(alias)
                continue
            resolved.append(value)
        return resolved, aliases

    @staticmethod
    def _append_signature(body_text: str, signature_text: str) -> str:
        if not signature_text:
            return body_text
        return f"{body_text.rstrip()}\n\n-- \n{signature_text.strip()}"
