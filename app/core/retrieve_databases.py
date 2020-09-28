import psycopg2

from config import PG_USER, PG_HOST, PG_PASSWORD, PG_PORT


def retrieve_databases():
    with psycopg2.connect(host=PG_HOST,
                          port=PG_PORT,
                          user=PG_USER,
                          password=PG_PASSWORD) as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT datname FROM pg_database;')
            databases = cur.fetchall()

    return databases
