# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import random for randomness
import random
# Import difflib for string difference calculation
import difflib
# Import Sakanya Core
from __main__ import SakanyaCore

class Love():
  def __init__(self, bot):
    self.bot = bot

  @commands.command(pass_context=True)
  async def love(self, context, user=None):
    """
    Send one of many preconfigured love phrases to a user.
    
    Format:
      >love <username>

    Examples:
      >love FoxInFlame
    """
    if user is None:
      await self.bot.say('Try `' + SakanyaCore().prefix + 'help love`.')
      return
    if context.message.server is None:
      await self.bot.say('You can only send love to someone when you\'re in the same server as them.\no(>< )o')
      return

    member = {
      'difference': 9999999,
      'member': None
    }
    server_members = context.message.server.members
    for server_member in server_members:
      # Get the length of the number of changes needed to go from user to server_member.name
      difference = sum(1 for _ in difflib.ndiff(user, server_member.name)) # You have to sum to get the length of a generator (can't len())
      # And keep only the lowest one.
      if difference < member['difference'] and difference < 30: # 30 seems nice.
        member['difference'] = difference
        member['member'] = server_member

    if member['member'] is None:
      await self.bot.say('No one called ' + user + ' was found...\no(>< )o')
      return
    if member['member'] == context.message.server.me:
      await self.bot.say('...um. Thanks! (o^ ^o)')
      return
    if member['member'].bot == True:
      await self.bot.say('Unfortunately, normal bots can\'t feel love... So I can\'t send the love to them. (-ω-、)')
      return
    if member['member'].id == context.message.author.id:
      await self.bot.say('Awww. Sending love to yourself... ⊂(･ω･*⊂) Well, loving yourself is always good!')
    phrases = [
      'Um, {0}? I\'m really sorry to disturb you, but... I... I... I love you! --{1}',
      'I can\'t stop thinking about you {0}, I think I\'ll go mad soon! --{1}',
      '{0}, I love you, I want you to love me too. And I won\'t let you say No. --{1}',
      'Oh {0}, I don’t even want to think about what life would be like without you. --{1}',
      'Everything about you turns me on, {0}. --{1}',
      'I can’t say it enough – I love you {0}. I love you more than anything. --{1}',
      'Oh {0}, shall I compare thee to a summer\'s day? Thou art more lovely and more temperate. --{1}',
      '{0}, one half of me is yours, the other half yours,\nMine own, I would say; but if mine, then yours,\nAnd so all is yours. --{1}',
      '{0}, thou art as glorious to this night, being o\'er my head, \nAs is a wingèd messenger of heaven\nUnto the white, upturnèd, wondering eyes\nOf mortals that fall back to gaze on him\nWhen he bestrides the lazy-puffing clouds\nAnd sails upon the bosom of the air. --{1}',
      'Hi {0}, I love you --{1}',
      'I want to kiss you all over! I\'m so into smooching with you {0}! --{1}',
      'Hi {0}, I like you, like a lot. --{1}',
      'I can\'t keep it in anymore, {0}. I have a HUGE crush on you! --{1}',
      'I want to cuddle with you so bad, {0}. --{1}',
      '{0}... I\'ll love you until the day after forever. --{1}',
      '{0}... There are only two times that I want to be with you... Now and Forever. --{1}',
      'I dreamt of you last night {0}, and we were kissing and laughing. I woke up to realise that dream has already come true. --{1}'
    ]
    await self.bot.send_message(member['member'], '❤ Here\'s a love message a special someone has sent you!\n```' + random.choice(phrases).format(member['member'].name, context.message.author.name) + '```')
    await self.bot.say('Your love has been sent to ' + member['member'].name + '! (･ω<)☆')

def setup(bot):
  bot.add_cog(Love(bot))