from jira import JIRA
from jira import exceptions as jira_exc

from . import jiexceptions, utils
from .settings import conf


def _init_jira():
    payload = {
        'server': conf['credentials']['host'],
        'basic_auth': (conf['credentials']['email'], conf['credentials']['token'])

    }
    return JIRA(**payload)


def add_time(ticket_number, time_spent, add_date=None):
    """
    Compose payload to log the time and fire a request to the API

    """
    jira = _init_jira()
    payload = {}

    if add_date:
        payload['started'] = utils.make_date(add_date)

    worklog_entry_comment = utils.make_comment(time_spent)
    if worklog_entry_comment:
        payload['comment'] = worklog_entry_comment

    try:
        issue = jira.issue(ticket_number)
    except jira_exc.JIRAError:
        raise jiexceptions.JITicketNotFoundException()

    try:
        jira.add_worklog(issue, time_spent, **payload)
    except jira_exc.JIRAError:
        raise jiexceptions.JIAPIError()
