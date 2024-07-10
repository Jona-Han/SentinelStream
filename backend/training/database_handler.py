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
            
    def get_training_data(self, data_uid):
        query = sql.SQL("SELECT * FROM training_data WHERE uid = %s;")
        return self.execute_query(query, (data_uid,))

    def get_training_params(self, params_uid):
        query = sql.SQL("SELECT * FROM training_params WHERE uid = %s;")
        return self.execute_query(query, (params_uid,))

    def store_model(self, model_binary, model_name):
        query = sql.SQL("INSERT INTO models (name, model_data) VALUES (%s, %s);")
        self.execute_query(query, (model_name, psycopg2.Binary(model_binary)))
