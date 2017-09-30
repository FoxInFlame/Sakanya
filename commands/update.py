# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import os and sys for a restart
import os, sys
# Import subprocess to call git
import subprocess
# Import time for sleeping
import time

class Update():
  def __init__(self, bot):
    self.bot = bot

  @commands.command(pass_context=True)
  async def update(self, context):
    """
    Update Sakanya from git. Only available to FoxInFlame.
    
    Format:
      >update

    Examples:
      >update
    """
    if context.message.author.id == '202501452596379648':
      await self.bot.add_reaction(context.message, '✅') # Add checkmark
      await self.bot.change_presence(game=discord.Game(name='Updating: Downloading...', type=0), status=None, afk=False)
      print('Pulling from git origin/master...')
      try:
        gitpull = subprocess.run(['git', 'pull', 'origin', 'master'], check=True, stdout=subprocess.PIPE, encoding='utf8')
        print('Git pull has succeeded.')
        if 'Already up-to-date.' in gitpull.stdout:
          print('However, it is already up-to-date. No need for a restart.')
          await self.bot.say('Success:\n```' + gitpull.stdout + '```No need for restart. Aborted.')
          await self.bot.change_presence(game=discord.game(name='٩(͡๏̯͡๏)۶', type=0), status=None, afk=False)
        else:
          await self.bot.say('Success:\n```' + gitpull.stdout + '```')
          await self.bot.change_presence(game=discord.Game(name='Updating: Restarting...', type=0), status=None, afk=False)
          # Git pull successful.
          print('Logging out in 3 seconds...')
          time.sleep(3) # Time to update presence 
          await self.bot.logout()
          os.execl(sys.executable, sys.executable, *sys.argv)
      except subprocess.CalledProcessError as e:
        print('Git pull has failed!')
        print(e.output)
        await self.bot.say('Sakanya ran into an error while pulling from git.\n```' + e.output + '```')
        await self.bot.change_presence(game=discord.Game(name='Updating: Download Error...', type=0), status=None, afk=False)
      except Exception as e:
        print('Git pull has failed for an unknown reason:')
        print('Line ' + str(sys.exc_info()[2].tb_lineno) + ': ' + e)
        await self.bot.say('Sakanya ran into an unexpected error while pulling from git.\n```' + e + '```')
        await self.bot.change_presence(game=discord.Game(name='Updating: Unexpected Error...', type=0), status=None, afk=False)
    else:
      await self.bot.add_reaction(context.message, '❎') # Add x mark
def setup(bot):
  bot.add_cog(Update(bot))