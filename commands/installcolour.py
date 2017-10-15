# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import Sakanya Core
from __main__ import SakanyaCore
# Import os and sys for a restart
import os, sys
# Import subprocess to call pip
import subprocess

class InstallColour():
  def __init__(self, bot):
    self.bot = bot

  @commands.command(pass_context=True)
  async def installcolour(self, context):
    """
    Installs colour pip.
    
    Format:
      >update

    Examples:
      >update
    """
    old_stdout = stdout
    log_file = open("message.log", "w")
    sys.stdout = log_file
    if context.message.author.id == '202501452596379648':
      print('---------------------------------------------------')
      print(SakanyaCore().prefix + 'installcolour initiated. Beginning installation of the colour package.')
      await self.bot.add_reaction(context.message, '✅') # Add checkmark
      await self.bot.change_presence(game=discord.Game(name='Package: Downloading...', type=0), status=None, afk=False)
      try:
        gitpull = subprocess.run(['pip', 'install', 'git+https://github.com/vaab/colour'], check=True, stdout=subprocess.PIPE)
        print('Installation finished.')
        await self.bot.say('Success:\n```' + gitpull.stdout.decode('utf-8') + '```')
        await self.bot.change_presence(game=discord.game(name='٩(͡๏̯͡๏)۶', type=0), status=None, afk=False)
      except subprocess.CalledProcessError as e:
        print('Package download has failed!')
        print(e.output)
        await self.bot.say('Sakanya ran into an error while downloading the package.\n```' + e.output + '```')
        await self.bot.change_presence(game=discord.Game(name='Package: Download Error...', type=0), status=None, afk=False)
      except Exception as e:
        exc_type, exc_obj, tb = sys.exc_info()
        print('pip install has failed:\n' + exc_obj)
        print('Line ' + str(tb.tb_lineno) + ': ' + e)
        await self.bot.say('Sakanya ran into an unexpected error while downloading the package.\nLine ' + str(tb.tb_lineno) + ': ```' + e + '```')
        await self.bot.change_presence(game=discord.Game(name='Package: Unexpected Error...', type=0), status=None, afk=False)
    else:
      await self.bot.add_reaction(context.message, '❎') # Add x mark
    sys.stdout = old_stdout
    log_file.close()
def setup(bot):
  bot.add_cog(InstallColour(bot))