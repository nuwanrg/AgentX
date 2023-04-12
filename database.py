#database.py
import psycopg2
import json
import os
from psycopg2 import pool
from utils import find_key_value
from datetime import datetime


db_pool = pool.SimpleConnectionPool(minconn=1, maxconn=10,
                                    database=os.getenv("DB_NAME"),
                                    user=os.getenv("DB_USER"),
                                    password=os.getenv("DB_PASSWORD"),
                                    host=os.getenv("DB_HOST"),
                                    port=os.getenv("DB_PORT"))

def drop_tables():
    # Drop the table if it exists
    drop_table_query = "DROP TABLE IF EXISTS media_files;"
    conn = db_pool.getconn()
    try:
        cursor = conn.cursor()
        try:

            #media_files
            cursor.execute(drop_table_query)
            conn.commit()
        
        except psycopg2.Error as e:
            print(f"Error droping tables : {e}")

        finally:
            cursor.close()
    finally:
        db_pool.putconn(conn)


def create_tables():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS whatsapp_messages (
        id SERIAL PRIMARY KEY,
        message JSONB NOT NULL
    );
    """

    #IF NOT EXISTS
    create_media_file_table = """
    CREATE TABLE media_files ( 
        id SERIAL PRIMARY KEY,
        media_id VARCHAR(255) NOT NULL,
        caption VARCHAR(1000) NULL,
        file_url VARCHAR(1000) NOT NULL,
        file_type VARCHAR(50) NOT NULL,
        created_at TIMESTAMPTZ NOT NULL
    );
    """

    conn = db_pool.getconn()
    try:
        cursor = conn.cursor()
        try:
            cursor.execute(create_table_query)
            conn.commit()

            cursor.execute(create_media_file_table)
            conn.commit()
        
        except psycopg2.Error as e:
            print(f"Error creating tables : {e}")

        finally:
            cursor.close()
    finally:
        db_pool.putconn(conn)


 
     

def save_message_data(json_data):
    # messages = find_key_value(json_data, "messages")
    # from = find_key_value(messages, "from")
    conn = db_pool.getconn()
    try:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO whatsapp_messages (message) VALUES (%s);", (json.dumps(json_data),))
            conn.commit()
        
        except psycopg2.Error as e:
            print(f"Error saving data: {e}")

        finally:
            cursor.close()
    finally:
        db_pool.putconn(conn)


def save_media_metadata(media_id, caption, file_url, file_type ):
    query = '''
        INSERT INTO media_files (media_id, caption, file_url, file_type, created_at)
        VALUES (%s, %s, %s, %s, %s)
    '''
    conn = db_pool.getconn()
    try:
        cursor = conn.cursor()
        try:
            cursor.execute(query, (media_id, caption, file_url, file_type, datetime.now()) )
            conn.commit()
            print('Saved successfully to media_files table')
        
        except psycopg2.Error as e:
            print(f"Error saving data: {e}")

        finally:
            cursor.close()
    finally:
        db_pool.putconn(conn)



def search_message_data(sender):
    conn = db_pool.getconn()
    try:
        cursor = conn.cursor()
        try:
            cursor.execute(
            """
            SELECT
                id,
                message
            FROM whatsapp_messages
            WHERE message->'entry'->0->'changes'->0->'value'->'messages'->0->>'from' = %s;
            """,
            (sender,))
            results = cursor.fetchall()
            return results
        
        except psycopg2.Error as e:
            print(f"Error searching JSON data: {e}")
            return []

        finally:
            cursor.close()
    finally:
        db_pool.putconn(conn)


# Example usage
# print('__name__', __name__)
# if __name__ == "database":
#     # Search JSON data
#     sender = "6591312590"
#     results = search_message_data( sender)
#     print(len(results), " results found")
#     for row in results:
#         print(row)

