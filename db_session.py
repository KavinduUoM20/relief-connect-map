import os
import psycopg2
from psycopg2.extras import RealDictCursor
from threading import Lock


class PostgresSingleton:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(PostgresSingleton, cls).__new__(cls)
                    cls._instance.connection = None
        return cls._instance

    def _get_connection(self):
        if not self.connection:
            self.connection = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT", "5432"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD")
            )
            self.connection.autocommit = True
        return self.connection

    def get_cursor(self):
        return self._get_connection().cursor(cursor_factory=RealDictCursor)

    def execute_query(self, query, params=None):
        cur = self.get_cursor()
        cur.execute(query, params)
        try:
            return cur.fetchall()
        except psycopg2.ProgrammingError:
            return None
