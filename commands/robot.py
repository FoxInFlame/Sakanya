# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import sys to import from parent directory
import sys
sys.path.append("..")
# Import Sakanya Core
from core import SakanyaCore
# Import URLlib.parse to manipulate URLs
import urllib.parse

class Robot():
  def __init__(self, bot):
    self.bot = bot

  @commands.command(pass_context=True)
  async def robot(self, context, *, text=None):
    """
    Request for the robot version of the user.
    
    Format:
      >robot [text]

    Examples:
      >robot
      >robot Motsy
    """
    if text is None: text = context.message.author.name
    await self.bot.say(content='', embed=discord.Embed(
      title = 'Robot: ' + text,
      color = SakanyaCore().embed_color,
      type = 'rich',
    ).set_image(url='https://robohash.org/' + urllib.parse.quote_plus(text))
    )

def setup(bot):
  bot.add_cog(Robot(bot))