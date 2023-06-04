import psycopg2
from psycopg2 import pool
from connection_pool import ConnectionPool
from datetime import datetime
from user_dto import UserDTO


# class UserCRUD:
# def __init__():
#     # conn_pool = ConnectionPool.get_instance()

#     # IF NOT EXISTS
#     create_usres = """
#     CREATE TABLE users (
#         id SERIAL PRIMARY KEY,
#         phone_number VARCHAR(100) NULL,
#         whatsapp_id VARCHAR(100) NULL,
#         whatsapp_name VARCHAR(100) NULL,
#         first_name VARCHAR(100) NULL,
#         last_name VARCHAR(100) NULL,
#         date_of_birth VARCHAR(100) NULL,
#         email VARCHAR(100) NULL,
#         gender VARCHAR(100) NULL,
#         created_at TIMESTAMPTZ NOT NULL,
#         message_count INT NULL
#     );
#     """

# conn = connection_pool.getconn()
# try:
#     cursor = conn.cursor()
#     try:
#         cursor.execute(create_usres)
#         conn.commit()

#     except psycopg2.Error as e:
#         print(f"Error creating tables : {e}")

#     finally:
#         cursor.close()
# finally:
#     connection_pool.putconn(conn)


def create_user(user_dto):
    print("Creating user...", user_dto.email, user_dto.phone_number)
    conn_pool = ConnectionPool.get_instance()
    conn = conn_pool.getconn()
    cursor = conn.cursor()

    # Check if user with given email or phone number already exists
    query = "SELECT id FROM users WHERE email = %s OR phone_number = %s;"
    values = (user_dto.email, user_dto.phone_number)
    cursor.execute(query, values)
    existing_user = cursor.fetchone()
    if existing_user:
        print("User with the same email or phone number already exists.")
        cursor.close()
        conn_pool.putconn(conn)
        return

    # Create new user
    query = "INSERT INTO users (email, phone_number, created_at) VALUES (%s, %s, %s) RETURNING id;"
    values = (user_dto.email, user_dto.phone_number, datetime.now())
    cursor.execute(query, values)
    conn.commit()
    user_id = cursor.fetchone()[0]
    print(f"User created with ID: {user_id}")

    cursor.close()
    conn_pool.putconn(conn)


def get_user(self, user_id):
    conn_pool = ConnectionPool.get_instance()
    conn = conn_pool.getconn()
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE id = %s;"
    values = (user_id,)
    cursor.execute(query, values)
    user = cursor.fetchone()
    if user:
        print(
            f"User ID: {user[0]}, Email: {user[1]}, Phone Number: {user[2]}")
    else:
        print("User not found.")

    cursor.close()
    conn_pool.putconn(conn)


def get_user_by_phone(phone_number):
    conn_pool = ConnectionPool.get_instance()
    conn = conn_pool.getconn()
    cursor = conn.cursor()

    try:
        # query = "SELECT * FROM users WHERE phone_number = %s;"
        query = "SELECT phone_number, whatsapp_id, whatsapp_name, first_name, last_name, date_of_birth, email, gender, created_at,message_count FROM users WHERE phone_number = %s;"

        values = (phone_number,)
        cursor.execute(query, values)
        user = cursor.fetchone()
        if user:
            user_dto = UserDTO(phone_number=user[0], whatsapp_id=user[1], whatsapp_name=user[2], first_name=user[3],
                               last_name=user[4], date_of_birth=user[5], email=user[6], gender=user[7], created_at=user[8], message_count=user[9])
            print(user_dto)
            print(
                f"User ID: {user[0]}, Email: {user[1]}, Phone Number: {user[2]}")
            return user_dto
        else:
            print("User not found.")

    except (psycopg2.Error, Exception) as e:
        # Handle the error or log the exception as per your requirements
        print("An error occurred:", e)

    finally:
        cursor.close()
        conn_pool.putconn(conn)


def update_user(self, user_id, email, phone_number):
    conn_pool = ConnectionPool.get_instance()
    conn = conn_pool.getconn()
    cursor = conn.cursor()

    query = "UPDATE users SET email = %s, phone_number = %s WHERE id = %s;"
    values = (email, phone_number, user_id)
    cursor.execute(query, values)
    conn.commit()
    print(f"User with ID {user_id} updated successfully.")

    cursor.close()
    conn_pool.putconn(conn)


def update_user_message_count(phone_number, message_count):
    print("Updating user message count...", message_count)
    conn_pool = ConnectionPool.get_instance()
    conn = conn_pool.getconn()
    cursor = conn.cursor()

    query = "UPDATE users SET message_count = %s WHERE phone_number = %s;"
    values = (message_count, phone_number)
    cursor.execute(query, values)
    conn.commit()
    print(f"User with ID {phone_number} updated successfully.")

    cursor.close()
    conn_pool.putconn(conn)


def delete_user(self, user_id):
    conn_pool = ConnectionPool.get_instance()
    conn = conn_pool.getconn()
    cursor = conn.cursor()

    query = "DELETE FROM users WHERE id = %s;"
    values = (user_id,)
    cursor.execute(query, values)
    conn.commit()
    print(f"User with ID {user_id} deleted successfully.")

    cursor.close()
    conn_pool.putconn(conn)


# Usage example
# connection_pool = ConnectionPool.get_instance()

# crud = UserCRUD()

# Perform CRUD operations as before
# crud.create_user('john@example.com', '1234567890')
# crud.get_user(1)
# crud.update_user(1, 'john.doe@example.com', '9876543210')
# crud.delete_user(1)

# Close all connections in the connection pool
# connection_pool.close_all_connections()

# get_user_by_phone('6591312592')
