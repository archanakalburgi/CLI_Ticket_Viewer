from urllib import parse
from src.ticket import Ticket

def get_current_page_num(uri):
    """
    return: int
    """
    try:
        parsed_uri = parse.parse_qs(parse.urlparse(uri).query)
        if parsed_uri["page"] is not None:
            return int(parsed_uri["page"][0]) - 1
    except:
        raise Exception("Invalid URI")

def _json_dict_to_ticket(ticket):
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
    tickets = [_json_dict_to_ticket(ticket) for ticket in json_tickets["tickets"]]
    return (json_tickets["previous_page"], tickets, json_tickets["next_page"])