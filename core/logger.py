import logging.config
import yaml


def config_logger():
    """
    Reads logger configuration from the yaml file
    """
    with open('logger_config.yaml', 'rt') as f:
        config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)


def get_logger(name):
    """
    Returns the logger object
    """
    return logging.getLogger(name)
