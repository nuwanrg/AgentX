import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, jsonify, request,json

from message_handler import handle_whatsapp_message
#from data_handler import save_whatsapp_messages
#from utils import find_key_value
from aiengine.config import Config
from aws_lambda_wsgi import AwsLambdaWsgi



app = Flask(__name__)
# print('__name__', __name__)


#setup_database()

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

lambda_handler = AwsLambdaWsgi(app).handler

if __name__ == '__main__':
    print('Starting Python Flask Server For WhatsApp Integration...')
    app.run(debug=True)
