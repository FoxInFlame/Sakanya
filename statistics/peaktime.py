# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import time for sleeping
import time

class PeakTime():
  def __init__(self, bot):
    self.bot = bot

  async def on_message(self, message):
    """
    Add the message to the count for the hour
    """
    
def setup(bot):
  bot.add_cog(PeakTime(bot))