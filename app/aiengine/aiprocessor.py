from .config.config import Config, check_openai_api_key

def process_message(data)->str:
    print('AIEngine Invoked')
    return 'WhatsApp response'