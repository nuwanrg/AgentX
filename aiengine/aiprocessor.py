import sys
import os
from colorama import Fore, Style
from aiengine.config.config import Config, check_openai_api_key
from monitor.logs import logger
from aiengine.prompt import construct_prompt

def process_message(text_msg)->str:

    print("Processing message")

    #System has to decide what kind of a prompt it requires to create. For example a caht model or auto agent model
    system_prompt = construct_prompt(text_msg)

    print("System prompt created", system_prompt)


    logger.typewriter_log(
    "FAILED TO GET RESPONSE FROM OPENAI",
    Fore.RED,
    "Auto-GPT has failed to get a response from OpenAI's services. "
    + f"Try running Auto-GPT again, and if the problem the persists try running it with `{Fore.CYAN}--debug{Fore.RESET}`.",
    )
    return 'WhatsApp response'
