# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import regexp
import re
# Import Sakanya Core
from __main__ import SakanyaCore

class BotChains():
  def __init__(self, bot):
    self.bot = bot
    #self.times = 3
  
  async def on_message(self, message):
    """
    Handle MAL links for Andre and BobDono
    """
    if message.server is not None and message.server.id == '317924870950223872':
      try:
        # Anime Links
        resultanime = re.search(r'https://myanimelist.net/anime/([0-9]+?)/', message.content).group(1)
        if resultanime is not None:
          await self.bot.send_message(message.channel, '!anime ' + resultanime)
      except:
        pass
      try:
        # Manga Links
        resultmanga = re.search(r'https://myanimelist.net/manga/([0-9]+?)/', message.content).group(1)
        if resultmanga is not None:
          await self.bot.send_message(message.channel, '!manga ' + resultmanga)
      except:
        pass
      try:
        # Character Links
        resultcharacter = re.search(
            r'https://myanimelist.net/character/([0-9]+?)/', message.content).group(1)
        if resultcharacter is not None:
          await self.bot.send_message(message.channel, 'b/character ' + resultcharacter)
      except:
        pass
        
  @commands.command(pass_context=True, aliases=['poke', 'hello'])
  async def chain(self, context):
    """
    Part of a bot chain - Sends message to n:hello.
    
    Format:
      >hello

    Examples:
      >hello
    """
    await self.bot.say('n:hello')


def setup(bot):
  bot.add_cog(BotChains(bot))
