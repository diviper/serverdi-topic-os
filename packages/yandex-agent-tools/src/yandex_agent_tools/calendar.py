from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4

from .accounts import AccountRegistry
from .safety import ConfirmationStore, has_explicit_confirmation


@dataclass
class FakeCalendarBackend:
    """Fake CalDAV-like backend for public tests."""

    events: dict[str, list[dict[str, object]]] = field(default_factory=dict)

    def list_events(self, account_id: str, start: str | None = None, end: str | None = None) -> list[dict[str, object]]:
        events = list(self.events.get(account_id, []))
        if not start and not end:
            return events
        start_dt = _parse_datetime(start) if start else None
        end_dt = _parse_datetime(end) if end else None
        return [event for event in events if _event_overlaps(event, start_dt=start_dt, end_dt=end_dt)]

    def create_event(self, account_id: str, event: dict[str, object]) -> dict[str, object]:
        event = dict(event)
        event.setdefault("uid", str(uuid4()))
        event.setdefault("created_at", datetime.now(timezone.utc).isoformat())
        self.events.setdefault(account_id, []).append(event)
        return {"status": "created", "account_id": account_id, "event": event}


def _parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    normalized = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def _event_overlaps(event: dict[str, object], *, start_dt: datetime | None, end_dt: datetime | None) -> bool:
    event_start = _parse_datetime(str(event.get("start", "")))
    event_end = _parse_datetime(str(event.get("end", ""))) or event_start
    if event_start is None:
        return True
    if start_dt and event_end and event_end < start_dt:
        return False
    if end_dt and event_start > end_dt:
        return False
    return True


def default_fake_calendar_backend() -> FakeCalendarBackend:
    return FakeCalendarBackend(
        events={
            "work": [
                {
                    "uid": "work-demo-1",
                    "summary": "Public-safe work demo",
                    "start": "2026-01-02T10:00:00Z",
                    "end": "2026-01-02T10:30:00Z",
                    "calendar_name": "Work Calendar",
                }
            ],
            "personal": [
                {
                    "uid": "personal-demo-1",
                    "summary": "Public-safe personal demo",
                    "start": "2026-01-03T10:00:00Z",
                    "end": "2026-01-03T10:30:00Z",
                    "calendar_name": "Personal Calendar",
                }
            ],
        }
    )


class CalendarTool:
    """Calendar tools with explicit protection for work calendar writes."""

    def __init__(
        self,
        registry: AccountRegistry | None = None,
        backend: FakeCalendarBackend | None = None,
        confirmations: ConfirmationStore | None = None,
    ) -> None:
        self.registry = registry or AccountRegistry()
        self.backend = backend or default_fake_calendar_backend()
        self.confirmations = confirmations or ConfirmationStore()

    def list(self, account_id: str, start: str | None = None, end: str | None = None) -> dict[str, object]:
        account = self.registry.get(account_id)
        return {
            "account_id": account_id,
            "calendar_name": account.calendar_name,
            "events": self.backend.list_events(account_id, start=start, end=end),
        }

    def create_preview(
        self,
        account_id: str,
        summary: str,
        start: str,
        end: str,
        description: str = "",
        explicit_confirm_text: str | None = None,
    ) -> dict[str, object]:
        account = self.registry.get(account_id)
        work_confirm_required = account.calendar_writes_require_explicit_confirm and not has_explicit_confirmation(
            explicit_confirm_text
        )
        event = {
            "account_id": account_id,
            "calendar_name": account.calendar_name,
            "summary": summary,
            "description": description,
            "start": start,
            "end": end,
        }
        confirmation_id = self.confirmations.create(
            "calendar_create",
            event,
            explicit_work_confirm_required=work_confirm_required,
        )
        return {
            "requires_confirmation": True,
            "requires_explicit_work_calendar_confirmation": work_confirm_required,
            "confirmation_id": confirmation_id,
            "preview": event,
        }

    def create_confirm(self, confirmation_id: str, explicit_confirm_text: str | None = None) -> dict[str, object]:
        action = self.confirmations.pop(confirmation_id)
        if action.action_type != "calendar_create":
            raise ValueError("confirmation_id does not belong to calendar_create")
        if action.explicit_work_confirm_required and not has_explicit_confirmation(explicit_confirm_text):
            raise PermissionError("Work calendar writes require explicit owner confirmation")
        account_id = str(action.payload["account_id"])
        return self.backend.create_event(account_id, action.payload)
