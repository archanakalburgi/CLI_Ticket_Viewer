import requests
from requests.auth import HTTPBasicAuth
from src.ticket import Ticket
from src.creds import EMAIL, TOKEN

USER_NAME =  EMAIL + "/token"
PASSWORD = TOKEN
DOMAIN = "https://zccarchanazendeskcom.zendesk.com/api/v2"


def call_zendesk_api(uri):
    """
    uri: string
    """
    response = requests.get(uri, auth=HTTPBasicAuth(USER_NAME, PASSWORD))
    response.raise_for_status()
    return response.json()


def get_ticket_count():
    """
    return: int
    """

    resp = call_zendesk_api(f"{DOMAIN}/tickets/count.json")["count"]
    return (resp["value"], resp["refreshed_at"])


def get_tickets(uri=None):
    """
    return: list of dicts
    """
    per_page = 10
    if uri is None:
        uri = f"{DOMAIN}/tickets.json?per_page={per_page}&page={1}"
    return _ticket_json_to_tickets(call_zendesk_api(uri))


def get_ticket_detail(ticket_id):
    """
    return: dict
    """
    uri = f"{DOMAIN}/tickets/{ticket_id}.json"
    tt = call_zendesk_api(uri)
    res = _ticket_to_json(tt["ticket"])
    return res


def get_user_by_id(user_id):
    """
    return: dict
    """
    uri = f"{DOMAIN}/users/{user_id}.json"
    return call_zendesk_api(uri)


def get_organization_by_id(org_id):
    """
    return: dict
    """
    uri = f"{DOMAIN}/organizations/{org_id}.json"
    return call_zendesk_api(uri)


def _ticket_to_json(ticket):
    """
    return: dict
    """
    return Ticket(
        id=ticket["id"],
        url=ticket["url"],
        created_at=ticket["created_at"],
        ticket_type=ticket["type"],
        subject=ticket["subject"],
        description=ticket["description"],
        priority=ticket["priority"],
        status=ticket["status"],
        assignee_id=ticket["assignee_id"],
        organization_id=ticket["organization_id"],
        tags=ticket["tags"],
        requester_id=ticket["requester_id"],
    )


def _ticket_json_to_tickets(json_tickets):
    """
    return: list of dicts
    """
    tickets = [_ticket_to_json(ticket) for ticket in json_tickets["tickets"]]
    return (json_tickets["previous_page"], tickets, json_tickets["next_page"])
