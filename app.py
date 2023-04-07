from flask import Flask, jsonify, request,json

from whatsapp_client import WhatsAppWrapper
from utils import find_key_value

app = Flask(__name__)
VERIFY_TOKEN = "THT_VERIFY_TOKEN"

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
    print("The hook is invoked with payload.")
    """__summary__: Get message from the webhook"""

    if request.method == "GET":
        if request.args.get('hub.verify_token') == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        return "Authentication failed. Invalid Token."
    
    client = WhatsAppWrapper()
    
    data = request.get_json()
    print("data", data)

    #category = find_key_value(data, "category")
    #print("category ", category) 
        # if category == "user_initiated":
        # print("user_initiated")
        # return '', 204
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
    

    # Access data in the dictionary
    object_type = data["object"]
    entry = data["entry"][0]
    entry_id = entry["id"]
    changes = entry["changes"][0]
    value = changes["value"]
    messaging_product = value["messaging_product"]
    metadata = value["metadata"]
    display_phone_number = metadata["display_phone_number"]
    phone_number_id = metadata["phone_number_id"]
    contacts = value["contacts"][0]
    profile = contacts["profile"]
    name = profile["name"]
    wa_id = contacts["wa_id"]
    messages = value["messages"][0]
    msg_from = messages["from"]
    print("msg_from", msg_from)




    # Do anything with the response
    # Sending a message to a phone number to confirm the webhook is working

    return '', 200

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
    app.run(debug=True)
