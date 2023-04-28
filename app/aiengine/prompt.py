from colorama import Fore

from aiengine.config import Config
from aiengine.config.ai_config import AIConfig
from aiengine.config.config import Config
from app.logs import logger
from .promptgenerator import PromptGenerator


CFG = Config()

def construct_prompt() -> str:
    """Construct the prompt for the AI to respond to

    Returns:
        str: The prompt string
    """
    config = AIConfig.load(CFG.ai_settings_file)


    return config.construct_full_prompt()