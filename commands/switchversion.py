# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import os and sys for a restart
import os, sys
# Import subprocess to call git
import subprocess

class SwitchVersion():
  def __init__(self, bot):
    self.bot = bot

  @commands.command(pass_context=True)
  async def switchversion(self, context, tag=None):
    """
    Switch Sakanya Versions. Only available to FoxInFlame.
    
    Format:
      >switchversion <tag|'master'>

    Examples:
      >switchversion
      >switchversion 1.0.2
    """
    if context.message.author.id == '202501452596379648':
      if tag is None:
        await self.bot.add_reaction(context.message, '❎') # Add x mark
        return
      await self.bot.add_reaction(context.message, '✅') # Add checkmark
      await bot.change_presence(game=discord.Game(name='Updating: Phase 1...', type=0), status=None, afk=False)
      print('Switching Versions...')
      try:
        gitpull = subprocess.run('git pull origin master', check=True, stdout=PIPE)
        await bot.change_presence(game=discord.Game(name='Updating: Phase 2...', type=0), status=None, afk=False)
        # Git pull successful.
        try:
          switchtag = subprocess.run('git checkout ' + tag, check=True, stdout=PIPE)
          await bot.change_presence(game=discord.Game(name='Updating: Restarting...', type=0), status=None, afk=False)
          # Checkout succeeded
          await self.bot.logout()
          os.execl(sys.executable, sys.executable, *sys.argv)
        except subprocess.CalledProcessError as e:
          await self.bot.say('Saknya ran into an error while switching tags.\n````' + e.output + '```')
        await bot.change_presence(game=discord.Game(name='Updating: Error in phase 2...', type=0), status=None, afk=False)
        # It will change to an emoji automatically in less than 15 minutes, so leave the status like that.
      except subprocess.CalledProcessError as e:
        await self.bot.say('Sakanya ran into an error while pulling from git.\n```' + e.output + '```')
        await bot.change_presence(game=discord.Game(name='Updating: Error in phase 1...', type=0), status=None, afk=False)

def setup(bot):
  bot.add_cog(SwitchVersion(bot))