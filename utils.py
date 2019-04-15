import os
from datetime import date, datetime


def ensure_env_file():
    if not os.path.exists('.env'):
        raise SystemExit('File .env not found')


def make_comment(time_spent):
    now_date = datetime.now().strftime('%A, %d %B %Y at %H:%M')
    return f'Time _({time_spent})_ added with *jipy* client on {now_date}'


def make_date(date_str):
    date_chopped = [int(date_part) for date_part in date_str.split('-')]
    return date(*date_chopped)
