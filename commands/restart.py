# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import os and sys for a restart
import os, sys

class Restart():
  def __init__(self, bot):
    self.bot = bot

  @commands.command(pass_context=True)
  async def restart(self, context):
    """
    Restart Sakanya. Only available to FoxInFlame.
    
    Format:
      >restart

    Examples:
      >restart
    """
    print('A restart was attempted by id ' + str(context.message.author.id))
    if context.message.author.id == '202501452596379648':
      await self.bot.add_reaction(context.message, '✅') # Add checkmark
      print('Accepted. Restarting...')
      await self.bot.change_presence(game=discord.Game(name='Restarting: Restarting...', type=0), status=None, afk=False)
      await self.bot.logout()
      os.execl(sys.executable, sys.executable, *sys.argv)
def setup(bot):
  bot.add_cog(Restart(bot))