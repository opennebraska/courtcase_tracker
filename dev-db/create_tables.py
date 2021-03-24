import psycopg2
from sql_queries import create_schema_queries, create_table_queries, drop_table_queries, drop_schema_queries
import os

DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

def create_database():
    """
    - Creates and connects to the court_cases db
    - Returns the connection and cursor to court_cases db
    """

    # connect to postgresql
    print(f"Connecting to {DB_HOST}...")
    conn = psycopg2.connect(f"host={DB_HOST} user={DB_USER} password={DB_PASSWORD}")

    conn.set_session(autocommit=True)
    cur = conn.cursor()

    # create court_cases database with UTF8 encoding
    print(f"Dropping and Creating {DB_NAME}...")
    cur.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
    cur.execute(f"CREATE DATABASE {DB_NAME} WITH ENCODING 'utf8' TEMPLATE template0")

    # close connection to postgresql
    conn.close()

    # connect to court_cases database
    print(f"Connecting to {DB_NAME} on {DB_HOST}...")
    conn = psycopg2.connect(f"host={DB_HOST} dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD}")
    cur = conn.cursor()

    return cur, conn


def drop_schemas(cur, conn):
    """
    Drops each schema using the queries in `drop_schema_queries` list.
    """
    print("Creating Schemas...")
    for query in drop_schema_queries:
        cur.execute(query)
        conn.commit()


def drop_tables(cur, conn):
    """
    Drops each table using the queries in `drop_table_queries` list.
    """
    print("Dropping Tables...")
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_schemas(cur, conn):
    """
    Creates each schema using the queries in `create_schema_queries` list.
    """
    print("Creating Schemas...")
    for query in create_schema_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Creates each table using the queries in `create_table_queries` list.
    """
    print("Creating Tables...")
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    - Drops (if exists) and Creates the court_cases database.

    - Establishes connection with the court_cases database and gets
    cursor to it.

    - Drops all the tables.

    - Creates all tables needed.

    - Finally, closes the connection.
    """
    cur, conn = create_database()

    drop_tables(cur, conn)
    drop_schemas(cur, conn)
    create_schemas(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
