from yandex_agent_tools.accounts import AccountRegistry


def test_registry_lists_public_accounts_without_secrets():
    registry = AccountRegistry()

    accounts = registry.list_public()

    assert {account["account_id"] for account in accounts} == {"work", "personal"}
    assert all("password" not in key.lower() for account in accounts for key in account)
    assert registry.get("work").mail_address == "work@example.com"
    assert registry.get("personal").calendar_name == "Personal Calendar"
