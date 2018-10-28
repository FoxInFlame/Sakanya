import discord
from discord.ext import commands
from core import SakanyaCore

class AddReaction():
  """
  Forces Sakanya to react to a specified message.
  This was used once to try to rig elections :)
  """
  def __init__(self, bot):
    self.bot = bot

  @commands.command(pass_context=True)
  @commands.check(SakanyaCore().is_owner)
  async def addreaction(self, context, channel_id=None, message_id=None, reaction=None):
    """
    Add a reaction to the specified message. Only available to FoxInFlame.
    
    Format:
      >addreaction <channel_id> <message_id> <reaction>

    Examples:
      >addreaction 418558526827266070 419691101826580490 :two:
    """
    if context.message.author.id == '202501452596379648':
      await self.bot.add_reaction(context.message, '✅') # Add checkmark
      try:
        message = await self.bot.get_message(discord.Object(channel_id), message_id)
        await self.bot.add_reaction(message, reaction)
      except Exception as e:
        owner = await self.bot.get_user_info('202501452596379648')
        await self.bot.send_message(owner, content=f'Could not react to the message: {str(e)}')
    else:
      await self.bot.add_reaction(context.message, '❌')

def setup(bot):
  bot.add_cog(AddReaction(bot))
