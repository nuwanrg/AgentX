import sys
import os
from .config.config import Config, check_openai_api_key
from monitor.logs import logger
from colorama import Fore, Style

def process_message(data)->str:
    logger.typewriter_log( "Invoked AI Message Processor",)
    return 'WhatsApp response'