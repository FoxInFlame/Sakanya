# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands

class AddReaction():
  def __init__(self, bot):
    self.bot = bot

  @commands.command(pass_context=True)
  async def addreaction(self, context, channelid=None, messageid=None, reaction=None):
    """
    Add a reaction to the specified message. Only available to FoxInFlame.
    
    Format:
      >restart

    Examples:
      >restart
    """
    if context.message.author.id == '202501452596379648':
      await self.bot.add_reaction(context.message, '✅') # Add checkmark
      try:
        message = await self.bot.get_message(discord.Object(channelid), messageid)
        await self.bot.add_reaction(message, reaction)
      except Exception as e:
        owner = await bot.get_user_info('202501452596379648')
        await bot.send_message(owner, content='Could not react to the message: ' + str(e))
    else:
      await self.bot.add_reaction(context.message, '❌');
def setup(bot):
  bot.add_cog(AddReaction(bot))