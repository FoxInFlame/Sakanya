# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import time for ping time
import time
# Import Sakanya Core
from __main__ import SakanyaCore

class Ping():
  def __init__(self, bot):
    self.bot = bot

  @commands.command(pass_context=True)
  async def ping(self, context):
    """
    Ping the Discord server and see the time.
    
    Format:
      >ping

    Examples:
      >ping
    """
    channel = context.message.channel
    time1 = time.perf_counter()
    await self.bot.send_typing(channel)
    time2 = time.perf_counter()
    await self.bot.say('Ping: {0}ms'.format(round((time2 - time1) * 1000)))

def setup(bot):
  bot.add_cog(Ping(bot))