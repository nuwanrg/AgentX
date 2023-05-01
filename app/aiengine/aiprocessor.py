import sys
import os
from app.aiengine.config.config import Config, check_openai_api_key
from app.monitor.logs import logger
from prompt import construct_prompt

def process_message(data)->str:

    print("Processing message")
    system_prompt = construct_prompt(data)


    logger.typewriter_log(
    "FAILED TO GET RESPONSE FROM OPENAI",
    Fore.RED,
    "Auto-GPT has failed to get a response from OpenAI's services. "
    + f"Try running Auto-GPT again, and if the problem the persists try running it with `{Fore.CYAN}--debug{Fore.RESET}`.",
    )
    return 'WhatsApp response'
