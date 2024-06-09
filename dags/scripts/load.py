from airflow.hooks.postgres_hook import PostgresHook 
import logging

logger = logging.getLogger('airflow.task')

class SQLExecutor:
    def __init__(self, conn_id):
        self.conn_id = conn_id
        self.conn = None
        self.cur = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def connect(self):
        if 'postgress_local_connection' in self.conn_id:
            pg_hook = PostgresHook(postgres_conn_id=self.conn_id)
            self.conn = pg_hook.get_conn()
            self.cur = self.conn.cursor()
            logger.info(f'connect from DatabaseManager: Connected to PostgreSQL with conn_id: {self.conn_id}')
        else:
            raise ValueError("connect from DatabaseManager: Unsupported connection type")

    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        logger.info(f'close from DatabaseManager: Connection closed for conn_id: {self.conn_id}')

    def load_data_entries_to_db(self, query, entries):
        try:
            self.cur.execute(query, entries)
            self.conn.commit()
            logger.info('load_data_entries_to_db from DatabaseManager: All entries successfully loaded.')
        except Exception as e:
            logger.error(f'load_data_entries_to_db from DatabaseManager: The following error occurred when loading the entries: {e}. Rollback will be executed.')
            self.conn.rollback()
            raise e
    def query(self,query):
        try:
            self.cur.execute(query)
            logger.info(f'query from DatabaseManager: Query {query} successfully executed.')
        except Exception as e:
            logger.error(f'query from DatabaseManager: The followeing error ocurred while executing the query... {e}')