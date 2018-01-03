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

class PresenceUpdate():
  def __init__(self, bot):
    self.bot = bot

  custom_presences = [
    'No Poverty',
    'Zero Hunger',
    'Good Health and Well-being',
    'Quality Education',
    'Gender Equality',
    'Clean Water and Sanitation',
    'Affordable and Clean Energy',
    'Decent Work and Economic Growth',
    'Industry, Innovation and Infrastructure',
    'Reduced Inequality',
    'Sustainable Cities and Communities',
    'Responsible Consumption and Production',
    'Climate Action',
    'Life Below Water',
    'Life on Land',
    'Peace, Justice and Strong Institutions',
    'Partnerships for the Goals'
  ]

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
    counter = 0
    while not self.bot.is_closed:
      random_kaomoji = random.random()
      if random_kaomoji < 0.5:
        # 50%
        if len(kaomojis) <= counter:
          counter = 0
        kaomoji = kaomojis[counter]
        counter += 1
      elif random_kaomoji < 0.85:
        # 35%
        kaomoji = 'Need help? {}help'.format(SakanyaCore().prefix)
      else:
        # 15%
        kaomoji = random.choice(self.custom_presences)

      type = random.randint(0, 3)
      if type == 3 or type == 2:
        random_you = random.random()
        if random_you < 0.3:
          kaomoji = 'you'
      await self.bot.change_presence(game=discord.Game(name=kaomoji, type=type), status=None, afk=False)
      await asyncio.sleep(SakanyaCore().presenceupdate_timer)

def setup(bot):
  bot.add_cog(PresenceUpdate(bot))