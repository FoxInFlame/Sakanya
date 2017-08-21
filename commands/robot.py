# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import URLlib.request for requests
import urllib.request
# Import URLlib.parse to manipulate URLs
import urllib.parse
# Import URLlib.error to handle error
import urllib.error

class Robot():
  def __init__(self, bot):
    self.bot = bot

  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

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
      color = 15839636,
      type = 'rich',
    ).set_image(url='https://robohash.org/' + urllib.parse.quote_plus(text))
    )

def setup(bot):
  bot.add_cog(Robot(bot))