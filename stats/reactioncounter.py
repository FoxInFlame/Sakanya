# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Impor asyncio to sleep when resetting to disable overwrite
import asyncio
# Import JSON to read json
import json
# Import Sakanya Core
from core import SakanyaCore

class Stats_ReactionCounter():
  """
  EDIT: After IATGOF's server crash, Counting since 2018-09-26 19:43 JST
  Counting since 2018-03-26 11:00 JST
  """

  def __init__(self, bot):
    self.bot = bot
    try:
      data_file = SakanyaCore().r.get('reactions')
      try:
        self.reactions_json = json.loads(data_file)
      except (TypeError, ValueError) as e:
        self.reactions_json = {}
    except:
      self.reactions_json = {}

  async def on_ready(self):
    # Set the list of server emojis so we can quickly check against it
    server = self.bot.get_server(SakanyaCore().server_id())
    self.server_emojis = server.emojis

  async def on_message(self, message):
    """
    Take count of the emojis inside a message so that we can put them into the JSON.
    """

    if message.server is None or message.server.id != SakanyaCore().server_id():
      return
    
    if message.author.bot is True:
      return

    for server_emoji in self.server_emojis:
      # Check if each emoji exists inside the message, and if so, update the JSON.
      amount_of_times_reaction_used = message.content.count(str(server_emoji))
      if amount_of_times_reaction_used > 0:
        if str(server_emoji) in self.reactions_json:
          self.reactions_json[str(server_emoji)] = self.reactions_json[str(
              server_emoji)] + amount_of_times_reaction_used
        else:
          self.reactions_json[str(server_emoji)
                              ] = amount_of_times_reaction_used
        
        SakanyaCore().r.set('reactions', json.dumps(self.reactions_json))

  async def on_reaction_add(self, reaction, user):
    """
    Add one for the reaction.
    Only called on message in Saka's cache (which means messages sent after bot start)
    """

    # Don't count statistics if the reaction is not a server emoji
    if reaction.custom_emoji is False:
      return

    if str(reaction.emoji) in self.reactions_json:
      self.reactions_json[str(reaction.emoji)
                          ] = self.reactions_json[str(reaction.emoji)] + 1
    else:
      self.reactions_json[str(reaction.emoji)] = 1
    SakanyaCore().r.set('reactions', json.dumps(self.reactions_json))
  
  async def on_reaction_remove(self, reaction, user):
    """
    Subtract one for the reaction.
    Only called on message in Saka's cache (which means messages sent after bot start)
    """
    
    # Don't count statistics if the reaction is not a server emoji
    if reaction.custom_emoji is False:
      return

    # If the reaction exists already, act accordingly
    # Otherwise, don't do anything
    if str(reaction.emoji) in self.reactions_json:
      # Remove key altogether if result is 0
      if self.reactions_json[str(reaction.emoji)] <= 1:
        self.reactions_json.pop(str(reaction.emoji), None)
      else:
        self.reactions_json[str(reaction.emoji)
                            ] = self.reactions_json[str(reaction.emoji)] - 1
    # Set Redis as well
    SakanyaCore().r.set('reactions', json.dumps(self.reactions_json))

  async def on_socket_response(self, jsonmsg):
    """
    Add/Subtract one for the reaction.
    Called for all responses, but filter out ones before cache with the presence of the
    'emoji' key
    """

    if jsonmsg['t'] == 'MESSAGE_REACTION_ADD' and 'emoji' in jsonmsg['d']:

      # Check if the event is valid
      if jsonmsg['d']['emoji']['id'] is None:
        return
      # Parse the emoji ID (which is going to be used as the key)
      key = '<:' + jsonmsg['d']['emoji']['name'] + ':' + jsonmsg['d']['emoji']['id'] + '>'
      # Check existence of emoji in database
      if key in self.reactions_json:
        self.reactions_json[key] = self.reactions_json[key] + 1
      else:
        self.reactions_json[key] = 1
      # Set Redis database as well
      SakanyaCore().r.set('reactions', json.dumps(self.reactions_json))
    
    elif jsonmsg['t'] == 'MESSAGE_REACTION_REMOVE' and 'emoji' in jsonmsg['d']:

      # Check if the event is valid
      if jsonmsg['d']['emoji']['id'] is None:
        return
      # Parse the emoji ID
      key = '<:' + jsonmsg['d']['emoji']['name'] + ':' + jsonmsg['d']['emoji']['id'] + '>'
      # Check existence of emoji in database
      if key in self.reactions_json:
        # If value becomes 0, remove the key altogether
        if self.reactions_json[key] <= 1:
          self.reactions_json.pop(key, None)
        else:
          self.reactions_json[key] = self.reactions_json[key] - 1
      # Set Redis Database as well
      SakanyaCore().r.set('reactions', json.dumps(self.reactions_json))

  @commands.command(pass_context=True)
  @commands.check(SakanyaCore().is_owner)
  async def reset_reactioncount(self, context, reaction=None):
    asyncio.sleep(1) # Prevent bumping into on_message handlers
    resetreaction = self.reactions_json.pop(reaction, None)
    if resetreaction is not None:
      SakanyaCore().r.set('reactions', json.dumps(self.reactions_json))
      await self.bot.add_reaction(context.message, '✅')

  @commands.command(pass_context=True)
  @commands.check(SakanyaCore().is_owner)
  async def override_reactioncount(self, context, reaction=None, overrideCount=None):
    if overrideCount is not None:
      self.reactions_json[reaction] = overrideCount
      SakanyaCore().r.set('reactions', json.dumps(self.reactions_json))
      await self.bot.add_reaction(context.message, '✅')
    else:
      await self.bot.add_reaction(context.message, '❎')

def setup(bot):
  bot.add_cog(Stats_ReactionCounter(bot))
