import requests
from requests.auth import HTTPBasicAuth
from src.creds import EMAIL, TOKEN
from src.util import _json_dict_to_ticket, _ticket_json_to_tickets

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
    res = _json_dict_to_ticket(tt["ticket"])
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

