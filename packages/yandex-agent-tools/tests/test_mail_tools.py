from yandex_agent_tools.accounts import ContactConfig, ContactRegistry
from yandex_agent_tools.mail import FakeMailBackend, MailTool


def test_mail_list_search_and_read_use_fake_backend():
    tool = MailTool()

    listed = tool.list("work", limit=5)
    searched = tool.search("work", "review")
    read = tool.read("work", "w1")

    assert listed["messages"][0]["id"] == "w1"
    assert searched["messages"][0]["subject"] == "Reference implementation review"
    assert read["message"]["text_body"] == "Please review the public-safe connector example."


def test_mail_send_preview_then_confirm_applies_signature_once():
    tool = MailTool()

    preview = tool.send_preview("personal", ["reader@example.org"], "Hello", "Draft body")
    body = preview["preview"]["body_text"]
    result = tool.send_confirm(preview["confirmation_id"])

    assert preview["requires_confirmation"] is True
    assert preview["preview"]["from"] == "Personal Agent <personal@example.com>"
    assert "-- \nRegards," in body
    assert result == {"status": "sent", "saved_to_sent": True, "sent_count": 1}


def test_mail_confirmation_id_is_one_time_use():
    tool = MailTool()
    preview = tool.send_preview("work", ["reader@example.org"], "Hello", "Draft body")

    tool.send_confirm(preview["confirmation_id"])

    try:
        tool.send_confirm(preview["confirmation_id"])
    except KeyError as exc:
        assert "Unknown or already used" in str(exc)
    else:
        raise AssertionError("confirmation_id was reused")


def test_mail_reply_preview_sets_re_subject_and_in_reply_to():
    tool = MailTool()

    preview = tool.reply_preview("work", "w1", "Thanks for the review.")

    assert preview["preview"]["subject"] == "Re: Reference implementation review"
    assert preview["preview"]["in_reply_to"] == "<w1@example.org>"


def test_mail_send_preview_resolves_account_and_contact_aliases():
    contacts = ContactRegistry(
        {"teammate_alpha": ContactConfig("teammate_alpha", "teammate.alpha@example.com", "Teammate Alpha")}
    )
    tool = MailTool(contact_registry=contacts)

    preview = tool.send_preview("personal", ["work", "teammate_alpha"], "Hello", "Draft body")

    assert preview["preview"]["to"] == ["work@example.com", "teammate.alpha@example.com"]
    assert preview["recipient_aliases_resolved"] == ["work", "teammate_alpha"]


def test_mail_headers_decode_mime_words_before_returning_headers():
    backend = FakeMailBackend(
        messages={
            "personal": [
                {
                    "id": "p2",
                    "from": "=?utf-8?b?QWxleGV5?= <sender@example.org>",
                    "to": ["personal@example.com"],
                    "subject": "=?utf-8?b?0J/RgNC40LLQtdGC?=",
                    "date": "2026-01-05T10:00:00Z",
                    "text_body": "Public-safe body.",
                    "message_id": "<p2@example.org>",
                }
            ]
        }
    )
    tool = MailTool(backend=backend)

    listed = tool.list("personal")

    assert listed["messages"][0]["from"] == "Alexey <sender@example.org>"
    assert listed["messages"][0]["subject"] == "Привет"


def test_mail_send_preview_accepts_attachment_metadata_without_binary_inline():
    import base64

    tool = MailTool()

    preview = tool.send_preview(
        "personal",
        ["reader@example.org"],
        "Attachment preview",
        "Draft body",
        attachments=[
            {
                "filename": "report.pdf",
                "content_type": "application/pdf",
                "content_base64": base64.b64encode(b"fake-pdf-bytes").decode("ascii"),
            }
        ],
    )

    assert preview["requires_confirmation"] is True
    assert preview["preview"]["attachments"] == [
        {"filename": "report.pdf", "content_type": "application/pdf", "size": 14}
    ]
    assert "fake-pdf-bytes" not in repr(preview)
    assert "ZmFrZS1wZGYtYnl0ZXM" not in repr(preview)


