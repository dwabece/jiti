#!/usr/bin/env python3
import fire
from jiti import ji
from jiti import utils
from jiti import jiexceptions


class JitiCLI():

    def log(self, ticket, time, date=None):
        """
        Logging N time on ticket for specific date

        """
        utils.ensure_env_file()

        msg = f'Registering {time} for {ticket}'
        msg += f' on date {date}' if date else ''
        msg += '...'
        print(msg)

        try:
            ji.add_time(
                ticket_number=ticket,
                time_spent=time,
                add_date=date
            )
        except jiexceptions.JIAPIError:
            raise SystemExit("Can't register worklog, something went wrong (On API side) 🚨")
        except jiexceptions.JITicketNotFoundException:
            raise SystemExit(f'Ticket {ticket} wasn\'t found in JIRA 🚨🤦🏻')
        except Exception as e:
            raise SystemExit(f'Oooops, something went wrong: {e}')

        print("You're all done! 🍻")


if __name__ == '__main__':
    fire.Fire(JitiCLI)
