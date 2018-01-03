# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import Sakanya Core
from __main__ import SakanyaCore
# import random for randomness (used in setting presence)
import random
# Import asynchronous waiting 
import asyncio
# Import URLlib.parse to manipulate URLs
import urllib.parse
# Import aiohttp for asynchronous HTTP requests
import aiohttp
# Import lxml to parse XML and HTML
from lxml import etree
# Import regex to find []
import re

class PresenceUpdate():
  def __init__(self, bot):
    self.bot = bot

  async def on_ready(self):
    self.bot.loop.create_task(self.changePresence())

  async def changePresence(self):
    async with aiohttp.ClientSession() as session:
      try:
        response = await session.get('http://kaomoji.ru/en/', headers=SakanyaCore().headers)
        tree = etree.HTML((await response.read()).decode('utf8'))
        kaomojis = tree.xpath('//table[@class="table_kaomoji"]//td/span/text()')
      except Exception as e:
        print(e)
        print('Couldn\'t access kaomoji.ru.')
        kaomojis = ['Need help? {}help'.format(SakanyaCore().prefix)]

      counter_kaomoji = 0
      while not self.bot.is_closed:
        
        # Flowchart https://i.imgur.com/iHTsRMk.png

        try:
          # Random boolean
          is_help = bool(random.random() < 0.35) 
          if is_help:
            # Random game type
            game_type = random.randint(0, 3)
            game_name = 'Need help? {}help'.format(SakanyaCore().prefix)
          else:
            # Random game type
            game_type = random.choice([0, 2, 3]) # No Streaming because there's nothing yet to put as a name

            if game_type == 0:
              # Playing - random kaomoji
              if len(kaomojis) <= counter_kaomoji:
                counter_kaomoji = 0
              game_name = kaomojis[counter_kaomoji]
              counter_kaomoji += 1
            elif game_type == 2:
              # Listening to - random nyaa music
              nyaamusic_xml = await session.get('https://nyaa.si/?page=rss&c=2_0&f=0', headers=SakanyaCore().headers)
              tree = etree.fromstring((await nyaamusic_xml.read()).decode('utf-8'))
              game_name = re.sub("[\(\[].*?[\)\]]", "", tree.xpath('//item[1]/title/text()')[0])
            elif game_type == 3:
              # Watching - you
              # Watching - random nyaa anime
              is_watchingyou = bool(random.getrandbits(1))
              if is_watchingyou:
                game_name = 'you'
              else:
                nyaaanime_xml = await session.get('https://nyaa.si/?page=rss&c=1_2&f=0', headers=SakanyaCore().headers)
                tree = etree.fromstring((await nyaaanime_xml.read()).decode('utf-8'))
                game_name = re.sub("[\(\[].*?[\)\]]", "", tree.xpath('//item[1]/title/text()')[0])
        except Exception as e:
          owner = await self.bot.get_user_info('202501452596379648')
          await self.bot.send_message(owner, 'Error while changing presence:```{}```'.format(repr(e)))

        await self.bot.change_presence(game=discord.Game(name=game_name, type=game_type), status=None, afk=False)
        await asyncio.sleep(SakanyaCore().presenceupdate_timer)

def setup(bot):
  bot.add_cog(PresenceUpdate(bot))
