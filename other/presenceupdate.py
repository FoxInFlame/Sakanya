# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import sys to import from parent directory
import sys
sys.path.append("..")
# Import Sakanya Core
from core import SakanyaCore
# import random for randomness (used in setting presence)
import random
# import json for JSON handling of APIs
import json
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
# Import sys to output line number of exception
import sys

class PresenceUpdate():
  def __init__(self, bot):
    self.bot = bot

  async def on_ready(self):
    self.bot.loop.create_task(self.changePresence())

  async def get_game_type_and_name(self, kaomojis, counter_kaomoji, session):
    """
    Get randomly generated game status names and types.
    Flowchart https://i.imgur.com/iHTsRMk.png
    """

    game_name = ''

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
          # nyaamusic_xml = await session.get('https://nyaa.si/?page=rss&c=2_0&f=0', headers=SakanyaCore().headers, timeout=None)
          # tree = etree.fromstring((await nyaamusic_xml.read()).decode('utf-8'))
          # game_name = re.sub("[\(\[].*?[\)\]]", "", tree.xpath('//item[1]/title/text()')[0])
          game_name = 'Music'
        elif game_type == 3:
          # Watching - you
          # Watching - random nyaa anime
          # Watching - random youtube video
          watching_type = random.randint(0, 2)
          if watching_type == 0:
            # Watching - you
            game_name = 'you'
          # elif watching_type == 1:
          #   # Watching - random nyaa anime
          #   nyaaanime_xml = await session.get('https://nyaa.si/?page=rss&c=1_2&f=0', headers=SakanyaCore().headers)
          #   tree = etree.fromstring((await nyaaanime_xml.read()).decode('utf-8'))
          #   game_name = re.sub("[\(\[].*?[\)\]]", "", tree.xpath('//item[1]/title/text()')[0])
          else:
            # Watching - random youtube video
            randomyoutube = await session.get('https://randomyoutube.net/api/getvid?api_token=***REMOVED***')
            video_id = json.loads(await randomyoutube.read())['vid']
            youtubeinformation = await session.get('https://www.googleapis.com/youtube/v3/videos?id=' + video_id + '&key=***REMOVED***&part=snippet')
            parsed = json.loads(await youtubeinformation.read())['items']
            if len(parsed) > 0:
              game_name = parsed[0]['snippet']['title']
            else:
              game_name = 'Need help? {}help'.format(SakanyaCore().prefix)

    except Exception as e:

      owner = await self.bot.get_user_info('202501452596379648')
      await self.bot.send_message(owner, 'Error while changing presence on line {}:```{}```{}'.format(sys.exc_info()[-1].tb_lineno, repr(e), 'Game type: ' + str(game_type) + (' / Watching type: ' + str(watching_type) if game_type == 3 else '') + (' / Video id: ' + video_id if game_type == 3 and watching_type == 2 else '')))
      game_type = random.randint(0, 3)
      game_name = 'Need help? {}help'.format(SakanyaCore().prefix)
    
    return (game_type, game_name, counter_kaomoji)

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
        
        game_data = await self.get_game_type_and_name(kaomojis, counter_kaomoji, session)

        counter_kaomoji = game_data[2]

        await self.bot.change_presence(game=discord.Game(name=game_data[1], type=game_data[0]), status=None, afk=False)
        await asyncio.sleep(SakanyaCore().presenceupdate_timer)

def setup(bot):
  bot.add_cog(PresenceUpdate(bot))
