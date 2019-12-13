import os
from pathlib import Path
from datetime import date, datetime


def get_config_path():
    home = str(Path.home())
    return os.path.join(home, '.jiti_settings')


def ensure_env_file():
    if not os.path.exists(get_config_path()):
        raise SystemExit('Config file not found')


def make_comment(time_spent):
    now_date = datetime.now().strftime('%A, %d %B %Y at %H:%M')
    return f'Time _({time_spent})_ added with *jiti* client on {now_date}'


def make_date(date_str):
    date_chopped = [int(date_part) for date_part in date_str.split('-')]
    return date(*date_chopped)
