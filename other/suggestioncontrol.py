# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import Sakanya Core
from __main__ import SakanyaCore

class SuggestionControl():
  def __init__(self, bot):
    self.bot = bot

  async def on_message(self, message):
    """
    Automatically add checkmark and xmark to any new suggestions.
    """
    if message.channel.id == '341874607651029003':
      await self.bot.add_reaction(message, '👍') # thumbsup
      await self.bot.add_reaction(message, '❌') # x

  async def on_socket_response(self, jsonmsg): # better than on_socket_raw_receive because it is already JSON encoded
    """
    Delete messages in #suggestions if they have at least 5 Xs
    """
    if jsonmsg['t'] == 'MESSAGE_REACTION_ADD':
      message = await self.bot.get_message(self.bot.get_channel(jsonmsg['d']['channel_id']), jsonmsg['d']['message_id'])
  
      if jsonmsg['d']['channel_id'] == '341874607651029003':
        # In #suggestions
        # Check if it already has an X (if so, delete)
        users = await self.bot.get_reaction_users(discord.Reaction(message=message, emoji='❌')) # A big fat X
        if len(users) >= 5: # Just in case it's really fast and it went over 5
          await self.bot.send_message(self.bot.get_channel('317924870950223872'), 'The following suggestion has been removed due to at least 5 people voting so.', embed=discord.Embed(
            color = SakanyaCore().embed_color,
            type = 'rich',
            description = '>> ' + message.content
          ))
          await self.bot.delete_message(message)

def setup(bot):
  bot.add_cog(SuggestionControl(bot))