"""
This will use ollama server to do LLM requests

env-vars:
  OLLAMA_HOST="localhost:11434" # the host where ollama is running
  OLLAMA_MODEL="llama3.2"       # the model-name to use. should have function-calling and stuff
"""

import os

OLLAMA_HOST=os.getenv('OLLAMA_HOST', 'localhost:11434')
OLLAMA_MODEL=os.getenv('OLLAMA_MODEL', 'llama3.2')

class LlmQuery:
  pass