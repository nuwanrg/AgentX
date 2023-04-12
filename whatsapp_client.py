#whatsapp_client.py
import os
import requests
import json
from utils import find_key_value
from heyoo import WhatsApp
from file_handler import FileHandler
from io import BytesIO
from database import save_media_metadata
import time



class WhatsAppWrapper:
    API_URL = "https://graph.facebook.com/v13.0/"
    API_TOKEN = os.getenv('WHATSAPP_API_TOKEN')
    NUMBER_ID = os.getenv('WHATSAPP_NUMBER_ID')


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
        # object_type = data["object"]
        # entry = data["entry"][0]
        # entry_id = entry["id"]
        # changes = entry["changes"][0]
        # value = changes["value"]
        # messaging_product = value["messaging_product"]
        # metadata = value["metadata"]
        # display_phone_number = metadata["display_phone_number"]
        # phone_number_id = metadata["phone_number_id"]
        # contacts = value["contacts"][0]
        # profile = contacts["profile"]
        # name = profile["name"]
        # wa_id = contacts["wa_id"]
        # messages = value["messages"][0]
        # msg_from = messages["from"]
        # profile = find_key_value(data, "profile")
        # name = find_key_value(profile, "name")

        msg_from = find_key_value(data, "from")
        name = find_key_value(data, "name")
        body = find_key_value(data, "body")
        # print("body ", body)
        # print("msg_from ", msg_from)
        # print("name ", name)

        message = 'Hi '+ name+ '. Thank you. We have received your message `' +body+'`.'
        response =  self.send_text_message(msg_from,message)


        return response

    def send_text_message(self, phone_number, message):
        print("send_text_message Invoked...")
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phone_number,
            "type": "text",
            "text": { 
                "preview_url": "false",
                "body": message
            }
        })

        # print(self.API_URL)
        # print(self.headers)

        response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)
        print("Message sent successfully... ")

        assert response.status_code == 200, "Error sending message"

        return response
    
    def handle_media_message(self, data, type):
        #media_id = find_key_value(data, "id")
        phone_number = find_key_value(data, "from")
        media = find_key_value(data, type)
        media_id=find_key_value(media, "id")
        caption=find_key_value(media, "caption")
        file_type=find_key_value(media, "mime_type")


        media_endpoint = f"https://graph.facebook.com/v16.0/{media_id}?access_token={self.API_TOKEN}"
        response = requests.get(media_endpoint, stream=True)
        file_url= response.url


        print("phone_number ", phone_number)
        print("media ", media)
        print("media_id ", media_id)
        print("file_url ", file_url)
        print("file_type ", file_type)
   
        file_object = self.download_file_from_whatsapp(media_id, self.API_TOKEN)

        if file_object:
            s3_object_name = media_id
            bucket_name = os.getenv('THT_DEV_BUCKET')
            file_handler = FileHandler()

            print( "file_object ", file_object)            
            s3_url = file_handler.upload_file_to_s3(file_object, bucket_name, s3_object_name)
            print("s3_url ", s3_url)

            #Save image metadata to DB
            file_url = 'none'
            #file_handler.generate_s3_url(bucket_name, s3_object_name)
            print("file_url ", file_url)

            save_media_metadata(media_id, caption, file_url, file_type )

        
        messenger = WhatsApp(self.API_TOKEN,  phone_number_id=self.NUMBER_ID)
        if type=='image':
            messenger.send_image(media_id,phone_number,link=False )
        elif type=='video': 
            messenger.send_video(media_id,phone_number,link=False )
        return
    
    def download_file_from_whatsapp(self,media_id, access_token):
        url = f"https://graph.facebook.com/v12.0/{media_id}?access_token={access_token}"
        response = requests.get(url, stream=True)

        if response.status_code != 200:
            print(f"Error downloading media file: {response.status_code} - {response.text}")
            return None

        return BytesIO(response.content)
    
    def handle_video_message(data):
        return