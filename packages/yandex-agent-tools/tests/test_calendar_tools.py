from yandex_agent_tools.accounts import ContactConfig, ContactRegistry
from yandex_agent_tools.calendar import CalendarTool


def test_calendar_list_uses_fake_backend():
    tool = CalendarTool()

    result = tool.list("personal")

    assert result["calendar_name"] == "Personal Calendar"
    assert result["events"][0]["summary"] == "Public-safe personal demo"


def test_calendar_list_filters_by_requested_time_range():
    tool = CalendarTool()

    inside = tool.list("personal", start="2026-01-03T00:00:00Z", end="2026-01-03T23:59:59Z")
    outside = tool.list("personal", start="2026-02-01T00:00:00Z", end="2026-02-02T00:00:00Z")

    assert [event["uid"] for event in inside["events"]] == ["personal-demo-1"]
    assert outside["events"] == []


def test_personal_calendar_create_preview_and_confirm():
    tool = CalendarTool()

    preview = tool.create_preview(
        "personal",
        "Demo event",
        "2026-01-04T10:00:00Z",
        "2026-01-04T10:30:00Z",
        "Fake public-safe event",
    )
    result = tool.create_confirm(preview["confirmation_id"])

    assert preview["requires_confirmation"] is True
    assert preview["requires_explicit_work_calendar_confirmation"] is False
    assert result["status"] == "created"
    assert result["event"]["calendar_name"] == "Personal Calendar"


def test_calendar_create_preview_resolves_contact_alias_attendees():
    contacts = ContactRegistry(
        {
            "teammate_alpha": ContactConfig(
                alias="teammate_alpha",
                email="teammate.alpha@example.com",
                display_name="Teammate Alpha",
                kind="colleague",
            )
        }
    )
    tool = CalendarTool(contact_registry=contacts)

    preview = tool.create_preview(
        "personal",
        "Demo with attendee",
        "2026-01-04T10:00:00Z",
        "2026-01-04T10:30:00Z",
        attendees=["teammate-alpha", "direct@example.org"],
    )

    assert preview["attendee_aliases_resolved"] == ["teammate_alpha"]
    assert preview["preview"]["attendees"] == ["teammate.alpha@example.com", "direct@example.org"]


def test_work_calendar_create_requires_explicit_confirm_on_confirm_step():
    tool = CalendarTool()

    preview = tool.create_preview(
        "work",
        "Work event",
        "2026-01-04T10:00:00Z",
        "2026-01-04T10:30:00Z",
    )

    assert preview["requires_explicit_work_calendar_confirmation"] is True
    try:
        tool.create_confirm(preview["confirmation_id"])
    except PermissionError as exc:
        assert "explicit owner confirmation" in str(exc)
    else:
        raise AssertionError("work calendar write was allowed without explicit confirmation")


def test_work_calendar_create_allows_explicit_confirm_text():
    tool = CalendarTool()

    preview = tool.create_preview(
        "work",
        "Work event",
        "2026-01-04T10:00:00Z",
        "2026-01-04T10:30:00Z",
        explicit_confirm_text="confirm work calendar write",
    )
    result = tool.create_confirm(preview["confirmation_id"])

    assert preview["requires_explicit_work_calendar_confirmation"] is False
    assert result["status"] == "created"
