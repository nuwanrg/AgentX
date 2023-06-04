import sys
import os
from colorama import Fore, Style
from aiengine.config.config import Config, check_openai_api_key
from monitor.logs import logger
from aiengine.prompt import construct_prompt
from aiengine.llm_utils import create_chat_completion
from aiengine.memory import get_memory
from aiengine.agent import Agent


def process_message(text_msg) -> str:

    print("Processing message")

    cfg = Config()

    if (cfg.app_mode == 'agent'):
        check_openai_api_key()

        # System has to decide what kind of a prompt it requires to create. For example a caht model or auto agent model
        system_prompt = construct_prompt(text_msg)
        print("System prompt created \n", system_prompt)

        full_message_history = []
        next_action_count = 0
        triggering_prompt = (
            "Determine which next command to use, and respond using the"
            " format specified above:"
        )

        # Initialize memory and make sure it is empty.
        # this is particularly important for indexing and referencing pinecone memory
        memory = get_memory(cfg, init=True)
        print("Memory initialized", memory.get_stats)

        agent = Agent(
            ai_name=cfg.ai_name,
            memory=memory,
            full_message_history=full_message_history,
            next_action_count=next_action_count,
            system_prompt=system_prompt,
            triggering_prompt=triggering_prompt,
        )

        agent.start_interaction_loop()

        return system_prompt

    else:
        print("App mode is not agent. So not processing the message")
        messages = [{"role": "user", "content": text_msg}]
        response = create_chat_completion(
            messages, cfg.fast_llm_model, cfg.temperature, cfg.fast_token_limit)
        return response
