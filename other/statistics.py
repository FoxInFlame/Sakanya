# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands

class Statistics():
  def __init__(self, bot):
    self.bot = bot

  async def on_message(self, message):
    """
    Just a joke. Come on Xaetral, add it!
    """
    if 'n:shrug' in message.content:
      await self.bot.say(embed=discord.Embed(
        color = 15839636,
        type = 'rich'
      ).set_image('https://i.imgur.com/bkNyHTT.png'))

def setup(bot):
  bot.add_cog(Statistics(bot))