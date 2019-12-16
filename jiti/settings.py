import os
from pathlib import Path
import configparser


def get_config_path():
    home = str(Path.home())
    return os.path.join(home, '.jiti_settings')


def ensure_env_file():
    if not os.path.exists(get_config_path()):
        raise SystemExit('Config file not found')


conf = configparser.ConfigParser()
config_file = get_config_path()
conf.read(config_file)
