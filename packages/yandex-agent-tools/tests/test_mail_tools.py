from yandex_agent_tools.mail import MailTool


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
