import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, jsonify, request,json

from message_handler import handle_whatsapp_message
from utils import find_key_value
from aiengine.config import Config

app = Flask(__name__)
print('__name__', __name__)

cfg=Config()

#setup_database()

@app.route("/")
def hello_world():
    return "Hello World!"

@app.route("/webhook", methods=['GET', 'POST'])
def webhook_whatsapp():
    print("The hook is invoked with payload...")
    """__summary__: Get message from the webhook"""

    if request.method == "GET":
        if request.args.get('hub.verify_token') == cfg.whatsapp_api_token:
            return request.args.get('hub.challenge')
        return "Authentication failed. Invalid Token."
    
    #call message_handler
    handle_whatsapp_message(request.get_json())

    return '', 200


# @app.route("/search", methods=['GET'])
# def search_messages():
#     print("Searching messages...")
#     """__summary__: Search message from the database"""
#     dataHandler = DataHandler()
#     results = dataHandler.search_message_data(request.args.get('from'));
#     return jsonify(results), 200

    
if __name__ == '__main__':
    print('Starting Python Flask Server For WhatsApp Integration...')
    app.run(debug=True)
