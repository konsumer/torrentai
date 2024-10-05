"""
This will use ollama server to do LLM requests

env-vars:
  URL_OLLAMA="localhost:11434" # the host where ollama is running
  OLLAMA_MODEL="llama3.2"       # the model-name to use. should have function-calling and stuff
"""

import os
from torrentai import prompt, tools, LlmQueryBase
from langchain_ollama import ChatOllama

URL_OLLAMA=os.getenv('URL_OLLAMA', 'http://localhost:11434')
OLLAMA_MODEL=os.getenv('OLLAMA_MODEL', 'llama3.2')

class LlmQuery(LlmQueryBase):
  def __init__(self, host=URL_OLLAMA, model=OLLAMA_MODEL):
    self.model = ChatOllama(model=model, format="json", temperature=0).bind_tools(tools=tools)
    self.prompt = prompt
