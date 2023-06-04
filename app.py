from flask import Flask, jsonify, request, json
from flask_cors import CORS
from aiengine.config import Config
from message_handler import handle_whatsapp_message
import os
from dotenv import load_dotenv
from user_handler import create_user
from db_tables import create_db_tables
load_dotenv()

# from data_handler import save_whatsapp_messages
# from utils import find_key_value


app = Flask(__name__)
CORS(app)
# print('__name__', __name__)

# create database connection


# user_crud = UserCRUD()

create_db_tables()


@app.route("/hello_world")
def hello_world():
    return "Hello World!"


@app.route("/whatsapp_webhook", methods=['GET', 'POST'])
def whatsapp_webhook():
    print("The hook is invoked with payload...")
    """__summary__: Get message from the webhook"""
    cfg = Config()
    if request.method == "GET":
        if request.args.get('hub.verify_token') == cfg.whatsapp_verify_token:
            return request.args.get('hub.challenge')
        return "Authentication failed. Invalid Token."

    # call message_handler
    handle_whatsapp_message(request.get_json())

    return '', 200


# @app.route("/search", methods=['GET'])
# def search_messages():
#     print("Searching messages...")
#     """__summary__: Search message from the database"""
#     dataHandler = DataHandler()
#     results = dataHandler.search_message_data(request.args.get('from'));
#     return jsonify(results), 200


# Endpoints for managing users
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    print('data', data["email"])
    user_id = create_user(data["email"], data["phone_number"])
    return jsonify({'message': 'User created', 'user_id': user_id}), 201


if __name__ == '__main__':
    print('Starting Python Flask Server For WhatsApp Integration...')
    app.run(debug=False)
