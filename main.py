from cmd import Cmd
import dataclasses
import api
from tabulate import tabulate


class MyCmd(Cmd):
    previous_page = None
    next_page = None

    prompt = "> "

    def do_ticket_detail(self, args):
        """
        Get ticket details by id
        """
        parsed_args = args.split(" ")
        if len(parsed_args) == 1:
            ticket_id = parsed_args[0]
            try:
                ticket = api.get_ticket_detail(ticket_id)
                print(tabulate(dataclasses.asdict(ticket).items(), tablefmt="plain"))
            except Exception as e:
                print(e)
                print("Invalid arguments, to see ticket details please provide a ticket like ticket_detail <id> eg: ticket_detail 1")
                return None

    def do_tickets(self, args):
        """
        Get tickets 10 at a time
        """
        page_to_show = None
        parsed_args = args.split(" ")  # todo move this to diff function
        if (
            len(parsed_args) == 1
            and parsed_args[0] == "b"
            and self.previous_page is not None
        ):
            page_to_show = self.previous_page
        elif self.next_page is not None:
            page_to_show = self.next_page
        else:
            page_to_show = None

        try:
            (self.previous_page, tickets, self.next_page) = api.get_tickets(
                page_to_show
            )
            if len(tickets) == 0:
                print("No tickets found. Or something went wrong, todo")
            else:
                self._print_tickets_table(tickets)
        except Exception as e:
            print(e)
            return None

    def do_exit(self, args):
        """
        Exit the program.
        """
        raise SystemExit()

    def _print_tickets_table(self, tickets):
        fields = [
            "id",
            "subject",
            "status",
            "priority",
            "requester_id",
            "assignee_id",
            "organization_id",
            "tags",
            "created_at",
            "ticket_type",
        ]
        values = [list(d.display().values()) for d in tickets]
        print(tabulate(values, headers=fields, tablefmt="pretty"))
        try:
            (count, refreshed_at) = api.get_ticket_count()
            print(f"Showing page: {api.get_current_page_num(self.next_page)}.  10 Tickets/page. There are total of {count} tickets as of {refreshed_at}")
        except Exception as e:
            print(f"Failed to get meta data, this is not fatal. Will try again on next command")
            return None

welcome_string= """ Welcome to Zendesk CLI. 
Available commands:
-------------------------------------------------------
tickets -            to get tickets 10 at a time
ticket_detail <id> - to get ticket details by id
-------------------------------------------------------
Note: 
1. If user id and organization endpoint is not available, you will see an ID. We try to get that information on every tickets request
2. Application State is not persisted.
"""
if __name__ == "__main__":

    app = MyCmd()
    app.cmdloop(welcome_string)
