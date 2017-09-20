# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands

class FindUser():
  def __init__(self, bot):
    self.bot = bot

  async def FindUser(self):
    """
    Find user by name
    
    Format:
      >restart

    Examples:
      >restart
    """
    print('testing very much find user')
def setup(bot):
  bot.add_cog(FindUser(bot))