from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class PendingAction:
    """Одноразовый preview, который надо подтвердить перед write-действием."""

    action_type: str
    payload: dict[str, Any]
    expires_at: datetime
    explicit_work_confirm_required: bool = False


class ConfirmationStore:
    """In-memory confirmation store для reference implementation.

    В production это можно заменить SQLite/Redis, но принцип остаётся тем же:
    confirm отправляет ровно тот draft/event, который видел пользователь.
    """

    def __init__(self, ttl_seconds: int = 600) -> None:
        self.ttl_seconds = ttl_seconds
        self._actions: dict[str, PendingAction] = {}

    def create(
        self,
        action_type: str,
        payload: dict[str, Any],
        *,
        explicit_work_confirm_required: bool = False,
    ) -> str:
        confirmation_id = str(uuid4())
        self._actions[confirmation_id] = PendingAction(
            action_type=action_type,
            payload=payload,
            expires_at=datetime.now(timezone.utc) + timedelta(seconds=self.ttl_seconds),
            explicit_work_confirm_required=explicit_work_confirm_required,
        )
        return confirmation_id

    def pop(self, confirmation_id: str) -> PendingAction:
        action = self._actions.pop(confirmation_id, None)
        if action is None:
            raise KeyError("Unknown or already used confirmation_id")
        if action.expires_at < datetime.now(timezone.utc):
            raise KeyError("Expired confirmation_id")
        return action


def has_explicit_confirmation(text: str | None) -> bool:
    """Проверить явное подтверждение для опасных write-действий."""
    if not text:
        return False
    normalized = text.lower()
    return "confirm" in normalized or "подтверждаю" in normalized
