# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import Sakanya Core
from __main__ import SakanyaCore
# Import time for sleeping
import time

class UselessInteractions():
  def __init__(self, bot):
    self.bot = bot

  #async def on_message(self, message):
    """
    Just a couple jokes :)
    None right now, but if there's going to be any, it'll be in here.
    """
    
def setup(bot):
  bot.add_cog(UselessInteractions(bot))