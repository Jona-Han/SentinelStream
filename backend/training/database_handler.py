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
            
    def get_training_data(self, data_uuid):
        """Returns training data from db."""
        query = sql.SQL("SELECT * FROM training_data WHERE uuid = %s;")
        return self.execute_query(query, (data_uuid,))

    def get_training_params(self, params_uuid):
        """Returns training params from db."""
        query = sql.SQL("SELECT * FROM training_params WHERE uuid = %s;")
        return self.execute_query(query, (params_uuid,))

    def store_model(self, model_binary, model_name):
        """Binarizes and stores model in db."""
        query = sql.SQL("INSERT INTO models (name, model_data) VALUES (%s, %s);")
        self.execute_query(query, (model_name, psycopg2.Binary(model_binary)))
