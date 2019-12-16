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
    """
    Fetches jira username from config

    """
    return settings.conf['credentials']['email']


def get_last_tickets(days=30):
    """
    Fetches tickets user interacted with in last N days

    :return: jira's ResultList object containing list of mentioned tickets
    :rtype: Object
    """
    query = f'worklogAuthor = currentUser() AND worklogDate >= startOfDay(-{days}d)'
    return jira.search_issues(query)


def get_worklogs_for_current_user(ticket_number, n_days_before=None):
    """
    Get worklog entries for specified ticket by it's nuber
    If `n_days_before` is empty, will fetch for current day only.

    :param string ticket_number: rly?
    :param None|int n_days_before: number of days in past to lookup for entries
    """
    current_user = get_jira_username_for_current_user()
    results = jira._get_json(f'issue/{ticket_number}/worklog')
    today = datetime.date.today()

    for worklog_entry in results['worklogs']:
        if (worklog_entry['author']['emailAddress'] != current_user):
            continue

        worklog_date = utils.date_from_jira_string(worklog_entry['started'])
        if n_days_before and worklog_date >= today - datetime.timedelta(days=n_days_before):
            yield worklog_entry

        if worklog_date == today:
            yield worklog_entry


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


class UserWorklog():
    def pushHours(self, day, hours):
        current_hours = getattr(self, day, 0)
        setattr(self, day, current_hours + hours)

    def prepopulate(self, days=None):
        today = datetime.datetime.today()
        dates = [(today - datetime.timedelta(days=i)).date() for i in range(days)]
        for date in dates:
            setattr(self, str(date), 0)
