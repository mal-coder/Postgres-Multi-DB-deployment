from os import environ

PRODUCTION = True if (environ['PRODUCTION'] == "True") else False
TASK_LIST = environ['TASKS_PATH']
TOP_ERROR_COUNT = int(environ['TOP_ERROR_COUNT'])
PG_HOST = environ['PG_HOST']
PG_PORT = environ['PG_PORT']
PG_USER = environ['PG_USER']
PG_PASSWORD = environ['PG_PASSWORD']
SMTP_SERVER = environ['SMTP_SERVER']
SMTP_PORT = int(environ['SMTP_PORT'])
SENDER_EMAIL = environ['SENDER_EMAIL']
RECEIVER_EMAIL = environ['RECEIVER_EMAIL']
EMAIL_PASSWORD = environ['EMAIL_PASSWORD']
