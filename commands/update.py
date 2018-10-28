import os
import sys
import subprocess
import time
import discord
from discord.ext import commands
from core import SakanyaCore


class Update():
  """
  This module is no longer used and is kept for archival purposes only.
  This class provides functions for the command `>update`.
  """

  def __init__(self, bot):
    self.bot = bot

  @commands.command(pass_context=True)
  @commands.check(SakanyaCore().is_owner)
  async def update(self, context):
    """
    Update Sakanya from git. Only available to FoxInFlame.

    Format:
      >update

    Examples:
      >update
    """
    print('---------------------------------------------------')
    print(SakanyaCore().prefix + 'update initiated.')
    await self.bot.add_reaction(context.message, '✅') # Add checkmark
    await self.bot.change_presence(
        game=discord.Game(name='Updating: Downloading...', type=0),
        status=None,
        afk=False)
    print('Pulling from git origin/master...')
    try:
      gitpull = subprocess.run(
          ['git', 'pull', 'origin', 'master'],
          check=True,
          stdout=subprocess.PIPE,
          encoding='utf8')
      gitstatus = subprocess.run(
          ['git', 'status'],
          check=True,
          stdout=subprocess.PIPE,
          encoding='utf8')
      print('Git pull has succeeded.')
      if 'Already up-to-date.' in gitpull.stdout:
        print('However, it is already up-to-date. No need for a restart.')
        await self.bot.say((
            'Success:\n'
            f'```{gitpull.stdout}```\n'
            f'```Status:{gitstatus.stdout}```No need for restart. Aborted.'))
        await self.bot.change_presence(
            game=discord.Game(name='٩(͡๏̯͡๏)۶', type=0),
            status=None,
            afk=False)
      else:
        await self.bot.say((
            'Success:\n'
            f'```{gitpull.stdout}```\n'
            f'```Status:{gitstatus.stdout}```'))
        await self.bot.change_presence(
            game=discord.Game(name='Updating: Restarting...', type=0),
            status=None,
            afk=False)
        # Git pull successful.
        print('Logging out in 3 seconds...')
        time.sleep(3)  # Time to update presence
        await self.bot.logout()
        os.execl(sys.executable, sys.executable, *sys.argv)
    except subprocess.CalledProcessError as e:
      print('Git pull has failed!')
      print(e.output)
      await self.bot.say((
          'Sakanya ran into an error while pulling from git.\n'
          f'```{e.output}```'))
      await self.bot.change_presence(
          game=discord.Game(name='Updating: Download Error...', type=0),
          status=None,
          afk=False)

    except Exception as e:
      exc_type, exc_obj, tb = sys.exc_info()
      print('Git pull has failed for an unknown reason:')
      print('Line ' + str(tb.tb_lineno) + ': ' + e)
      await self.bot.say((
          'Sakanya ran into an unexpected error while pulling from git.\n'
          f'Line {str(tb.tb_lineno)}: ```{e}```'))
      await self.bot.change_presence(
          game=discord.Game(name='Updating: Unexpected Error...', type=0),
          status=None,
          afk=False)

def setup(bot):
  bot.add_cog(Update(bot))
