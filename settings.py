import configparser

conf = configparser.ConfigParser()
config_file = r'.env'
conf.read(config_file)
