# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import os for file system checks
import os
# Import URLlib.request for requests
#import urllib.request
# Import URLlib.parse to manipulate URLs
#import urllib.parse
# Import URLlib.error to handle error
#import urllib.error

class StoryTime():
  def __init__(self, bot):
    self.bot = bot

  pasteBinDevKey = '8115a7f76471088372c96c36713f64b8'

  file = open(filename, 'w', encoding='utf8')
  file.write('')
  file.close()
  async def on_message(self, message):
    """
    Save each message in #storytime to a TXT file.
    """
    if message.channel.id == '350204559089467393':
      filename = 'nullstory.txt'
      if os.path.exists(filename):
        append_write_flag = 'a'
      else: 
        append_write_flag = 'w'
      file = open(filename, append_write_flag, encoding='utf8')
      file.write('\t' + message.author.name + ': ' + message.content.rstrip() + '\n')
      file.close()

#  @commands.command()
#  async def readstory(self):
#    """
#    Paste the story to a PasteBin and send the link.
#    
#    Format:
#      >readstory
#
#    Examples:
#      >readstory
#    """
#    filename = 'nullstory.txt'
#    if os.path.exists(filename) is False:
#      await self.bot.say(embed=discord.Embed(
#        color = 15839636,
#        type = 'rich',
#        description = 'The file containing the story could not be found on the system.'
#      ))
#      return
#    else:
#      with open(filename) as f:
#        print('opened')
#        request = urllib.request.Request(url='https://pastebin.com/api/api_post.php', data=urllib.parse.quote_plus({
#          'api_option': 'paste',
#          'api_user_key': '',
#          'api_paste_private': '1',
#          'api_paste_name': 'Nullified Story',
#          'api_paste_expire_date': '1D',
#          'api_dev_key': self.pasteBinDevKey,
#          'api_paste_code': f.read()
#        }))
#        try:
#          print('try')
#          response = urllib.request.urlopen(request)
#          print(response)
#          await self.bot.say(embed=discord.Embed(
#            color = 15839636,
#            type = 'rich',
#            description = 'Here you go: ' + response.read()
#          ))
#        except (urllib.error.HTTPError, urllib.error.URLError) as e:
#          print('except')
#          await self.bot.say(embed=discord.Embed(
#            color = 15839636,
#            type = 'rich',
#            description = 'Sakanya ran into a problem while posting to PasteBin:\n```' + str(e) + '```'
#          ))

def setup(bot):
  bot.add_cog(StoryTime(bot))