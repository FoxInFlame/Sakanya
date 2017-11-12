# Import discord
import discord
# Import os to use relative file names
import os
# Import JSON to read roles.json
import json
# Import Sakanya Core
from __main__ import SakanyaCore

class Stats_MessageCounter():
  """
  Counting since 2017-11-12 10:00 JST
  """
  
  def __init__(self, bot):
    self.bot = bot
    try:
      with open(os.path.join(os.path.dirname(__file__), 'authors.json'), 'r') as data_file:
        try:
          self.authors_json = json.load(data_file)
        except ValueError as e:
          self.authors_json = {}
    except IOError:
      self.authors_json = {}

  async def on_message(self, message):
    """
    Take count of the sent messages so that we can draw graphs from them.
    """
    if message.server is None or message.server.id != SakanyaCore().server_id():
      return

    if message.author.id in self.authors_json:
      self.authors_json[message.author.id] = self.authors_json[message.author.id] + 1
    else:
      self.authors_json[message.author.id] = 1

    with open(os.path.join(os.path.dirname(__file__), 'authors.json'), 'w') as file: # Then overwrite the file
      file.write(json.dumps(self.authors_json, indent=2))


def setup(bot):
  bot.add_cog(Stats_MessageCounter(bot))