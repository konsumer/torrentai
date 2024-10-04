"""
This will use ollama server to do LLM requests

env-vars:
  OLLAMA_HOST="localhost:11434" # the host where ollama is running
  OLLAMA_MODEL="llama3.2"       # the model-name to use. should have function-calling and stuff
"""

import os
from torrentai import prompt, tools, LlmQueryBase
from langchain_ollama import ChatOllama

OLLAMA_HOST=os.getenv('OLLAMA_HOST', 'localhost:11434')
OLLAMA_MODEL=os.getenv('OLLAMA_MODEL', 'llama3.2')

class LlmQuery(LlmQueryBase):
  def __init__(self, host=OLLAMA_HOST, model=OLLAMA_MODEL):
    self.model = ChatOllama(model=model, format="json", temperature=0).bind_tools(tools=tools)
    self.prompt = prompt
