# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import sys to import from parent directory
import sys
sys.path.append("..")
# Import Sakanya Core
from core import SakanyaCore


class GiftExchange():
  def __init__(self, bot):
    self.bot = bot

  # better than on_socket_raw_receive because it is already JSON encoded
  async def on_socket_response(self, jsonmsg):
    """
    Add user to list in message if reacted with :beer:.
    Remove user from list in message if removed :beer:.
    """
    if jsonmsg['t'] == 'MESSAGE_REACTION_ADD' and 'emoji' in jsonmsg['d'] and jsonmsg['d']['channel_id'] == '341874607651029003':
      message = await self.bot.get_message(
          self.bot.get_channel(jsonmsg['d']['channel_id']),
          jsonmsg['d']['message_id'])
      member = self.bot.get_channel(
          jsonmsg['d']['channel_id']).server.get_member(jsonmsg['d']['user_id'])
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
    Add user to list in message if reacted with :beer:.
    Remove user from list in message if removed :beer:.
    """

    if reaction.message.channel.id is not '319721090274295809':
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
      key = '<:' + jsonmsg['d']['emoji']['name'] + \
          ':' + jsonmsg['d']['emoji']['id'] + '>'
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
      key = '<:' + jsonmsg['d']['emoji']['name'] + \
          ':' + jsonmsg['d']['emoji']['id'] + '>'
      # Check existence of emoji in database
      if key in self.reactions_json:
        # If value becomes 0, remove the key altogether
        if self.reactions_json[key] <= 1:
          self.reactions_json.pop(key, None)
        else:
          self.reactions_json[key] = self.reactions_json[key] - 1
      # Set Redis Database as well
      SakanyaCore().r.set('reactions', json.dumps(self.reactions_json))


  def handleSuggestionReactionEvent(self, emoji, message, member):
    if message.channel.id == '341874607651029003':  # Double check
      upvotes = downvotes = 0  # Just setting up.
      for reaction in message.reactions:
        if reaction.emoji == '👍':
          upvotes = reaction.count - 1  # Remove Saka's vote
        if reaction.emoji == '❌':
          downvotes = reaction.count - 1  # Remove Saka's vote

      # In #suggestions
      # Check if the reaction is a green checkmark by the author (if so, mark as complete)
      if member.id == message.author.id and emoji == '✅':  # :white_check_mark:
        return (
            True,
            '✅ Wooh! The following suggestion been marked as completed by the author (' +
            (member.nick if member.nick is not None else member.name) + ')!',
            discord.Embed(
                color=SakanyaCore().embed_color,
                type='rich',
                description='❯❯ ' + message.content + '\n' +
                '(' + str(upvotes) + ' upvotes, ' +
                str(downvotes) + ' downvotes)')
        )

      # Check if the reaction is a green checkmark by FoxInFlame (if so, force mark as complete)
      elif member.id == '202501452596379648' and emoji == '✅':
        return (
            True,
            '✅ Wooh! The following suggestion been marked as completed by FoxInFlame!',
            discord.Embed(
                color=SakanyaCore().embed_color,
                type='rich',
                description='❯❯ ' + message.content + '\n' +
                '(' + str(upvotes) + ' upvotes, ' +
                str(downvotes) + ' downvotes)')
        )

      # Check if it already has an X (if so, consider deletion)
      if downvotes >= 5 and downvotes - upvotes >= 2:
        return (
            True,
            'The following suggestion has been removed due to at least 5 people thinking so.',
            discord.Embed(
                color=SakanyaCore().embed_color,
                type='rich',
                description='❯❯ ' + message.content + '\n' +
                '(' + str(upvotes) + ' upvotes, ' +
                str(downvotes) + ' downvotes)')
        )

    return (False, '')


def setup(bot):
  bot.add_cog(SuggestionControl(bot))
