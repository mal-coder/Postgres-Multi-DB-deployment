import psycopg2
from time import sleep
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import PG_USER, PG_HOST, PG_PASSWORD, PG_PORT, PRODUCTION


def set_up_dbs():
    if not PRODUCTION:
        sleep(5)
        print("Running in testing mode. Creating test DBs'.")
        with psycopg2.connect(host=PG_HOST,
                              port=PG_PORT,
                              user=PG_USER,
                              password=PG_PASSWORD) as conn:
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            with conn.cursor() as cur:
                for i in range(100):
                    cur.execute(f'CREATE DATABASE "test_db_{i}";')
    else:
        print("Running in production mode. Skipping creating test DBs'.")


if __name__ == '__main__':
    set_up_dbs()
