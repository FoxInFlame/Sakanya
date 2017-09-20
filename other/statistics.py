# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands

class Statistics():
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

def setup(bot):
  bot.add_cog(Statistics(bot))