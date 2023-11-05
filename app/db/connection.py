import logging
from os import getenv
from contextlib import contextmanager
from psycopg2 import pool

DATABASE_VARS = {
    "dbname": getenv("POSTGRES_DB"),
    "user": getenv("POSTGRES_USER"),
    "password": getenv("POSTGRES_PASSWORD"),
    "host": getenv("POSTGRES_HOST"),
    "port": getenv("POSTGRES_PORT"),
}


class Database:
    _connection_pool = None

    @staticmethod
    def initialize():
        Database._connection_pool = pool.SimpleConnectionPool(
            minconn=1, maxconn=10, **DATABASE_VARS
        )
        logging.info("Initialized database connection pool.")

    @staticmethod
    def get_connection():
        return Database._connection_pool.getconn()

    @staticmethod
    def return_connection(connection):
        Database._connection_pool.putconn(connection)

    @staticmethod
    def close_all_connections():
        Database._connection_pool.closeall()


@contextmanager
def get_db_connection():
    connection = Database.get_connection()
    try:
        yield connection
    except Exception as e:
        connection.rollback()
        logging.error(f"Error in get_db_connection context manager: {e}")
        raise
    finally:
        Database.return_connection(connection)
