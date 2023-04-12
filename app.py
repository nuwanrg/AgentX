import config
import os
from flask import Flask, jsonify, request,json

from whatsapp_client import WhatsAppWrapper
from utils import find_key_value
from database import create_tables, save_message_data, search_message_data,drop_tables
app = Flask(__name__)
print('__name__', __name__);

#Enable this to drop the tables when the application starts. This has to handle different way when the application is deployed in production
drop_tables()

# Call the create_table function to set up the table when the application starts
create_tables()

@app.route("/")
def hello_world():
    return "Hello World!"

@app.route('/getResponse', methods=['GET'])
def whatsapp_webhook():
    # You can access query parameters using request.args.get()
    # For example, if your webhook has a query parameter 'message':
    # message = request.args.get('message', '')
    response = {
        "status": "success",
        "message": "WhatsApp webhook received"
    }
    return jsonify(response)



@app.route("/webhook", methods=['GET', 'POST'])
def webhook_whatsapp():
    print("The hook is invoked with payload...")
    """__summary__: Get message from the webhook"""

    if request.method == "GET":
        if request.args.get('hub.verify_token') == os.getenv('WHATSAPP_VERIFY_TOKEN'):
            return request.args.get('hub.challenge')
        return "Authentication failed. Invalid Token."
    
    data = request.get_json()
    print("data", data)

    #Save the data to the database
    save_message_data(data)

    client = WhatsAppWrapper()
    type = find_key_value(data, "type")
    print("type ", type)
   
    if type == "user_initiated":
        print("user_initiated")
        return '', 204
    elif type == "text":
        response = client.handle_text_message(data)
    elif type == "image":
        response = client.handle_image_message(data)
    elif type == "video":
        response = client.handle_video_message(data)

    return '', 200


@app.route("/search", methods=['GET'])
def search_messages():
    print("Searching messages...")
    """__summary__: Search message from the database"""

    results = search_message_data(request.args.get('from'));
    return jsonify(results), 200



#some test code
@app.route("/send_template_message", methods=["POST"])
def send_template_message():
    print("send_template_message Invoked")
    """_summary_: Send a message with a template to a phone number"""

    if "language_code" not in request.json:
        return jsonify({"error": "Missing language_code"}), 400

    if "phone_number" not in request.json:
        return jsonify({"error": "Missing phone_number"}), 400

    if "template_name" not in request.json:
        return jsonify({"error": "Missing template_name"}), 400

    client = WhatsAppWrapper()
    
    print(request.get_json())
    response = client.send_template_message(
        template_name=request.json["template_name"],
        language_code=request.json["language_code"],
        phone_number=request.json["phone_number"],
    )

    return jsonify(
        {
            "data": response,
            "status": "success",
        },
    ), 200
    
if __name__ == '__main__':
    print('Starting Python Flask Server For WhatsApp Integration...')
    app.run(debug=True)
