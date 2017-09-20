# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import os for file system checks
import os

class FileManagement():
  def __init__(self, bot):
    self.bot = bot

  @commands.command(pass_context=True)
  async def emptyfile(self, context, filename=None):
    """
    Empty a file
    
    Format:
      >emptyfile [filename]

    Examples:
      >emptyfile nullstory.txt
    """ 
    if context.message.author.id != '202501452596379648':
      return
    if filename is None:
      await self.bot.say('A file name has to be specified.')
      return
    try: 
      file = open(filename, 'w', encoding='utf8')
      file.write('')
      file.close()
      await self.bot.say('Emptied file ' + filename)
    except Exception as e:
      await self.bot.say('Error: ' + str(e))

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
        contents = f.read()
        contents = (contents[:1800] + '...') if len(contents) > 1802 else contents
        filename_parsed, file_extension = os.path.splitext(filename)
        await self.bot.say(embed=discord.Embed(
          color = 15839636,
          title = 'File: ' + filename,
          type = 'rich',
          description = '```' + file_extension[1:] + '\n' + contents + '\n```'
        ))
    except Exception as e:
      await self.bot.say('Error: ' + str(e))
def setup(bot):
  bot.add_cog(FileManagement(bot))