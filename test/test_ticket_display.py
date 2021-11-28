from src.ticket import Ticket
import responses
import json


def test_ticket_details_display_with_id_failing():
    ticket = Ticket(
        id=1,
        url="https://zccarchanazendeskcom.zendesk.com/api/v2/tickets/1.json",
        created_at="2019-01-01T00:00:00Z",
        ticket_type="incident",
        subject="test",
        status="open",
        priority="urgent",
        requester_id="30",
        assignee_id="15",
        organization_id="1",
        tags=["tag1", "tag2"],
        description="test",
    )
    assert ticket.ticket_detail_display()[0] == ["id", 1]


@responses.activate
def test_ticket_details_display_with_id():
    mock_org_uri = (
        "https://zccarchanazendeskcom.zendesk.com/api/v2/organizations/1.json"
    )
    mock_user_uri = "https://zccarchanazendeskcom.zendesk.com/api/v2/users/1.json"
    f = open("test/test_data/org.json", "r")
    responses.add(
        responses.GET,
        mock_org_uri,
        status=200,
        json=json.load(f),
        content_type="application/json",
    )
    f = open("test/test_data/user1.json", "r")
    responses.add(
        responses.GET,
        mock_user_uri,
        status=200,
        json=json.load(f),
        content_type="application/json",
    )
    ticket = Ticket(
        id=1,
        url="https://zccarchanazendeskcom.zendesk.com/api/v2/tickets/1.json",
        created_at="2019-01-01T00:00:00Z",
        ticket_type="incident",
        subject="test",
        status="open",
        priority="urgent",
        requester_id="1",
        assignee_id="1",
        organization_id="1",
        tags=["tag1", "tag2"],
        description="test",
    )
    assert ticket.ticket_detail_display() == [
        ["id", ticket.id],
        ["description", ticket.description],
        ["tags", ",".join(ticket.tags)],
        ["status", ticket.status],
        ["priority", ticket.priority],
        ["requester", "Test User"],
        ["assignee", "Test User"],
        ["organization_id", "Test Organization"],
        ["created_at", ticket.created_at],
        ["ticket_type", ticket.ticket_type],
    ]


@responses.activate
def test_ticket_details_display_empty_priority_should_not_break():
    mock_org_uri = (
        "https://zccarchanazendeskcom.zendesk.com/api/v2/organizations/1.json"
    )
    mock_user_uri = "https://zccarchanazendeskcom.zendesk.com/api/v2/users/1.json"
    f = open("test/test_data/org.json", "r")
    responses.add(
        responses.GET,
        mock_org_uri,
        status=200,
        json=json.load(f),
        content_type="application/json",
    )
    f = open("test/test_data/user1.json", "r")
    responses.add(
        responses.GET,
        mock_user_uri,
        status=200,
        json=json.load(f),
        content_type="application/json",
    )
    ticket = Ticket(
        id=1,
        url="https://zccarchanazendeskcom.zendesk.com/api/v2/tickets/1.json",
        created_at="2019-01-01T00:00:00Z",
        ticket_type="incident",
        subject="test",
        status="open",
        priority=None,
        requester_id="1",
        assignee_id="1",
        organization_id="1",
        tags=["tag1", "tag2"],
        description="test",
    )
    assert ticket.ticket_detail_display() == [
        ["id", ticket.id],
        ["description", ticket.description],
        ["tags", ",".join(ticket.tags)],
        ["status", ticket.status],
        ["priority", ""],
        ["requester", "Test User"],
        ["assignee", "Test User"],
        ["organization_id", "Test Organization"],
        ["created_at", ticket.created_at],
        ["ticket_type", ticket.ticket_type],
    ]


@responses.activate
def test_ticket_details_display_empty_ticket_type_should_not_break():
    mock_org_uri = (
        "https://zccarchanazendeskcom.zendesk.com/api/v2/organizations/1.json"
    )
    mock_user_uri = "https://zccarchanazendeskcom.zendesk.com/api/v2/users/1.json"
    f = open("test/test_data/org.json", "r")
    responses.add(
        responses.GET,
        mock_org_uri,
        status=200,
        json=json.load(f),
        content_type="application/json",
    )
    f = open("test/test_data/user1.json", "r")
    responses.add(
        responses.GET,
        mock_user_uri,
        status=200,
        json=json.load(f),
        content_type="application/json",
    )
    ticket = Ticket(
        id=1,
        url="https://zccarchanazendeskcom.zendesk.com/api/v2/tickets/1.json",
        created_at="2019-01-01T00:00:00Z",
        ticket_type=None,
        subject="test",
        status="open",
        priority="urgent",
        requester_id="1",
        assignee_id="1",
        organization_id="1",
        tags=["tag1", "tag2"],
        description="test",
    )
    assert ticket.ticket_detail_display() == [
        ["id", ticket.id],
        ["description", ticket.description],
        ["tags", ",".join(ticket.tags)],
        ["status", ticket.status],
        ["priority", ticket.priority],
        ["requester", "Test User"],
        ["assignee", "Test User"],
        ["organization_id", "Test Organization"],
        ["created_at", ticket.created_at],
        ["ticket_type", ""],
    ]
