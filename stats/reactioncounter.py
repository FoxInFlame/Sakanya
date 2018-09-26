# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import os to use relative file names
import os
# Impor asyncio to sleep when resetting to disable overwrite
import asyncio
# Import JSON to read roles.json
import json
# Import Sakanya Core
from __main__ import SakanyaCore

class Stats_ReactionCounter():
  """
  EDIT: After IATGOF's server crash, Counting since 2018-09-26 19:43 JST
  Counting since 2018-03-26 11:00 JST
  """

  def __init__(self, bot):
    self.bot = bot
    try:
      with open(os.path.join(os.path.dirname(__file__), 'reactions.json'), 'r') as data_file:
        try:
          self.reactions_json = json.load(data_file)
        except ValueError as e:
          self.reactions_json = {}
    except IOError:
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
        
        with open(os.path.join(os.path.dirname(__file__), 'reactions.json'), 'w') as file:
          file.write(json.dumps(self.reactions_json, indent=2))

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
    with open(os.path.join(os.path.dirname(__file__), 'reactions.json'), 'w') as file:
      file.write(json.dumps(self.reactions_json, indent=2))
  
  async def on_reaction_remove(self, reaction, user):
    """
    Subtract one for the reaction.
    Only called on message in Saka's cache (which means messages sent after bot start)
    """
    
    # Don't count statistics if the reaction is not a server emoji
    if reaction.custom_emoji is False:
      return

    if str(reaction.emoji) in self.reactions_json:
      if self.reactions_json[str(reaction.emoji)] <= 1:
        self.reactions_json.pop(str(reaction.emoji), None)
      else:
        self.reactions_json[str(reaction.emoji)
                            ] = self.reactions_json[str(reaction.emoji)] - 1
    # Else do nothing, since 0-0 should be 0 in this case

    with open(os.path.join(os.path.dirname(__file__), 'reactions.json'), 'w') as file:
      file.write(json.dumps(self.reactions_json, indent=2))

  async def on_socket_response(self, jsonmsg):
    """
    Add/Subtract one for the reaction.
    Called for all responses, but filter out ones before cache with 'emoji' presence
    """

    if jsonmsg['t'] == 'MESSAGE_REACTION_ADD' and 'emoji' in jsonmsg['d']:

      if jsonmsg['d']['emoji']['id'] is None:
        return
      
      key = '<:' + jsonmsg['d']['emoji']['name'] + ':' + jsonmsg['d']['emoji']['id'] + '>'
      if key in self.reactions_json:
        self.reactions_json[key] = self.reactions_json[key] + 1
      else:
        self.reactions_json[key] = 1
      with open(os.path.join(os.path.dirname(__file__), 'reactions.json'), 'w') as file:
        file.write(json.dumps(self.reactions_json, indent=2))
    
    elif jsonmsg['t'] == 'MESSAGE_REACTION_REMOVE' and 'emoji' in jsonmsg['d']:

      if jsonmsg['d']['emoji']['id'] is None:
        return
      
      key = '<:' + jsonmsg['d']['emoji']['name'] + ':' + jsonmsg['d']['emoji']['id'] + '>'
      if key in self.reactions_json:
        if self.reactions_json[key] <= 1:
          self.reactions_json.pop(key, None)
        else:
          self.reactions_json[key] = self.reactions_json[key] - 1
      with open(os.path.join(os.path.dirname(__file__), 'reactions.json'), 'w') as file:
        file.write(json.dumps(self.reactions_json, indent=2))

  @commands.command(pass_context=True)
  async def reset_reactioncount(self, context, reaction=None):
    if context.message.author.id == '202501452596379648':
      asyncio.sleep(1) # Prevent bumping into on_message handlers
      resetreaction = self.reactions_json.pop(reaction, None)
      if resetreaction is not None:
        # Then overwrite the file
        with open(os.path.join(os.path.dirname(__file__), 'reactions.json'), 'w') as file:
          await self.bot.add_reaction(context.message, '✅')  # Add checkmark
    else:
      await self.bot.add_reaction(context.message, '❎')  # Add x mark

  @commands.command(pass_context=True)
  async def override_reactioncount(self, context, reaction=None, overrideCount=None):
    if context.message.author.id == '202501452596379648' and overrideCount is not None:
      self.reactions_json[reaction] = overrideCount
      await self.bot.add_reaction(context.message, '✅')
    else:
      await self.bot.add_reaction(context.message, '❎')

def setup(bot):
  bot.add_cog(Stats_ReactionCounter(bot))
