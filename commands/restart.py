import os
import sys
import discord
from discord.ext import commands
from core import SakanyaCore


class Restart():
  """
  This class provides functions for the command `>restart`.
  """

  def __init__(self, bot):
    self.bot = bot

  @commands.command(pass_context=True)
  @commands.check(SakanyaCore().is_owner)
  async def restart(self, context):
    """
    Restart Sakanya. Only available to FoxInFlame.

    Format:
      >restart

    Examples:
      >restart
    """
    await self.bot.add_reaction(context.message, '✅') # Add checkmark
    print('Accepted. Restarting...')
    await self.bot.change_presence(game=discord.Game(
        name='Restarting: Restarting...',
        type=0
    ), status=None, afk=False)
    await self.bot.logout()
    os.execl(sys.executable, sys.executable, *sys.argv)

def setup(bot):
  bot.add_cog(Restart(bot))
