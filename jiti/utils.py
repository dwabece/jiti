
import datetime


from jiti import settings


def make_comment(time_spent):
    now_date = datetime.datetime.now().strftime('%A, %d %B %Y at %H:%M')
    return f'Time _({time_spent})_ added with *jiti* client on {now_date}'


def make_date(date_str):
    date_chopped = [int(date_part) for date_part in date_str.split('-')]
    return date(*date_chopped)


def date_from_jira_string(worklog_date):
    """
    Creates date object from jira-formatted string

    """
    date_str = worklog_date[:10]
    return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()


def print_worklog_entry(date, time):
    date_obj = date_from_jira_string(date)
    time_obj = datetime.timedelta(seconds=time)

    msg = f'{date_obj} ({date_obj.strftime("%a")}) '
    if date_obj.isoweekday() > 5:
        print(msg + '😎')
        return

    treshold = int(settings.conf['configuration']['worklog_threshold'])

    msg += f'{str(time_obj)[:-3]} logged'
    if time < treshold:
        time_left = str(datetime.timedelta(seconds=treshold - time))[:-3]
        msg += f', {time_left} to go'
    else:
        msg += ' 👌🏼'

    print(msg)
