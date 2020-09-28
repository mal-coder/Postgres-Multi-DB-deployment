import asyncio
import json

from config import TASK_LIST
from app.core.log import logger
from app.core.process_task import process_task
from app.core.retrieve_databases import retrieve_databases
from app.core.send_email import send_email


async def main():
    with open(TASK_LIST) as json_file:
        task_list = json.load(json_file)

    databases, exclude = task_list.get('databases', None), task_list.get('exclude', list())
    if not databases:
        databases = retrieve_databases()

    print("Starting modifications.")
    for task_name, task in task_list['tasks'].items():
        results = {'success': 0,
                   'error': []}
        task_logger, log_name = logger(task_name)
        tasks = [process_task(database, task, task_logger, results) for database in databases if
                 database[0] not in exclude]

        await asyncio.gather(*tasks)

        send_email(task_name, task, log_name, results)

    print("Program completed.")


if __name__ == '__main__':
    asyncio.run(main())
