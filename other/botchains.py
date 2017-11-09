# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import Sakanya Core
from __main__ import SakanyaCore

class BotChains():
  def __init__(self, bot):
    self.bot = bot

  @commands.command(pass_context=True)
  async def hello(self, context):
    """
    Part of a bot chain - Sends message to n:hello.
    
    Format:
      >hello

    Examples:
      >hello
    """
    await self.bot.say('n:hello')

def setup(bot):
  bot.add_cog(BotChains(bot))