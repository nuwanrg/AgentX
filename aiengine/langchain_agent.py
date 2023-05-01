import os
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI

from aiengine.config import Config
cfg = Config()

llm = OpenAI(temperature=cfg.temperature,openai_api_key=cfg.openai_api_key)
tools = load_tools(["serpapi", "llm-math"], llm=llm)
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
agent.run("Wha is the weather like in Bali today?")