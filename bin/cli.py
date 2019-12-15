#!/usr/bin/env python3
import click
from jiti import ji
from jiti import utils
from jiti import jiexceptions
from jiti import worklogs
from datetime import timedelta


@click.group()
def jiticli():
    pass


@jiticli.command()
@click.option('--ticket', required=True, prompt='Ticket ID', help='Ticket you want to log time for')
@click.option('--time', prompt='Time', default='15m', help='Time you\'d like to log')
@click.option('--date', help="Date you'd like log time for")
def logtime(ticket, time, date=None):
    utils.ensure_env_file()

    msg = f'Registering {time} for {ticket}'
    msg += f' on date {date}' if date else ''
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


@jiticli.command()
@click.option('--days', help="Days back you'd like to check your worklog", type=int)
def worklog(days=None):
    worklog = worklogs.get_worklog(days).__dict__
    if not worklog:
        print('You havent logged anything for today')

    for (date, time) in worklog.items():
        utils.print_worklog_entry(date, time)


cli = click.CommandCollection(sources=[jiticli])

if __name__ == '__main__':
    cli()
