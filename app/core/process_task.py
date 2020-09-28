import psycopg2

from config import PG_HOST, PG_USER, PG_PASSWORD, PG_PORT


async def process_task(database, task, task_logger, results):
    try:
        with psycopg2.connect(host=PG_HOST,
                              port=PG_PORT,
                              database=database[0],
                              user=PG_USER,
                              password=PG_PASSWORD) as conn:
            with conn.cursor() as cur:
                cur.execute(task)

                msg = f'Task on {database[0].upper()} database completed'

                results['success'] += 1
                task_logger.info(msg=f'INFO: {msg}')

    except Exception as e:
        try:
            error = e.pgerror.splitlines()
            msg = f'{error[0]}. Error code: {e.pgcode}.'
            results['error'].append(msg)
            task_logger.error(msg=f'ERROR: Task on {database[0].upper()} failed: {msg}, {error[1:]}')

        except Exception:
            results['error'].append(e)
            task_logger.error(msg=f'ERROR: Task on {database[0].upper()} failed: {e}')






