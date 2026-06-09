from yandex_agent_tools.accounts import AccountRegistry, ContactRegistry


def test_registry_lists_public_accounts_without_secrets():
    registry = AccountRegistry()

    accounts = registry.list_public()

    assert {account["account_id"] for account in accounts} == {"work", "personal"}
    assert all("password" not in key.lower() for account in accounts for key in account)
    assert registry.get("work").mail_address == "work@example.com"
    assert registry.get("personal").calendar_name == "Personal Calendar"


def test_contact_registry_lists_alias_metadata_without_emails(monkeypatch):
    monkeypatch.setenv("YAT_CONTACT_ALIASES", "teammate-alpha")
    monkeypatch.setenv("YAT_CONTACT_TEAMMATE_ALPHA_EMAIL", "teammate.alpha@example.com")
    monkeypatch.setenv("YAT_CONTACT_TEAMMATE_ALPHA_DISPLAY_NAME", "Teammate Alpha")

    registry = ContactRegistry()

    contacts = registry.list_public()
    assert contacts == [
        {"alias": "teammate_alpha", "display_name": "Teammate Alpha", "kind": "colleague", "has_email": True}
    ]
    assert "teammate.alpha@example.com" not in str(contacts)
    assert registry.get("teammate_alpha").email == "teammate.alpha@example.com"
