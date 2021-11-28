from cmd import Cmd
import dataclasses
import api_call
from tabulate import tabulate


class MyCmd(Cmd):
    previous_page = None
    next_page = None

    prompt = "> "

    def do_ticket_detail(self, args):
        parsed_args = args.split(" ")
        if len(parsed_args) == 1:
            ticket_id = parsed_args[0]
            try:
                ticket = api_call.get_ticket_detail(ticket_id)
                print(tabulate(dataclasses.asdict(ticket).items(), tablefmt="plain"))
            except Exception as e:
                print(e)
                return None
            # print(ticket)
        else:
            print(
                "Invalid arguments, to see ticket details please provide a ticket like ticket_detail <id> eg: ticket_detail 1"
            )

    def do_tickets(self, args):
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
            (self.previous_page, tickets, self.next_page) = api_call.get_tickets(
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
        print(f"Showing page: {api_call.get_current_page_num(self.next_page)}")

if __name__ == "__main__":

    app = MyCmd()
    app.cmdloop("Enter a command to do something. eg `create name price`.")
