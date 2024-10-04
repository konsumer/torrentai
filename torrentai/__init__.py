import chainlit as cl

class TorrentAI:
  def __init__(self, *args):
    print(args)

  async def on_chat_start(self):
    pass

  async def on_message(self, message: cl.Message):
    pass