def test_mail_send_confirm_sends_previewed_attachments_once():
    import base64

    tool = MailTool()

    preview = tool.send_preview(
        "personal",
        ["reader@example.org"],
        "Attachment send",
        "Draft body",
        attachments=[
            {
                "filename": "report.pdf",
                "content_type": "application/pdf",
                "content_base64": base64.b64encode(b"fake-pdf-bytes").decode("ascii"),
            }
        ],
    )
    result = tool.send_confirm(preview["confirmation_id"])

    assert result == {
        "status": "sent",
        "saved_to_sent": True,
        "sent_count": 1,
        "attachments": [{"filename": "report.pdf", "content_type": "application/pdf", "size": 14}],
    }
    assert tool.backend.sent[0]["attachments"][0]["content_bytes"] == b"fake-pdf-bytes"
    try:
        tool.send_confirm(preview["confirmation_id"])
    except KeyError as exc:
        assert "Unknown or already used" in str(exc)
    else:
        raise AssertionError("confirmation_id was reused")


def test_mail_send_preview_rejects_invalid_attachment_base64():
    tool = MailTool()

    try:
        tool.send_preview(
            "personal",
            ["reader@example.org"],
            "Bad attachment",
            "Draft body",
            attachments=[{"filename": "bad.txt", "content_base64": "not base64!!!"}],
        )
    except ValueError as exc:
        assert "base64" in str(exc)
    else:
        raise AssertionError("invalid base64 accepted")
    assert tool.backend.sent == []


def test_mail_send_preview_sanitizes_attachment_filename():
    import base64

    tool = MailTool()

    preview = tool.send_preview(
        "personal",
        ["reader@example.org"],
        "Safe filename",
        "Draft body",
        attachments=[
            {
                "filename": "../private/report.pdf",
                "content_base64": base64.b64encode(b"fake-pdf-bytes").decode("ascii"),
            }
        ],
    )

    assert preview["preview"]["attachments"] == [
        {"filename": "report.pdf", "content_type": "application/pdf", "size": 14}
    ]
    assert "private" not in repr(preview)



def test_mail_send_preview_rejects_invalid_attachment_content_type():
    import base64

    tool = MailTool()

    try:
        tool.send_preview(
            "personal",
            ["reader@example.org"],
            "Bad content type",
            "Draft body",
            attachments=[
                {
                    "filename": "report.pdf",
                    "content_type": "application/pdf\r\nX-Bad: 1",
                    "content_base64": base64.b64encode(b"fake-pdf-bytes").decode("ascii"),
                }
            ],
        )
    except ValueError as exc:
        assert "content_type" in str(exc)
    else:
        raise AssertionError("invalid content_type accepted")
    assert tool.backend.sent == []


def test_mail_send_preview_rejects_total_attachment_size(monkeypatch):
    import base64

    tool = MailTool()
    monkeypatch.setattr(MailTool, "MAX_ATTACHMENT_BYTES", 10)
    monkeypatch.setattr(MailTool, "MAX_TOTAL_ATTACHMENT_BYTES", 10)

    try:
        tool.send_preview(
            "personal",
            ["reader@example.org"],
            "Too much total",
            "Draft body",
            attachments=[
                {"filename": "one.txt", "content_base64": base64.b64encode(b"123456").decode("ascii")},
                {"filename": "two.txt", "content_base64": base64.b64encode(b"123456").decode("ascii")},
            ],
        )
    except ValueError as exc:
        assert "total" in str(exc)
    else:
        raise AssertionError("oversize attachment total accepted")
    assert tool.backend.sent == []


def test_mail_send_preview_rejects_oversize_attachment(monkeypatch):
    import base64

    tool = MailTool()
    monkeypatch.setattr(MailTool, "MAX_ATTACHMENT_BYTES", 4)

    try:
        tool.send_preview(
            "personal",
            ["reader@example.org"],
            "Big attachment",
            "Draft body",
            attachments=[
                {
                    "filename": "big.txt",
                    "content_type": "text/plain",
                    "content_base64": base64.b64encode(b"12345").decode("ascii"),
                }
            ],
        )
    except ValueError as exc:
        assert "too large" in str(exc)
    else:
        raise AssertionError("oversize attachment accepted")
    assert tool.backend.sent == []
