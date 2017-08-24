# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import os for file system checks
import os

class ReadFile():
  def __init__(self, bot):
    self.bot = bot

  @commands.command(pass_context=True)
  async def readfile(self, context, filename=None):
    """
    Read a file
    
    Format:
      >readfile [filename]

    Examples:
      >readfile nullstory.txt
    """
    if context.message.author.id != '202501452596379648':
      return
    if filename is None:
      await self.bot.say('A file name has to be specified.')
      return
    try: 
      with open(filename, encoding='utf8') as f:
        contents = (f.read()[:1800] + '...') if len(f.read()) > 1802 else f.read()
        filename_parsed, file_extension = os.path.splitext(filename)
        await self.bot.say(embed=discord.Embed(
          color = 15839636,
          title = 'File: ' + filename_parsed,
          type = 'rich',
          description = '```' + file_extension[1:] + '\n' + contents + '\n```'
        ))
    except Exception as e:
      await self.bot.say('Error: ' + str(e))
def setup(bot):
  bot.add_cog(ReadFile(bot))