import discord
from discord.ext import commands
from core import SakanyaCore


class Modules():
  """
  This class provides functions for the command `>modules`.
  """

  def __init__(self, bot):
    self.bot = bot

  @commands.command(pass_context=True)
  @commands.check(SakanyaCore().is_admin)
  async def modules(self, context, action=None, moduleName=None):
    """
    List, enable or disable modules.

    Format:
      >modules [enable|disable] [modulename]

    Examples:
      >modules
      >modules enable commands.help
      >modules disable stats.lastactivity
    """

    if context.message.author.id == '202501452596379648':
      await self.bot.add_reaction(context.message, '✅') # Add checkmark
    else:
      return

    if action is None:
      await self.bot.say(embed=discord.Embed(
          color=SakanyaCore().embed_color,
          type='rich',
          title='Loaded modules',
          description='· `' + ('`\n· `'.join(tuple(self.bot.extensions))) + '`'
      ))
      return

    if (action != 'enable' and action != 'disable') or moduleName is None:
      await self.bot.say('Wrong usage. Check source code.')
      return

    if action == 'enable':
      try:
        self.bot.load_extension(moduleName)
      except (AttributeError, ImportError) as e:
        await self.bot.say((
            f'Failed to enable extension `{moduleName}`\n'
            f'{type(e).__name__}: {str(e)}'))
        return
      await self.bot.say(f'`{moduleName}` has been enabled.')
      return

    elif action == 'disable':
      if moduleName in tuple(self.bot.extensions):
        self.bot.unload_extension(moduleName)
      else:
        await self.bot.say(f'Failed to disable extension `{moduleName}`\nExtension does not exist.')
        return
      await self.bot.say(f'`{moduleName}` has been disabled.')

def setup(bot):
  bot.add_cog(Modules(bot))
