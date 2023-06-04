# message_handler.py
import os
import requests
import json
from speech_to_text import convert_speech_to_text
from whatsapp.whatsapp_client import send_text_message, handle_media_message, handle_video_message
from data_handler import save_whatsapp_messages
from utils import find_key_value
from aiengine.aiprocessor import process_message
from user_handler import get_user_by_phone, update_user_message_count, create_user
from pydub import AudioSegment
from user_dto import UserDTO
from aiengine.config import Config
cfg = Config()


def handle_whatsapp_message(data):
    # Deconstruct the message
    print("incoming_message data ", data)
    phone_number = find_key_value(data, "from")
    name = find_key_value(data, "name")
    incoming_message = find_key_value(data, "body")
    statuses = find_key_value(data, "statuses")
    # print('statuses', statuses)

    catergory = find_key_value(data, "category")

    if catergory == "business_initiated":
        return '', 204

    # Save incoming messages from Whatsapp to the database
    save_whatsapp_messages(data)

    if statuses:
        # todo handle the statuses
        return '', 204

    # save user
    phone_number = find_key_value(data, "from")
    user_dto = UserDTO()
    user_dto.phone_number = phone_number
    create_user(user_dto)

    user = get_user_by_phone(phone_number)
    print("user.message_count ", user.message_count)

    if user.message_count is None:
        count = 1
    else:
        count = user.message_count + 1

    update_user_message_count(phone_number, count)

    # Respond to the message received from Whatsapp
    type = find_key_value(data, "type")
    print("type ", type)
    if type == "user_initiated":
        print("user_initiated")
        return '', 204
    elif type == "text":
        # Process the message in the AI engine
        response = process_message(incoming_message)
        send_text_message(phone_number, response)
    elif type == "image" or type == "video" or type == "audio":
        transcript = convert_media_message(data, type)
        response = process_message(transcript)
        send_text_message(phone_number, response)

    elif type == "video":
        response = handle_video_message(data)


def convert_media_message(data, type):
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
    filename = f"media/{media_id}.ogg"
    mp3_file = f"media/{media_id}.mp3"
    download_file(url, headers, filename)
    convert_ogg_to_mp3(filename, mp3_file)

    # call to openai whisper
    transcript = convert_speech_to_text(mp3_file)

    # delete ogg file
    delete_file(filename)

    # delete mp3 file
    delete_file(mp3_file)
    return transcript


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


def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File '{file_path}' deleted successfully.")
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except PermissionError:
        print(f"Permission denied: unable to delete file '{file_path}'.")
    except Exception as e:
        print(f"An error occurred while deleting file '{file_path}': {str(e)}")
