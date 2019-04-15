import configparser
from .utils import get_config_path

conf = configparser.ConfigParser()
config_file = get_config_path()
conf.read(config_file)
