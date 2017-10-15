# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import Sakanya Core
from __main__ import SakanyaCore

class RoleColour():
  def __init__(self, bot):
    self.bot = bot

  @commands.command(pass_context=True)
  async def sendrolecolours(self, context):
    """
    Sends the role ids and colours to FoxInFlame.
    Only available to FoxInFlame.

    Format:
      >sendrolecolours

    Examples:
      >sendrolecolours
    """

    if context.message.author.id == '202501452596379648':
      msg = ''
      print(context.message.server.roles)
      for role in context.message.server.roles:
        if role.name == '@everyone': 
          continue
        print(role)
        msg += 'Role Name: ' + role.name + '\nRole Id: ' + role.id + '\nRole Colour:' + str(role.colour.value) + '\n'
      owner = await self.bot.get_user_info('202501452596379648')
      await self.bot.send_message(owner, content=msg) 
      await self.bot.say('*DEBUG*: Sent.')

  #@commands.command(pass_context=True, aliases=['color'])
  #async def colour(self, context):
    """
    Set the colour of the user's role to what they specify.
    
    Format:
      >color|colour <hex colour>

    Examples:
      >color #ff8a65
      >colour ffddff
      >color 51ab21
    """
    
def setup(bot):
  bot.add_cog(RoleColour(bot))