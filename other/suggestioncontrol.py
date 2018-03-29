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
    if jsonmsg['t'] == 'MESSAGE_REACTION_ADD' and 'emoji' in jsonmsg['d'] and jsonmsg['d']['channel_id'] == '341874607651029003':
      message = await self.bot.get_message(
        self.bot.get_channel(jsonmsg['d']['channel_id']),
        jsonmsg['d']['message_id'])
      member = self.bot.get_channel(jsonmsg['d']['channel_id']).server.get_member(jsonmsg['d']['user_id'])
      emoji = jsonmsg['d']['emoji']['name']
      message_data = self.handleSuggestionReactionEvent(emoji, message, member)
      if message_data[0] is True:
        await self.bot.send_message(
          self.bot.get_channel('317924870950223872'),
          message_data[1],
          embed=message_data[2])
        await self.bot.delete_message(message)

  async def on_reaction_add(self, reaction, user):
    """
    Woo.
    """
    if reaction.message.channel.id == '341874607651029003':
      message_data = self.handleSuggestionReactionEvent(str(reaction.emoji), reaction.message, user)
      if message_data[0] is True:
        await self.bot.send_message(
          self.bot.get_channel('317924870950223872'),
          message_data[1],
          embed=message_data[2])
        await self.bot.delete_message(reaction.message)

  def handleSuggestionReactionEvent(self, emoji, message, member):
    if message.channel.id == '341874607651029003': # Double check
      upvotes = 0
      downvotes = 0
      for reaction in message.reactions:
        if reaction.emoji == '👍':
          upvotes = reaction.count
        if reaction.emoji == '❌':
          downvotes = reaction.count
    
      # In #suggestions
      # Check if the reaction is a green checkmark by the author (if so, mark as complete)
      if member.id == message.author.id and emoji == '✅': #:white_check_mark:
        return (
          True,
          '✅ Wooh! The following suggestion been marked as completed by the author (' +
          (member.nick if member.nick is not None else member.name) + ')!',
          discord.Embed(
            color = SakanyaCore().embed_color,
            type = 'rich',
            description = '❯❯ ' + message.content + '\n' +
            '(' + str(upvotes) + ' upvotes, ' + 
            str(downvotes) + ' downvotes)')
        )

      # Check if the reaction is a green checkmark by FoxInFlame (if so, force mark as complete)
      elif member.id == '202501452596379648' and emoji == '✅':
        return (
          True,
          '✅ Wooh! The following suggestion been marked as completed by FoxInFlame!',
          discord.Embed(
            color = SakanyaCore().embed_color,
            type = 'rich',
            description = '❯❯ ' + message.content + '\n' +
            '(' + str(upvotes) + ' upvotes, ' +
            str(downvotes) + ' downvotes)')
        )

      # Check if it already has an X (if so, consider deletion)
      if downvotes >= 5 and if downvotes - upvotes >= 2:
        return (
          True,
          'The following suggestion has been removed due to at least 5 people thinking so.',
          discord.Embed(
            color = SakanyaCore().embed_color,
            type = 'rich',
            description = '❯❯ ' + message.content + '\n' +
            '(' + str(upvotes) + ' upvotes, ' + 
            str(downvotes) + ' downvotes)')
        )
      
    return (False, '')
      
          
def setup(bot):
  bot.add_cog(SuggestionControl(bot))
