from __future__ import annotations


def fake_multipart_mail() -> dict[str, object]:
    """Return a rich, obviously fake mail fixture.

    The fixture models common IMAP/SMTP edge cases without storing binary
    attachment bytes or private message content.
    """
    return {
        "id": "multipart-demo-1",
        "from": "sender@example.org",
        "to": ["personal@example.com"],
        "subject": "Public-safe multipart fixture",
        "date": "2026-01-05T09:00:00Z",
        "text_body": "Plain text demo body for a public-safe fixture.",
        "html_body_present": True,
        "message_id": "<multipart-demo-1@example.org>",
        "attachments": [
            {"filename": "demo-note.txt", "content_type": "text/plain", "size": 128},
        ],
        "raw_parts": [
            {"content_type": "text/plain", "disposition": "inline"},
            {"content_type": "text/html", "disposition": "inline"},
            {"content_type": "text/plain", "disposition": "attachment", "filename": "demo-note.txt"},
        ],
    }


def fake_search_result_fixture() -> dict[str, object]:
    """Return a search-result fixture that never exposes the full body."""
    return {
        "id": "search-demo-1",
        "from": "sender@example.org",
        "to": ["work@example.com"],
        "subject": "Public-safe search result",
        "date": "2026-01-05T10:00:00Z",
        "snippet": "Snippet only; full body is available only through read.",
        "message_id": "<search-demo-1@example.org>",
    }


def fake_mail_with_attachment_metadata(messages: list[dict[str, object]] | None = None):
    """Build a FakeMailBackend from rich fake fixtures."""
    from .mail import FakeMailBackend

    return FakeMailBackend(
        messages={
            "personal": messages or [fake_multipart_mail()],
            "work": [fake_search_result_fixture()],
        }
    )


def fake_caldav_event_fixture() -> dict[str, object]:
    """Return a CalDAV-like event fixture with public-safe ICS text."""
    ics = "\r\n".join(
        [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//ServerDi Topic OS//Public Safe Demo//EN",
            "BEGIN:VEVENT",
            "UID:public-demo-event-1",
            "DTSTART:20260106T090000Z",
            "DTEND:20260106T093000Z",
            "SUMMARY:Public-safe approval demo",
            "DESCRIPTION:Fake event used for documentation and tests only.",
            "END:VEVENT",
            "END:VCALENDAR",
            "",
        ]
    )
    return {
        "uid": "public-demo-event-1",
        "calendar_name": "Work Calendar",
        "summary": "Public-safe approval demo",
        "start": "2026-01-06T09:00:00Z",
        "end": "2026-01-06T09:30:00Z",
        "href": "/calendars/work/public-demo-event-1.ics",
        "etag": '"public-demo-event-1"',
        "ics": ics,
    }


def fake_failed_confirmation_fixture() -> dict[str, str]:
    """Document the expected shape for rejected repeated confirmations."""
    return {
        "confirmation_id": "already-used-confirmation-id",
        "status": "rejected",
        "reason": "confirmation id was already used",
    }
