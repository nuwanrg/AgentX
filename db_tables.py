
from connection_pool import ConnectionPool
import psycopg2


def create_db_tables():
    # drop_tables()
    create_tables()


def drop_tables():
    # Drop the table if it exists
    drop_table_query = "DROP TABLE IF EXISTS media_files;"

    conn_pool = ConnectionPool.get_instance()
    conn = conn_pool.getconn()
    try:
        cursor = conn.cursor()
        try:

            # media_files
            cursor.execute(drop_table_query)
            conn.commit()

        except psycopg2.Error as e:
            print(f"Error droping tables : {e}")

        finally:
            cursor.close()
    finally:
        conn_pool.putconn(conn)


def create_tables():
    print("Creating tables...")
    create_table_query = """
    CREATE TABLE IF NOT EXISTS whatsapp_messages (
        id SERIAL PRIMARY KEY,
        message JSONB NOT NULL
    );
    """

    # IF NOT EXISTS
    create_media_file_table = """
    CREATE TABLE  IF NOT EXISTS media_files ( 
        id SERIAL PRIMARY KEY,
        media_id VARCHAR(255) NOT NULL,
        caption VARCHAR(1000) NULL,
        file_url VARCHAR(1000) NOT NULL,
        file_type VARCHAR(50) NOT NULL,
        created_at TIMESTAMPTZ NOT NULL
    );
    """

    # IF NOT EXISTS
    create_usres = """
    CREATE TABLE IF NOT EXISTS users ( 
        id SERIAL PRIMARY KEY,
        phone_number VARCHAR(100) NULL,
        whatsapp_id VARCHAR(100) NULL,
        whatsapp_name VARCHAR(100) NULL,
        first_name VARCHAR(100) NULL,
        last_name VARCHAR(100) NULL,
        date_of_birth VARCHAR(100) NULL,
        email VARCHAR(100) NULL,
        gender VARCHAR(100) NULL,
        created_at TIMESTAMPTZ NOT NULL,
        message_count INT NULL
    );
    """
    conn_pool = ConnectionPool.get_instance()
    conn = conn_pool.getconn()
    # cursor = conn.cursor()
    # conn = db_pool.getconn()

    try:
        cursor = conn.cursor()
        try:
            cursor.execute(create_table_query)
            conn.commit()

            cursor.execute(create_media_file_table)
            conn.commit()

            cursor.execute(create_usres)
            conn.commit()

        except psycopg2.Error as e:
            print(f"Error creating tables : {e}")

        finally:
            cursor.close()
    finally:
        conn_pool.putconn(conn)
