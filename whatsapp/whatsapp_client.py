# whatsapp_client.py
import os
import requests
import json
from utils import find_key_value
from heyoo import WhatsApp
from io import BytesIO
from urllib import request
import openai
from aiengine.config import Config
from pydub import AudioSegment
cfg = Config()


openai.api_key = cfg.openai_api_key


headers = {
    "Authorization": f"Bearer {cfg.whatsapp_api_token}",
    "Content-Type": "application/json",
}
API_URL = "https://graph.facebook.com/v13.0/" + cfg.whatsapp_number_id


def send_text_message(phone_number, message):
    print("send_text_message is called... ")
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
    response = requests.request(
        "POST", f"{API_URL}/messages", headers=headers, data=payload)
    print("Message sent successfully... ")

    assert response.status_code == 200, "Error sending message"

    return response


def convert_ogg_to_mp3(ogg_file, mp3_file):
    # Load the OGG audio file
    ogg_audio = AudioSegment.from_ogg(ogg_file)

    # Export the audio in MP3 format
    ogg_audio.export(mp3_file, format="mp3")
    print(f"File '{mp3_file}' converted successfully.")


def download_file(url, headers, filename):
    response = requests.get(url, headers=headers, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"File '{filename}' downloaded successfully.")
    else:
        print(f"Failed to download file. Error: {response.text}")


def handle_media_message(data, type):
    phone_number = find_key_value(data, "from")
    media = find_key_value(data, type)
    media_id = find_key_value(media, "id")
    caption = find_key_value(media, "caption")
    file_type = find_key_value(media, "mime_type")

    media_api = f"https://graph.facebook.com/v16.0/{media_id}?access_token={cfg.whatsapp_api_token}"
    media = requests.get(media_api, stream=True)

    print('media_url.content :', media.content)

    # Convert the response content from bytes to a string

    response_text = media.content.decode('utf-8')

    # Parse the response text as JSON
    response_data = json.loads(response_text)

    # Extract the URL attribute from the response data
    url = response_data['url']
    # Print the URL
    print('url ', url)

    # url = "https://lookaside.fbsbx.com/whatsapp_business/attachments/?mid=243415971717183&ext=1685773628&hash=ATsG6MJ3v1JJ3fI7lwaSnEVMJxlNyF4aTlRvC8XQko54SA"
    headers = {"Authorization": f"Bearer {cfg.whatsapp_api_token}"}
    filename = f"{media_id}.ogg"
    mp3_file = f"{media_id}.mp3"
    download_file(url, headers, filename)
    convert_ogg_to_mp3(filename, mp3_file)

    # file_from_whatsapp = download_file_from_whatsapp(media_id)
    # print('file_from_whatsapp : ', file_from_whatsapp)

    # media_endpoint = f"https://graph.facebook.com/v16.0/{media_id}?access_token={cfg.whatsapp_api_token}"
    # response = requests.get(media_endpoint, stream=True)
    # file_url = response.url
    # print("file_url ", file_url)

    # data = download_file_from_whatsapp(media_id)
    # # print("data ", data)

    # messenger = WhatsApp(cfg.whatsapp_api_token,
    #                      phone_number_id=cfg.whatsapp_number_id)
    # if type == 'image':
    #     messenger.send_image(media_id, phone_number, link=False)
    # elif type == 'video':
    #     messenger.send_video(media_id, phone_number, link=False)
    # elif type == 'audio':

    #     url = "https://lookaside.fbsbx.com/whatsapp_business/attachments/?mid=3097496617213413&ext=1685611262&hash=ATsoayrtCpr65W7cJabWWGNjKuO7ZJ-T1KBl49HL2-B8nw"
    #     response = request.urlopen(url)
    #     audio_file = response.read()

    #     transcript = openai.Audio.transcribe("whisper-1", audio_file)
    #     print("transcript ", transcript)

    #     messenger.send_audio(media_id, phone_number, link=False)


def download_file_from_whatsapp(media_id):
    url = f"https://graph.facebook.com/v12.0/{media_id}?access_token={cfg.whatsapp_api_token}"
    response = requests.get(url, stream=True)
    print('response.content ', response.content)

    if response.status_code != 200:
        print(
            f"Error downloading media file: {response.status_code} - {response.text}")
        return None

    return BytesIO(response.content)


def handle_video_message(data):
    return
