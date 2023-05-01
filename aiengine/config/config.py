"""Configuration class to store the state of bools for different scripts access."""
import os

import openai
import yaml
from colorama import Fore
from dotenv import load_dotenv

from aiengine.config.singleton import Singleton

load_dotenv(verbose=True)


class Config(metaclass=Singleton):
    """
    Configuration class to store the state of bools for different scripts access.
    """

    def __init__(self) -> None:
        """Initialize the Config class"""
        # self.debug_mode = False
        # self.continuous_mode = False
        # self.continuous_limit = 0
        # self.speak_mode = False
        # self.skip_reprompt = False
        self.allow_downloads = False
        # self.skip_news = False

        #Database
        self.db_name = os.getenv("DB_NAME")
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_host = os.getenv("DB_HOST")
        self.db_port = os.getenv("DB_PORT")

        #Whatsapp
        self.whatsapp_api_token=os.getenv("WHATSAPP_API_TOKEN")
        self.whatsapp_number_id=os.getenv("WHATSAPP_NUMBER_ID")
        self.whatsapp_hook_token=os.getenv("WHATSAPP_HOOK_TOKEN")
        self.whatsapp_verify_token =os.getenv("WHATSAPP_VERIFY_TOKEN")

        #OPENAI
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.temperature = float(os.getenv("TEMPERATURE", "0"))

        #S3
        self.s3_bucket_dev = os.getenv("S3_BUCKET_DEV")

        self.ai_settings_file = os.getenv("AI_SETTINGS_FILE", "ai_settings.yaml")
        self.fast_llm_model = os.getenv("FAST_LLM_MODEL", "gpt-3.5-turbo")
        self.smart_llm_model = os.getenv("SMART_LLM_MODEL", "gpt-4")
        self.fast_token_limit = int(os.getenv("FAST_TOKEN_LIMIT", 4000))
        self.smart_token_limit = int(os.getenv("SMART_TOKEN_LIMIT", 8000))
        self.browse_chunk_max_length = int(os.getenv("BROWSE_CHUNK_MAX_LENGTH", 3000))
        self.browse_spacy_language_model = os.getenv(
            "BROWSE_SPACY_LANGUAGE_MODEL", "en_core_web_sm"
        )

        #PINECONE
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        self.pinecone_region = os.getenv("PINECONE_ENV")

        self.huggingface_audio_to_text_model = os.getenv(
            "HUGGINGFACE_AUDIO_TO_TEXT_MODEL"
        )

        self.execute_local_commands = (
            os.getenv("EXECUTE_LOCAL_COMMANDS", "False") == "True"
        )

        openai.api_key = self.openai_api_key



def check_openai_api_key() -> None:
    """Check if the OpenAI API key is set in config.py or as an environment variable."""
    cfg = Config()
    if not cfg.openai_api_key:
        print(
            Fore.RED
            + "Please set your OpenAI API key in .env or as an environment variable."
        )
        print("You can get your key from https://platform.openai.com/account/api-keys")
        exit(1)
