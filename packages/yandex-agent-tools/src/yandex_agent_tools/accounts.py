from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class AccountConfig:
    """Один публично-безопасный профиль аккаунта без раскрытия секретов."""

    account_id: str
    mail_address: str
    mail_display_name: str
    mail_signature_text: str
    calendar_username: str
    calendar_name: str
    calendar_writes_require_explicit_confirm: bool

    def public_dict(self) -> dict[str, object]:
        """Вернуть только безопасные поля, которые можно показывать агенту."""
        return {
            "account_id": self.account_id,
            "mail_address": self.mail_address,
            "mail_display_name": self.mail_display_name,
            "calendar_username": self.calendar_username,
            "calendar_name": self.calendar_name,
            "calendar_writes_require_explicit_confirm": self.calendar_writes_require_explicit_confirm,
        }


def _env(name: str, default: str) -> str:
    return os.getenv(name, default)


def load_accounts_from_env() -> dict[str, AccountConfig]:
    """Загрузить work/personal аккаунты из env с безопасными placeholder defaults."""
    return {
        "work": AccountConfig(
            account_id="work",
            mail_address=_env("YAT_WORK_MAIL_ADDRESS", "work@example.com"),
            mail_display_name=_env("YAT_WORK_MAIL_DISPLAY_NAME", "Work Agent"),
            mail_signature_text=_env("YAT_WORK_MAIL_SIGNATURE_TEXT", "Regards,\nWork Agent").replace("\\n", "\n"),
            calendar_username=_env("YAT_WORK_CALENDAR_USERNAME", "work@example.com"),
            calendar_name=_env("YAT_WORK_CALENDAR_NAME", "Work Calendar"),
            calendar_writes_require_explicit_confirm=_env("YAT_WORK_CALENDAR_WRITES_REQUIRE_EXPLICIT_CONFIRM", "true").lower()
            in {"1", "true", "yes"},
        ),
        "personal": AccountConfig(
            account_id="personal",
            mail_address=_env("YAT_PERSONAL_MAIL_ADDRESS", "personal@example.com"),
            mail_display_name=_env("YAT_PERSONAL_MAIL_DISPLAY_NAME", "Personal Agent"),
            mail_signature_text=_env("YAT_PERSONAL_MAIL_SIGNATURE_TEXT", "Regards,\nPersonal Agent").replace("\\n", "\n"),
            calendar_username=_env("YAT_PERSONAL_CALENDAR_USERNAME", "personal@example.com"),
            calendar_name=_env("YAT_PERSONAL_CALENDAR_NAME", "Personal Calendar"),
            calendar_writes_require_explicit_confirm=_env(
                "YAT_PERSONAL_CALENDAR_WRITES_REQUIRE_EXPLICIT_CONFIRM", "false"
            ).lower()
            in {"1", "true", "yes"},
        ),
    }


class AccountRegistry:
    """Registry скрывает детали конфигурации за короткими account_id."""

    def __init__(self, accounts: dict[str, AccountConfig] | None = None) -> None:
        self._accounts = accounts or load_accounts_from_env()

    def get(self, account_id: str) -> AccountConfig:
        try:
            return self._accounts[account_id]
        except KeyError as exc:
            raise KeyError(f"Unknown account_id: {account_id}") from exc

    def list_public(self) -> list[dict[str, object]]:
        return [account.public_dict() for account in self._accounts.values()]
