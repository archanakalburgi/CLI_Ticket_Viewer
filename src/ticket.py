import logging
from dataclasses import dataclass
import src.api as api

USER_ID_MAP = {}
ORG_ID_MAP = {}

@dataclass
class Ticket:
    id: int
    url: str
    subject: str
    description: str
    status: str
    priority: str
    requester_id: int
    assignee_id: int
    organization_id: int
    tags: list
    created_at: str
    ticket_type: str

    def update_user_id_map(self, user_id):
        try:
            USER_ID_MAP[self.requester_id] = api.get_user_by_id(user_id)["user"]["name"]
        except Exception as e:
            logging.error(f"Failed to get user info for {self.requester_id}, {e}")
            pass

    def updated_org_id_map(self, org_id):
        try:
            ORG_ID_MAP[self.organization_id] = api.get_organization_by_id(org_id)[
                "organization"
            ]["name"]
        except Exception as e:
            logging.error(
                f"Failed to get organization info for {self.organization_id}, {e}"
            )
            pass

    def __post_init__(self):
        if self.requester_id not in USER_ID_MAP:
            if self.requester_id is not None:
                self.update_user_id_map(self.requester_id)
            if self.organization_id is not None:
                self.updated_org_id_map(self.organization_id)

    def display(self):
        return {
            "id": self.id,
            "subject": self.subject,
            # "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "requester": USER_ID_MAP.get(self.requester_id, self.requester_id),
            "assignee": USER_ID_MAP.get(self.assignee_id, self.assignee_id),
            "organization_id": ORG_ID_MAP.get(
                self.organization_id, self.organization_id
            ),
            "tags": self.tags,
            "created_at": self.created_at,
            "ticket_type": self.ticket_type,
        }

    def __empty_string_if_none(self, val):
        if val is None:
            return ""
        return val

    def ticket_detail_display(self):
        return [
            ["id", self.id],
            ["description", self.description],
            ["tags", ",".join(self.tags)],
            ["status", self.status],
            ["priority", self.__empty_string_if_none(self.priority)],
            ["requester", USER_ID_MAP.get(self.requester_id, self.requester_id)],
            ["assignee", USER_ID_MAP.get(self.assignee_id, self.assignee_id)],
            ["organization_id", ORG_ID_MAP.get(self.organization_id, self.organization_id)],
            ["created_at", self.created_at],
            ["ticket_type", self.__empty_string_if_none(self.ticket_type)]
        ]