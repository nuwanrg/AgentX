import psycopg2
from psycopg2 import pool
from aiengine.config import Config


class ConnectionPool:
    _conn_pool = None

    @classmethod
    def get_instance(cls):
        cfg = Config()
        if cls._conn_pool is None:
            cls._conn_pool = psycopg2.pool.SimpleConnectionPool(minconn=1, maxconn=10,
                                                                database=cfg.db_name,
                                                                user=cfg.db_user,
                                                                password=cfg.db_password,
                                                                host=cfg.db_host,
                                                                port=cfg.db_port
                                                                )
        return cls._conn_pool

    def get_connection(self):
        return self.pool.getconn()
