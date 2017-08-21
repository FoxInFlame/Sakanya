# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands

class Waifu():
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def waifu(self):
    """
    Remind user that Saka is their waifu.
    
    Format:
      >waifu

    Examples:
      >waifu
    """
    await self.bot.say('...am I not your waifu any more?')

def setup(bot):
  bot.add_cog(Waifu(bot))