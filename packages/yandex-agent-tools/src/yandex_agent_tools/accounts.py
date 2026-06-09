from __future__ import annotations

import os
import re
from dataclasses import dataclass


_ALIAS_RE = re.compile(r"[^a-z0-9_]+")


def normalize_alias(value: str) -> str:
    """Normalize public-safe short aliases used by agents and fixtures."""

    normalized = _ALIAS_RE.sub("_", value.strip().lower().replace("-", "_").replace(" ", "_"))
    normalized = re.sub(r"_+", "_", normalized).strip("_")
    if not normalized:
        raise ValueError("Alias must not be empty")
    return normalized


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


@dataclass(frozen=True)
class ContactConfig:
    """Private recipient address stored behind a short alias.

    The public API exposes alias/display metadata only. The email is used for
    delivery previews/confirms but is intentionally omitted from list output.
    """

    alias: str
    email: str
    display_name: str
    kind: str = "colleague"

    def public_dict(self) -> dict[str, object]:
        return {
            "alias": self.alias,
            "display_name": self.display_name,
            "kind": self.kind,
            "has_email": bool(self.email),
        }


def _env(name: str, default: str) -> str:
    return os.getenv(name, default)


def _env_bool(name: str, default: str) -> bool:
    return _env(name, default).lower() in {"1", "true", "yes"}


def _contact_env_prefix(alias: str) -> str:
    return "YAT_CONTACT_" + alias.upper().replace("-", "_").replace(" ", "_")


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
            calendar_writes_require_explicit_confirm=_env_bool(
                "YAT_WORK_CALENDAR_WRITES_REQUIRE_EXPLICIT_CONFIRM", "true"
            ),
        ),
        "personal": AccountConfig(
            account_id="personal",
            mail_address=_env("YAT_PERSONAL_MAIL_ADDRESS", "personal@example.com"),
            mail_display_name=_env("YAT_PERSONAL_MAIL_DISPLAY_NAME", "Personal Agent"),
            mail_signature_text=_env("YAT_PERSONAL_MAIL_SIGNATURE_TEXT", "Regards,\nPersonal Agent").replace("\\n", "\n"),
            calendar_username=_env("YAT_PERSONAL_CALENDAR_USERNAME", "personal@example.com"),
            calendar_name=_env("YAT_PERSONAL_CALENDAR_NAME", "Personal Calendar"),
            calendar_writes_require_explicit_confirm=_env_bool(
                "YAT_PERSONAL_CALENDAR_WRITES_REQUIRE_EXPLICIT_CONFIRM", "false"
            ),
        ),
    }


def load_contacts_from_env() -> dict[str, ContactConfig]:
    """Load optional contact aliases from environment.

    Example:
        YAT_CONTACT_ALIASES=teammate_alpha
        YAT_CONTACT_TEAMMATE_ALPHA_EMAIL=teammate.alpha@example.com
        YAT_CONTACT_TEAMMATE_ALPHA_DISPLAY_NAME=Teammate Alpha
        YAT_CONTACT_TEAMMATE_ALPHA_KIND=colleague
    """

    aliases = [item.strip() for item in _env("YAT_CONTACT_ALIASES", "").split(",") if item.strip()]
    contacts: dict[str, ContactConfig] = {}
    for raw_alias in aliases:
        alias = normalize_alias(raw_alias)
        prefix = _contact_env_prefix(alias)
        email = _env(f"{prefix}_EMAIL", f"{alias}@example.com")
        contacts[alias] = ContactConfig(
            alias=alias,
            email=email,
            display_name=_env(f"{prefix}_DISPLAY_NAME", alias.replace("_", " ").title()),
            kind=_env(f"{prefix}_KIND", "colleague"),
        )
    return contacts


class AccountRegistry:
    """Registry скрывает детали конфигурации за короткими account_id."""

    def __init__(self, accounts: dict[str, AccountConfig] | None = None) -> None:
        self._accounts = accounts or load_accounts_from_env()

    def get(self, account_id: str) -> AccountConfig:
        try:
            return self._accounts[account_id]
        except KeyError as exc:
            raise KeyError(f"Unknown account_id: {account_id}") from exc

    def maybe_get(self, account_id: str) -> AccountConfig | None:
        return self._accounts.get(account_id)

    def list_public(self) -> list[dict[str, object]]:
        return [account.public_dict() for account in self._accounts.values()]


class ContactRegistry:
    """Registry for private contact aliases with redacted list output."""

    def __init__(self, contacts: dict[str, ContactConfig] | None = None) -> None:
        self._contacts = contacts or load_contacts_from_env()

    def get(self, alias: str) -> ContactConfig:
        normalized = normalize_alias(alias)
        try:
            return self._contacts[normalized]
        except KeyError as exc:
            raise KeyError(f"Unknown contact alias: {normalized}") from exc

    def maybe_get(self, alias: str) -> ContactConfig | None:
        return self._contacts.get(normalize_alias(alias))

    def list_public(self) -> list[dict[str, object]]:
        return [contact.public_dict() for contact in self._contacts.values()]
