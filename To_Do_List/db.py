import os
import psycopg2
from contextlib import contextmanager

@contextmanager
def get_conn(host=None, port=None, dbname=None, user=None, password=None):
    # allow passing params (used in startup) or env defaults
    host = host or os.environ.get("POSTGRES_HOST", "db")
    port = port or int(os.environ.get("POSTGRES_PORT", 5432))
    dbname = dbname or os.environ.get("POSTGRES_DB", "todo_db")
    user = user or os.environ.get("POSTGRES_USER", "todo_user")
    password = password or os.environ.get("POSTGRES_PASSWORD", "todo_pass")
    conn = psycopg2.connect(host=host, port=port, dbname=dbname, user=user, password=password)
    try:
        yield conn
    finally:
        conn.close()

def dict_from_cursor_row(cursor):
    cols = [desc[0] for desc in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]