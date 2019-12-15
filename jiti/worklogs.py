"""
Module for fetching information about logged hours

"""
import datetime

from jiti import ji
from jiti import utils
from jiti import settings

jira = ji._init_jira()
time_results = {}


def get_jira_username_for_current_user():
    # TODO take email from settings, it's in .jiti_settings
    return settings.conf['credentials']['email']


def format_worklog(worklog):
    time_spent = sum([x for x in zip(*worklog)][2])
    return str(datetime.timedelta(seconds=time_spent))


def get_last_tickets(days=30):
    """
    Fetches tickets user was working for in last N days

    """
    query = f'worklogAuthor = currentUser() AND worklogDate >= startOfDay(-{days}d)'
    return jira.search_issues(query)


def get_worklogs_for_current_user(ticket_number, n_days_before=None):
    """
    Get worklog entries for passed ticket nuber
    If `n_days_before` is empty, will fetch for current day only.

    :param string ticket_number: rly?
    :param None|int n_days_before: number of days in past to lookup for entries
    """
    developer_name = get_jira_username_for_current_user()
    results = jira._get_json(f'issue/{ticket_number}/worklog')
    today = datetime.date.today()

    for worklog_entry in results['worklogs']:
        if (worklog_entry['author']['emailAddress'] != developer_name):
            continue

        worklog_date = utils.date_from_jira_string(worklog_entry['started'])
        if n_days_before and worklog_date >= today - datetime.timedelta(days=n_days_before):
            yield worklog_entry

        if worklog_date == today:
            yield worklog_entry


class UserWorklog():
    def pushHours(self, day, hours):
        current_hours = getattr(self, day, 0)
        setattr(self, day, current_hours + hours)

    def prepopulate(self, days=None):
        today = datetime.datetime.today()
        dates = [(today - datetime.timedelta(days=i)).date() for i in range(days)]
        for date in dates:
            setattr(self, str(date), 0)


def get_worklog(days=None):
    """
    Fetches logged time

    """
    tickets_worked_on = get_last_tickets()
    worklog_obj = UserWorklog()
    if days:
        worklog_obj.prepopulate(days)

    for ticket in tickets_worked_on:
        for worklog_entry in get_worklogs_for_current_user(ticket.key, days):
            time_spent_seconds = worklog_entry['timeSpentSeconds']
            date_logged = worklog_entry['started'][:10]

            worklog_obj.pushHours(
                date_logged,
                time_spent_seconds
            )
    return worklog_obj
