# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import JSON to read json
import json
# Import Sakanya Core
from core import SakanyaCore

class Stats_MessageCounter():
  """
  EDIT: After IATGOF's server crash, Counting since 2018-09-26 21:32 JST
  (+ rough visual estimate of previous stats since 9/18)
  Counting since 2017-11-23 22:00 JST
  """
  
  def __init__(self, bot):
    self.bot = bot
    try:
      data_file = SakanyaCore().r.get('authors')
      try:
        self.authors_json = json.loads(data_file)
      except (TypeError, ValueError) as e:
        self.authors_json = {}
    except:
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

    SakanyaCore().r.set('authors', json.dumps(self.authors_json))


  @commands.command(pass_context=True)
  @commands.check(SakanyaCore.is_owner)
  async def reset_messagecount(self, context, userid=None):
    resetuser = self.authors_json.pop(userid, None)
    if resetuser is not None:
      SakanyaCore().r.set('authors', json.dumps(self.authors_json))
      await self.bot.add_reaction(context.message, '✅')

  @commands.command(pass_context=True)
  @commands.check(SakanyaCore.is_owner)
  async def override_messagecount(self, context, userid=None, overrideCount=None):
    if overrideCount is not None:
      if userid in self.authors_json:
        self.authors_json[userid]['count'] = int(overrideCount)
      else:
        override_user = await self.bot.get_user_info(userid)
        self.authors_json[userid] = {
           'count': int(overrideCount),
           'name': override_user.name,
           'bot': override_user.bot
        }
      SakanyaCore().r.set('authors', json.dumps(self.authors_json))
      await self.bot.add_reaction(context.message, '✅')
    else:
      await self.bot.add_reaction(context.message, '❎')
  
def setup(bot):
  bot.add_cog(Stats_MessageCounter(bot))
