import logging
from logging import handlers
from datetime import datetime


def logger(task_name):
    log_name = f'{task_name} {datetime.now()}.log'
    log = logging.getLogger(task_name)
    log.setLevel(logging.INFO)
    handler = logging.handlers.RotatingFileHandler(log_name)
    log.addHandler(handler)

    return log, log_name
