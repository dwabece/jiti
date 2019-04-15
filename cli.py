#!/usr/bin/env python3
import click
import ji
import jiexceptions
import utils


@click.command()
@click.option('--ticket', required=True, prompt='Ticket ID', help='Ticket you want to log time for')
@click.option('--time', prompt='Time', default='15m', help='Time you\'d like to log')
@click.option('--date', help="Date you'd like log time for")
def logtime(ticket, time, date=None):
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
        print("Can't register worklog, something went wrong (On API side) 🚨")
    except jiexceptions.JITicketNotFoundException:
        print(f'Ticket {ticket} wasn\'t found in JIRA 🚨🤦🏻')
    except Exception as e:
        raise SystemExit(f'Oooops, something went wrong: {e}')

    print("You're all done! 🍻")


if __name__ == '__main__':
    logtime()
