from yandex_agent_tools.fixtures import (
    fake_caldav_event_fixture,
    fake_failed_confirmation_fixture,
    fake_mail_with_attachment_metadata,
    fake_multipart_mail,
    fake_search_result_fixture,
)
from yandex_agent_tools.mail import MailTool


def test_fake_multipart_mail_read_returns_sanitized_text_and_attachment_metadata_only():
    message = fake_multipart_mail()
    tool = MailTool(backend=fake_mail_with_attachment_metadata([message]))

    read = tool.read("personal", "multipart-demo-1")
    listed = tool.list("personal", limit=1)

    assert read["message"]["text_body"] == "Plain text demo body for a public-safe fixture."
    assert read["message"]["html_body_present"] is True
    assert read["message"]["attachments"] == [
        {"filename": "demo-note.txt", "content_type": "text/plain", "size": 128}
    ]
    assert "binary" not in read["message"]
    assert "attachment_bytes" not in read["message"]
    assert "text_body" not in listed["messages"][0]


def test_fake_search_result_fixture_uses_snippet_not_full_body():
    result = fake_search_result_fixture()

    assert result["subject"] == "Public-safe search result"
    assert result["snippet"] == "Snippet only; full body is available only through read."
    assert "text_body" not in result


def test_fake_caldav_event_fixture_is_public_safe_and_caldav_like():
    event = fake_caldav_event_fixture()

    assert event["uid"] == "public-demo-event-1"
    assert event["calendar_name"] == "Work Calendar"
    assert event["href"].endswith("/public-demo-event-1.ics")
    assert "BEGIN:VCALENDAR" in event["ics"]
    assert "SUMMARY:Public-safe approval demo" in event["ics"]


def test_fake_failed_confirmation_fixture_documents_reuse_failure():
    failure = fake_failed_confirmation_fixture()

    assert failure["confirmation_id"] == "already-used-confirmation-id"
    assert failure["status"] == "rejected"
    assert failure["reason"] == "confirmation id was already used"
