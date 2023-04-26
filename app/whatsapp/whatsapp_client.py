#whatsapp_client.py
import os
import requests
import json
from utils import find_key_value
from heyoo import WhatsApp
from io import BytesIO

from aiengine.config import Config
cfg = Config()


headers = {
    "Authorization": f"Bearer {cfg.whatsapp_api_token}",
    "Content-Type": "application/json",
}
API_URL = "https://graph.facebook.com/v13.0/" + cfg.whatsapp_number_id


def send_text_message (phone_number, message):

    # message = 'Hi '+ name+ '. Thank you. We have received your message `' +body+'`.'
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
    response = requests.request("POST", f"{API_URL}/messages", headers=headers, data=payload)
    print("Message sent successfully... ")

    assert response.status_code == 200, "Error sending message"

    return response

def handle_media_message(data, type):
    phone_number = find_key_value(data, "from")
    media = find_key_value(data, type)
    media_id=find_key_value(media, "id")
    caption=find_key_value(media, "caption")
    file_type=find_key_value(media, "mime_type")


    media_endpoint = f"https://graph.facebook.com/v16.0/{media_id}?access_token={cfg.whatsapp_api_token}"
    response = requests.get(media_endpoint, stream=True)
    file_url= response.url
    
    messenger = WhatsApp(cfg.whatsapp_api_token,  phone_number_id=cfg.whatsapp_number_id)
    if type=='image':
        messenger.send_image(media_id,phone_number,link=False )
    elif type=='video': 
        messenger.send_video(media_id,phone_number,link=False )
    return

def download_file_from_whatsapp(media_id):
    url = f"https://graph.facebook.com/v12.0/{media_id}?access_token={cfg.whatsapp_api_token}"
    response = requests.get(url, stream=True)

    if response.status_code != 200:
        print(f"Error downloading media file: {response.status_code} - {response.text}")
        return None

    return BytesIO(response.content)

def handle_video_message(data):
    return