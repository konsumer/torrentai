import os
import chainlit as cl
import logging
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage
from docstring_parser import parse
import tools

def tool_parse(tools):
  """
  build tools inform from functions & docs
  """
  toolsOut = []
  for fname in dir(tools):
    if not fname.startswith('__'):
      f = getattr(tools, fname)
      d = parse(f.__doc__)
      newtool = { "parameters": {"type": "object", "properties": {}}, "required": [], "name":fname, "description": d.description.strip() } 
      for p in d.params:
        newtool["parameters"]["properties"][p.arg_name] = {
          "type": p.type_name,
          "description": p.description
        }
        if not  p.is_optional:
          newtool["required"].append(p.arg_name)

      toolsOut.append(newtool)
  return toolsOut

tools_description = tool_parse(tools)

PROMPT_SYSTEM=os.getenv('PROMPT_SYSTEM', "You are a helpful AI assistant that manages torrents and helps users download media. Use the provided tools when necessary.")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

prompt = ChatPromptTemplate.from_messages([
  SystemMessage(content=PROMPT_SYSTEM),
  ("human", "{input}"),
])

# generate tools info from tools

def formatSize(sizeInBytes, decimalNum=1, isUnitWithI=False, sizeUnitSeperator=""):
  """format size to human readable string"""
  # https://en.wikipedia.org/wiki/Binary_prefix#Specific_units_of_IEC_60027-2_A.2_and_ISO.2FIEC_80000
  # K=kilo, M=mega, G=giga, T=tera, P=peta, E=exa, Z=zetta, Y=yotta
  sizeUnitList = ['','K','M','G','T','P','E','Z']
  largestUnit = 'Y'

  if isUnitWithI:
    sizeUnitListWithI = []
    for curIdx, eachUnit in enumerate(sizeUnitList):
      unitWithI = eachUnit
      if curIdx >= 1:
        unitWithI += 'i'
      sizeUnitListWithI.append(unitWithI)

    # sizeUnitListWithI = ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']
    sizeUnitList = sizeUnitListWithI

    largestUnit += 'i'

  suffix = "B"
  decimalFormat = "." + str(decimalNum) + "f" # ".1f"
  finalFormat = "%" + decimalFormat + sizeUnitSeperator + "%s%s" # "%.1f%s%s"
  sizeNum = sizeInBytes
  for sizeUnit in sizeUnitList:
      if abs(sizeNum) < 1024.0:
        return finalFormat % (sizeNum, sizeUnit, suffix)
      sizeNum /= 1024.0
  return finalFormat % (sizeNum, largestUnit, suffix)

class TorrentAI:
  def __init__(self, *args):
    self.mediaInfo = []
    self.llmQuery = []
    self.torrentSource = []
    self.torrentManager = []
    self.collectionManager = []
    for adapter in args:
      adapter.engine = self
      if isinstance(adapter, MediaInfoBase):
        self.mediaInfo.append(adapter)
      elif isinstance(adapter, LlmQueryBase):
        self.llmQuery.append(adapter)
      elif isinstance(adapter, TorrentSourceBase):
        self.torrentSource.append(adapter)
      elif isinstance(adapter, TorrentManagerBase):
        self.torrentManager.append(adapter)
      elif isinstance(adapter, CollectionManagerBase):
        self.collectionManager.append(adapter)
    if len(self.llmQuery) != 1:
      raise Exception('You need only 1 LlmQuery provider.')
    if len(self.torrentManager) != 1:
      raise Exception('You need only 1 TorrentManager provider.')
    if len(self.torrentSource) < 1:
      raise Exception('You need at least 1 TorrentSource provider.')

  async def on_chat_start(self):
    logging.info("Chat started")
    cl.user_session.set("model", self.llmQuery[0].model)

  async def on_message(self, message: cl.Message):
    logging.info(f"Received message: {message.content}")
    try:
      response = await cl.make_async(self.process_query)(message.content)
      logging.info(f"Response: {response}")
      await cl.Message(content=response).send()
    except Exception as e:
      error_message = f"An error occurred: {str(e)}"
      logging.error(f"Error: {error_message}")
      await cl.Message(content=error_message).send()

  def process_query(self, query):
    logging.info(f"Processing query: {query}")
    formatted_prompt = prompt.format_messages(input=query)
    logging.debug(f"Formatted prompt: {formatted_prompt}")
    result = self.llmQuery[0].model.invoke(formatted_prompt)
    logging.info(f"Model result: {result}")
    if result.tool_calls:
      out = []
      for tool_call in result.tool_calls:
        function_name = tool_call['name']
        args = tool_call['args']
        logging.info(f"Function call: {function_name}, Args: {args}")
        function = getattr(self, function_name, None)
        if callable(function):
          out.append(function(args))
      print(out)
      return "\n".join(out)
    return result.content

  def output_results(self, type, args):
    results = []
    if "year" not in args:
      args['year']=None
    if "artist" not in args:
      args['artist']=None
    for adapter in self.torrentSource:
      newresults = adapter.get_torrents(type, args['title'], args['year'], args['artist'])
      results=[*results, *newresults]
    type_string = "TV show"
    if type == "movie":
      type_string = "the movie"
    if type == "album":
      type_string = "the album"
    out=f"Here is a list of available torrents for {type_string} {args['title']}:\n\n| id | title | ratio | size |\n|---|---|---|---|"
    for r in results:
      out = f"{out}\n| {r['id']} | {r['title']} | {r['seeders']}/{r['leechers']} | {formatSize(r['size'])}  |"
    out = f"{out}\n\nWhich do you want to download?"
    return out

  # these are tool-callbacks

  def download_torrent(self, args):
    self.torrentManager[0].download_torrent(args['id'])
    return f"Downloading torrent {args['id']}"

  def get_torrents_for_movie(self, args):
    return self.output_results("movie", args)

  def get_torrents_for_an_album(self, args):
    return self.output_results("album", args)

  def starters():
    return [
      cl.Starter(
        label="Find a movie and add it to library",
        message="Get the movie Labrynth",
        # icon="/public/idea.svg",
      ),
      cl.Starter(
        label="Check on a running download",
        message="How is Labrynth doing?",
        # icon="/public/idea.svg",
      ),
      cl.Starter(
        label="Get an album",
        message="How is Labrynth doing?",
        # icon="/public/idea.svg",
      ),
    ]



class MediaInfoBase:
  pass

class LlmQueryBase:
  pass

class TorrentSourceBase:
  pass

class TorrentManagerBase:
  pass

class CollectionManagerBase:
  pass
