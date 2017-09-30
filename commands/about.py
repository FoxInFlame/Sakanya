# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import glob to look through the files
import glob
# Import datetime to find the age
from datetime import datetime
# Import Sakanya Core
from __main__ import SakanyaCore

class About():
  def get_lines(self):
    files = glob.glob('./**/*.py', recursive=True)

    line_count = 0
    char_count = 0
    for file in files:
      with open(file, encoding="utf8") as f:
        for line in f:
          if line.rstrip(): # If not empty line
            line_count += 1
            char_count += len(line)
    return len(files), line_count, char_count

  def __init__(self, bot):
    self.bot = bot
    filestats = self.get_lines()
    self.files = filestats[0]
    self.lines = filestats[1]
    self.chars = filestats[2]

  @commands.command()
  async def about(self):
    """
    Show the about message for Sakanya.
    
    Format:
      >about

    Examples:
      >about
    """
    # Time
    now = datetime.now()
    then = datetime(2017, 8, 14, 23, 59, 0, 0) # Checked with André welcome message timestamp
    timediff = now - then
    await self.bot.say(embed=discord.Embed(
      color = SakanyaCore().embed_color,
      type = 'rich',
      description = '*Sakanya sakanya sakanya~~~~*\nNice to meet you! I\'m Sakanya.'
    )
    .set_author(name='🐟 Profile: ' + SakanyCore().name, url=discord.Embed.Empty, icon_url=discord.Embed.Empty)
    .set_thumbnail(url='https://i.imgur.com/ARHTNkU.png')
    .add_field(name='About', value='Version: **' + SakanyaCore().version + '**\n\n' + SakanyaCore().self_introduction, inline=False)
    .add_field(name='Name Origin', value='The first goal for me was to reverse image search a lot of ~~lewd~~ pictures o(>ω<)o. "Reverse" in Japanese is 逆, which is read as Saka (or Gyaku). Since my favourite animal is a cat, I am now called as Saka*nya*.', inline=False)
    .add_field(name='Stats', value=str(self.chars) + ' characters, ' + str(self.lines) + ' lines in length\nSpread across ' + str(self.files) + ' files\n%d day(s) and %d hour(s)' % (timediff.days, timediff.seconds / 3600) + ' old')
    )

def setup(bot):
  bot.add_cog(About(bot))