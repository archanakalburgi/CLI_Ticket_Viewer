import api
import pytest
import responses
from requests.exceptions import HTTPError
import json


def test_invalid_uri():
    pytest.raises(Exception, api.get_current_page_num, "invalid uri")


@responses.activate
def test_404_should_not_kill_2():
    responses.add(
        responses.GET, "https://zccarchanazendeskcom.zendesk.com/", status=500
    )
    pytest.raises(
        HTTPError,
        api.call_zendesk_api,
        "https://zccarchanazendeskcom.zendesk.com/",
    )


@responses.activate
def test_should_parse_valid_json():
    mock_uri = "https://zccarchanazendeskcom.zendesk.com/"
    f = open("test/test_data/test.json", "r")
    responses.add(
        responses.GET,
        mock_uri,
        status=200,
        json=json.load(f),
        content_type="application/json",
    )
    resp = api.get_tickets(mock_uri)
    len(resp) == 10


@responses.activate
def test_invalid_json_should_not_kill_app():
    mock_uri = "https://zccarchanazendeskcom.zendesk.com/"
    f = open("test/test_data/test_invalid.json", "r")
    responses.add(
        responses.GET,
        mock_uri,
        status=200,
        json=json.load(f),
        content_type="application/json",
    )
    pytest.raises(KeyError, api.get_tickets, mock_uri)



def test_ticket_details_display_with_id_failing():
    ticket = api.Ticket(
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
    mock_org_uri = "https://zccarchanazendeskcom.zendesk.com/api/v2/organizations/1.json"
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
    ticket = api.Ticket(
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
            ["ticket_type", ticket.ticket_type]
        ]

@responses.activate
def test_ticket_details_display_empty_priority_should_not_break():
    mock_org_uri = "https://zccarchanazendeskcom.zendesk.com/api/v2/organizations/1.json"
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
    ticket = api.Ticket(
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
            ["ticket_type", ticket.ticket_type]
        ]

@responses.activate
def test_ticket_details_display_empty_ticket_type_should_not_break():
    mock_org_uri = "https://zccarchanazendeskcom.zendesk.com/api/v2/organizations/1.json"
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
    ticket = api.Ticket(
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
            ["ticket_type", ""]
        ]