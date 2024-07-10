import psycopg2
from psycopg2 import sql

class DatabaseHandler:
    def __init__(self, conn_params):
        self.conn_params = conn_params

    def execute_query(self, query, params=None):
        """Execute a query with optional parameters."""
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                conn.commit()
                return cur.fetchall()

    def get_model(self, model_uuid):
        query = sql.SQL("SELECT * FROM models WHERE uuid = %s;")
        self.execute_query(query, (model_uuid,))