from __future__ import annotations

import os

from .accounts import AccountRegistry, ContactRegistry
from .calendar import CalendarTool
from .mail import MailTool

registry = AccountRegistry()
contact_registry = ContactRegistry()
mail_tool = MailTool(registry=registry, contact_registry=contact_registry)
calendar_tool = CalendarTool(registry=registry, contact_registry=contact_registry)

try:
    from fastapi import Depends, FastAPI, Header, HTTPException
    from pydantic import BaseModel, Field
except ImportError:  # pragma: no cover - allows importing package without server extras
    FastAPI = None  # type: ignore[assignment]
else:
    app = FastAPI(title="Yandex Agent Tools Reference")

    def require_token(authorization: str | None = Header(default=None)) -> None:
        expected = os.getenv("YAT_API_TOKEN", "replace-with-local-token")
        if authorization != f"Bearer {expected}":
            raise HTTPException(status_code=401, detail="Unauthorized")

    class MailListRequest(BaseModel):
        account_id: str
        limit: int = 10

    class MailSearchRequest(BaseModel):
        account_id: str
        query: str
        limit: int = 10

    class MailReadRequest(BaseModel):
        account_id: str
        message_id: str

    class MailAttachmentInput(BaseModel):
        filename: str
        content_type: str = "application/octet-stream"
        content_base64: str

    class MailSendPreviewRequest(BaseModel):
        account_id: str
        to: list[str]
        subject: str
        body_text: str
        attachments: list[MailAttachmentInput] = Field(default_factory=list)

    class MailReplyPreviewRequest(BaseModel):
        account_id: str
        message_id: str
        body_text: str
        attachments: list[MailAttachmentInput] = Field(default_factory=list)

    def model_to_dict(model: BaseModel) -> dict[str, object]:
        dump = getattr(model, "model_dump", None)
        if dump is not None:
            return dump()
        return model.dict()

    class ConfirmRequest(BaseModel):
        confirmation_id: str
        explicit_confirm_text: str | None = None

    class CalendarListRequest(BaseModel):
        account_id: str
        start: str | None = None
        end: str | None = None

    class CalendarCreatePreviewRequest(BaseModel):
        account_id: str
        summary: str
        start: str
        end: str
        description: str = ""
        attendees: list[str] = []
        explicit_confirm_text: str | None = None

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/accounts")
    def accounts(_: None = Depends(require_token)) -> list[dict[str, object]]:
        return registry.list_public()

    @app.get("/contacts")
    def contacts(_: None = Depends(require_token)) -> list[dict[str, object]]:
        return contact_registry.list_public()

    @app.post("/tools/mail/list")
    def mail_list(request: MailListRequest, _: None = Depends(require_token)) -> dict[str, object]:
        return mail_tool.list(request.account_id, request.limit)

    @app.post("/tools/mail/search")
    def mail_search(request: MailSearchRequest, _: None = Depends(require_token)) -> dict[str, object]:
        return mail_tool.search(request.account_id, request.query, request.limit)

    @app.post("/tools/mail/read")
    def mail_read(request: MailReadRequest, _: None = Depends(require_token)) -> dict[str, object]:
        return mail_tool.read(request.account_id, request.message_id)

    @app.post("/tools/mail/send/preview")
    def mail_send_preview(request: MailSendPreviewRequest, _: None = Depends(require_token)) -> dict[str, object]:
        return mail_tool.send_preview(
            request.account_id,
            request.to,
            request.subject,
            request.body_text,
            attachments=[model_to_dict(item) for item in request.attachments],
        )

    @app.post("/tools/mail/send/confirm")
    def mail_send_confirm(request: ConfirmRequest, _: None = Depends(require_token)) -> dict[str, object]:
        return mail_tool.send_confirm(request.confirmation_id)

    @app.post("/tools/mail/reply/preview")
    def mail_reply_preview(request: MailReplyPreviewRequest, _: None = Depends(require_token)) -> dict[str, object]:
        return mail_tool.reply_preview(
            request.account_id,
            request.message_id,
            request.body_text,
            attachments=[model_to_dict(item) for item in request.attachments],
        )

    @app.post("/tools/mail/reply/confirm")
    def mail_reply_confirm(request: ConfirmRequest, _: None = Depends(require_token)) -> dict[str, object]:
        return mail_tool.reply_confirm(request.confirmation_id)

    @app.post("/tools/calendar/list")
    def calendar_list(request: CalendarListRequest, _: None = Depends(require_token)) -> dict[str, object]:
        return calendar_tool.list(request.account_id, start=request.start, end=request.end)

    @app.post("/tools/calendar/create/preview")
    def calendar_create_preview(
        request: CalendarCreatePreviewRequest,
        _: None = Depends(require_token),
    ) -> dict[str, object]:
        return calendar_tool.create_preview(
            request.account_id,
            request.summary,
            request.start,
            request.end,
            request.description,
            request.attendees,
            request.explicit_confirm_text,
        )

    @app.post("/tools/calendar/create/confirm")
    def calendar_create_confirm(request: ConfirmRequest, _: None = Depends(require_token)) -> dict[str, object]:
        return calendar_tool.create_confirm(request.confirmation_id, request.explicit_confirm_text)
