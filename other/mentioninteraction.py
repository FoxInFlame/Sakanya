# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# import random for randomness
import random

class MentionInteraction():
  def __init__(self, bot):
    self.bot = bot

  async def on_message(self, message):
    """
    Interact with mentions of other bots together with Sakanya herself.
    """
    mention_sakanya = False
    mention_andre = False
    mention_kaneda = False
    mention_nekohime = False
    for user in list(message.mentions):
      if user.id == '346773965299253250': # If I'm mentioned
        mention_sakanya = True
      if user.id == '331874668719898634': # If I'm mentioned
        mention_andre = True
      if user.id == '333960965320343552': # If I'm mentioned
        mention_kaneda = True
      if user.id == '270198146020278272': # If I'm mentioned
        mention_nekohime = True
      
    if mention_sakanya == True:
      if '?' in message.content and message.author.bot == False:
        await self.bot.send_typing(message.channel)
        randomusers = random.sample(list(message.server.members), 2)
        await self.bot.send_message(message.channel, '(・・ ) ? That\'s a good question... Maybe it\'ll be wiser to ask someone smart, like {} or {}.'.format(randomusers[0].name, randomusers[1].name))
      elif '😭' in message.content:
        await self.bot.send_message(message.channel, ' ｡･ﾟ･(ﾉД`)ヽ(￣ω￣ )')
      elif mention_andre == False and mention_kaneda == False and mention_nekohime == False:
        await self.bot.send_typing(message.channel)
        chance = random.random()
        if chance > 50:
          await self.bot.send_message(message.channel, 'Um, nyani?') # 50% chance
        elif chance > 25:
          await self.bot.send_message(message.channel, '...wha!? (つ✧ω✧)つ') # 25% chance
        else:
          await self.bot.send_message(message.channel, '...(≧▽≦)/') # 25% chance
      elif mention_andre == True and mention_kaneda == False and mention_nekohime == False:
        await self.bot.send_typing(message.channel)
        await self.bot.send_message(message.channel, '...André isn\'t really my type... |д･)')
      elif mention_andre == False and mention_kaneda == True and mention_nekohime == False:
        await self.bot.send_typing(message.channel)
        await self.bot.send_message(message.channel, 'Um. Kanny.... it\'s.. it\'s not like I like you or anything!\n(⁄ ⁄>⁄ ▽ ⁄<⁄ ⁄)')
      elif mention_andre == False and mention_kaneda == False and mention_nekohime == True:
        await self.bot.send_typing(message.channel)
        await self.bot.send_message(message.channel, 'Nyaa! (\*・∀・)爻(・∀・\*)')
      elif mention_andre == True and mention_kaneda == True and mention_nekohime == True:
        await self.bot.send_typing(message.channel)
        await self.bot.send_message(message.channel, 'What did you call us all in for?')

def setup(bot):
  bot.add_cog(MentionInteraction(bot))