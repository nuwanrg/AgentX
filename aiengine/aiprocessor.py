import sys
import os
from colorama import Fore, Style
from aiengine.config.config import Config, check_openai_api_key
from monitor.logs import logger
from aiengine.prompt import construct_prompt
from aiengine.llm_utils import create_chat_completion

def process_message(text_msg)->str:

    print("Processing message")

    cfg = Config()

    if(cfg.app_mode == 'agent'):
        check_openai_api_key()

        #System has to decide what kind of a prompt it requires to create. For example a caht model or auto agent model
        system_prompt = construct_prompt(text_msg)

        print("System prompt created", system_prompt)


        logger.typewriter_log(
        "FAILED TO GET RESPONSE FROM OPENAI",
        Fore.RED,
        "System failed to get a response from OpenAI's services. "
        + f"Try running it again, and if the problem the persists try running it with `{Fore.CYAN}--debug{Fore.RESET}`.",
        )
    else:
        print("App mode is not agent. So not processing the message")
        messages=[{"role": "user", "content": text_msg}
  ]
        response =create_chat_completion(messages, cfg.fast_llm_model, cfg.temperature, cfg.fast_token_limit)
    return response
