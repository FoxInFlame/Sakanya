# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import sys to import from parent directory
import sys
sys.path.append("..")
# Import Sakanya Core
from core import SakanyaCore

class Modules():
  def __init__(self, bot):
    self.bot = bot

  @commands.command(pass_context=True)
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
        color = SakanyaCore().embed_color,
        type = 'rich',
        title = 'Loaded modules',
        description = '· `' + ('`\n· `'.join(tuple(self.bot.extensions))) + '`'
      ))
      return
    
    if (action != "enable" and action != "disable") or moduleName is None:
      await self.bot.say('Wrong usage. Check source code.')
      return
 
    if action == "enable":
      try:
        self.bot.load_extension(moduleName)
      except (AttributeError, ImportError) as e:
        await self.bot.say("Failed to enable extension `{0}`\n{1}: {2}".format(moduleName, type(e).__name__, str(e)))
        return
      await self.bot.say("`{}` has been enabled.".format(moduleName))
      return
    elif action == "disable":
      if moduleName in tuple(self.bot.extensions):
        self.bot.unload_extension(moduleName)
      else:
        await self.bot.say("Failed to disable extension `{}`\nExtension does not exist.".format(moduleName))
        return
      await self.bot.say("`{}` has been disabled.".format(moduleName))

def setup(bot):
  bot.add_cog(Modules(bot))