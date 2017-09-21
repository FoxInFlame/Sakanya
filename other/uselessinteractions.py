# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import time for sleeping
import time

class UselessInteractions():
  def __init__(self, bot):
    self.bot = bot

  async def on_message(self, message):
    """
    Just a couple jokes :)
    """
    if 'n:shrug' in message.content:
      # Come on Xaetral, add it!
      await self.bot.send_message(message.channel, embed=discord.Embed(
        color = 15839636,
        type = 'rich',
        description = 'Come on <@226457042171330560>, add it!'
      ).set_image(url='https://i.imgur.com/bkNyHTT.png'))
    if 'n:cry' in message.content:
      # Come on Xaetral, add it!
      await self.bot.send_message(message.channel, embed=discord.Embed(
        color = 15839636,
        type = 'rich',
        description = 'Come on <@226457042171330560>, add it!'
      ).set_image(url='https://i.imgur.com/2jgzYuP.jpg'))
    if 'n:motherofgod' in message.content:
      # Come on Xaetral, add it!
      await self.bot.send_message(message.channel, embed=discord.Embed(
        color= 15839636,
        type = 'rich',
        description = 'Come on <@226457042171330560>, add it!'
      ).set_image(url='https://emoji.slack-edge.com/T1FLD7YUB/motherofgod/c3e5d235c08ea041.png'))
    if 'n:emotes' in message.content:
      # Come on Xaetral, add it!
      time.sleep(1) # Time to update presence 
      await self.bot.send_message(message.channel, embed=discord.Embed(
        color = 15839636,
        type = 'rich',
        title = 'Extra available emotes',
        description = 'Type `n:` followed by the name (`n:shrug` for example).\nThey will be replaced with the corresponding extra image. “ψ(｀∇´)ψ '
      ).set_image(url='https://i.imgur.com/j5QIz4l.png'))
    if message.author.id == '331874668719898634' and message.content == 'I\'m sorry, I don\'t know who Motsy is. There is no member called Motsy here. Please enter the name of someone who exists.':
      await self.bot.send_message(message.channel, 'But Motsy exists, and we all know it! It\'s just you, André, who is trying to deny the actual fact and face away from the truth.')
def setup(bot):
  bot.add_cog(UselessInteractions(bot))