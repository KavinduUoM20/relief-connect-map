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
                    cls._instance._init_connection()
        return cls._instance

    def _init_connection(self):
        db_host = os.getenv("DB_HOST")
        if not db_host:
            raise ValueError("DB_HOST environment variable is required")
        
        self.connection = psycopg2.connect(
            host=db_host,
            port=os.getenv("DB_PORT", "5432"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        self.connection.autocommit = True

    def get_cursor(self):
        return self.connection.cursor(cursor_factory=RealDictCursor)

    def execute_query(self, query, params=None):
        cur = self.get_cursor()
        cur.execute(query, params)
        try:
            return cur.fetchall()
        except psycopg2.ProgrammingError:
            # For INSERT/UPDATE/DELETE
            return None
