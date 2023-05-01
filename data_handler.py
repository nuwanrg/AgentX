# data_handler.py
import psycopg2
import json
from psycopg2 import pool
import requests
from file.file_handler import upload_file_to_s3, generate_s3_url
from utils import find_key_value
from datetime import datetime
from aiengine.config import Config, check_openai_api_key
from whatsapp.whatsapp_client import download_file_from_whatsapp

cfg = Config()

db_pool = pool.SimpleConnectionPool(minconn=1, maxconn=10,
                                    database=cfg.db_name,
                                    user=cfg.db_user,
                                    password=cfg.db_password,
                                    host=cfg.db_host,
                                    port=cfg.db_port)

def setup_database():
    drop_tables()
    create_tables()

def drop_tables():
    # Drop the table if it exists
    drop_table_query = "DROP TABLE IF EXISTS media_files;"
    conn = db_pool.getconn()
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
        db_pool.putconn(conn)


def create_tables():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS whatsapp_messages (
        id SERIAL PRIMARY KEY,
        message JSONB NOT NULL
    );
    """

    # IF NOT EXISTS
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


def save_whatsapp_messages(data):

    type = find_key_value(data, "type")
    # print("type ", type)

    # if type == "user_initiated": #user_initiated messages are system generated, no need to save
    #     print("user_initiated")
    #     return '', 204
    # elif type == "text":
    #     response = save_whatsapp_text_messages(data)
    # elif type == "image" or type == "video":
    #     response = save_whatsapp_media_messages(data, type)


def save_whatsapp_text_messages(json_data):
    conn = db_pool.getconn()
    try:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO whatsapp_messages (message) VALUES (%s);", (json.dumps(json_data),))
            conn.commit()

        except psycopg2.Error as e:
            print(f"Error saving data: {e}")

        finally:
            cursor.close()
    finally:
        db_pool.putconn(conn)

def save_whatsapp_media_messages(data,type):
    phone_number = find_key_value(data, "from")
    media = find_key_value(data, type)
    media_id=find_key_value(media, "id")
    caption=find_key_value(media, "caption")
    file_type=find_key_value(media, "mime_type")


    media_endpoint = f"https://graph.facebook.com/v16.0/{media_id}?access_token={cfg.whatsapp_api_token}"
    response = requests.get(media_endpoint, stream=True)
    file_url= response.url


    print("phone_number ", phone_number)
    print("media ", media)
    print("media_id ", media_id)
    print("file_url ", file_url)
    print("file_type ", file_type)

    file_object = download_file_from_whatsapp(media_id)

    if file_object:    
        s3_object_name = media_id
        bucket_name = cfg.s3_bucket_dev
 
        print( "file_object ", file_object)            
        s3_url = upload_file_to_s3(file_object, bucket_name, s3_object_name)
        print("s3_url ", s3_url)

        #Save image metadata to DB
        file_url = 'none'
        generate_s3_url(bucket_name, s3_object_name)
        print("file_url ", file_url)
        save_media_metadata(media_id, caption, file_url, file_type )



def save_media_metadata(media_id, caption, file_url, file_type):
    query = '''
        INSERT INTO media_files (media_id, caption, file_url, file_type, created_at)
        VALUES (%s, %s, %s, %s, %s)
    '''
    conn = db_pool.getconn()
    try:
        cursor = conn.cursor()
        try:
            cursor.execute(query, (media_id, caption, file_url,
                        file_type, datetime.now()))
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
