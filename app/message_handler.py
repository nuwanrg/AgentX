# message_handler.py
from utils import find_key_value
from data.data_handler import save_whatsapp_messages
from whatsapp.whatsapp_client import send_text_message, handle_media_message, handle_video_message
from aiengine.aiprocessor import process_message


def handle_whatsapp_message(data):
    #Deconstruct the message
    phone_number = find_key_value(data, "from")
    name = find_key_value(data, "name")
    incoming_message = find_key_value(data, "body")

    # Save incoming messages from Whatsapp to the database
    save_whatsapp_messages(data)

    # Process the message in the AI engine
    response = process_message(incoming_message)
    
    type = find_key_value(data, "type")
    print("type ", type)

    #Respond to the message received from Whatsapp
    if type == "user_initiated":
        print("user_initiated")
        return '', 204
    elif type == "text":
        response = send_text_message(phone_number, response)
    elif type == "image" or type == "video":
        response = handle_media_message(data, type)
    elif type == "video":
        response = handle_video_message(data)
