import logging
import configparser

class objectview(object):
    def __init__(self, d):
        self.__dict__ = d

def setup_logging():
    """ Basic logging setup """
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    return logging
    
def get_config(config_file):
    """ Read configuration file, and returns a configparser object """
    conf = configparser.ConfigParser()
    conf.read(config_file)
    return conf