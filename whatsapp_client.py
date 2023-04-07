# app/whatsapp_client.py

import os
import requests

import json
from utils import find_key_value
from heyoo import WhatsApp


class WhatsAppWrapper:
    API_URL = "https://graph.facebook.com/v13.0/"
    API_TOKEN = os.environ.get("WHATSAPP_API_TOKEN")
    NUMBER_ID = os.environ.get("WHATSAPP_NUMBER_ID")

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {self.API_TOKEN}",
            "Content-Type": "application/json",
        }
        self.API_URL = self.API_URL + self.NUMBER_ID

    def send_template_message(self, template_name, language_code, phone_number):

        payload = json.dumps({
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": language_code
                }
            }
        })

        print(self.API_URL)
        print(self.headers)

        response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)

        assert response.status_code == 200, "Error sending message"

        return response.status_code
    
    def handle_text_message (self, data):
        print("handle_text_message Invoked")
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
        response =  self.send_text_message(msg_from)
        return response

    def send_text_message(self, phone_number):
        print("send_text_message Invoked")
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phone_number,
            "type": "text",
            "text": { 
                "preview_url": "false",
                "body": "Text Reply Test"
            }
        })

        # print(self.API_URL)
        # print(self.headers)

        response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)
        print("Message sent successfully. response ", response)

        assert response.status_code == 200, "Error sending message"

        return response
    
    def handle_image_message(self, data):
        media_id = find_key_value(data, "id")
        phone_number = find_key_value(data, "from")
        image = find_key_value(data, "image")
        image_id=find_key_value(image, "id")
        print("media_id ", media_id)
        print("phone_number ", phone_number)
        print("image ", image)
        print("image_id ", image_id)

        messenger = WhatsApp(self.API_TOKEN,  phone_number_id=self.NUMBER_ID)
        messenger.send_image(image_id,phone_number,link=False )
        return
    
    def handle_video_message(data):
        return