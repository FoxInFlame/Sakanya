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

def setup(bot):
  bot.add_cog(Stats_ReactionCounter(bot))
