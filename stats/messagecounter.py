# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import os to use relative file names
import os
# Import JSON to read roles.json
import json
# Import Sakanya Core
from __main__ import SakanyaCore

class Stats_MessageCounter():
  """
  EDIT: After IATGOF's server crash, Counting since 2018-09-26 19:43 JST
  Counting since 2017-11-23 22:00 JST
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
      if isinstance(self.authors_json[message.author.id], int):
        self.authors_json[message.author.id] = {
          'count': self.authors_json[message.author.id] + 1
        }
      else:
        self.authors_json[message.author.id]['count'] = self.authors_json[message.author.id]['count'] + 1
    else:
      self.authors_json[message.author.id] = {
        'count': 1
      }

    self.authors_json[message.author.id]['name'] = message.author.name
    
    if 'bot' not in self.authors_json[message.author.id]:
      self.authors_json[message.author.id]['bot'] = message.author.bot

    with open(os.path.join(os.path.dirname(__file__), 'authors.json'), 'w') as file: # Then overwrite the file
      file.write(json.dumps(self.authors_json, indent=2))


  @commands.command(pass_context=True)
  async def reset_messagecount(self, context, userid=None):
    if context.message.author.id == '202501452596379648':
      resetuser = self.authors_json.pop(userid, None)
      if resetuser is not None:
        # Then overwrite the file
        with open(os.path.join(os.path.dirname(__file__), 'authors.json'), 'w') as file:
          file.write(json.dumps(self.authors_json, indent=2))
          await self.bot.add_reaction(context.message, '✅')  # Add checkmark
    else:
      await self.bot.add_reaction(context.message, '❎')  # Add x mark

  @commands.command(pass_context=True)
  async def override_messagecount(self, context, userid=None, overrideCount=None):
    if context.message.author.id == '202501452596379648' and overrideCount is not None:
      if userid in self.authors_json:
        self.authors_json[userid]['count'] = overrideCount
      else:
        override_user = await self.bot.get_user_info(userid)
        self.authors_json[userid] = {
           'count': overrideCount,
           'name': override_user.name,
           'bot': override_user.bot
        }
      # Then overwrite the file
      with open(os.path.join(os.path.dirname(__file__), 'authors.json'), 'w') as file:
        file.write(json.dumps(self.authors_json, indent=2))
        await self.bot.add_reaction(context.message, '✅')
    else:
      await self.bot.add_reaction(context.message, '❎')
  
def setup(bot):
  bot.add_cog(Stats_MessageCounter(bot))
