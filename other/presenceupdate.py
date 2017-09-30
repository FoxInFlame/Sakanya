# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import random for randomness
import random
# Import Sakanya Core
from __main__ import SakanyaCore
# import random for randomness (used in setting presence)
import random
# Import asynchronous waiting 
import asyncio
# Import URLlib.request for requests
import urllib.request
# Import URLlib.parse to manipulate URLs
import urllib.parse
# Import URLlib.error to handle error
import urllib.error
# Import lxml to parse XML and HTML
from lxml import etree

class PresenceUpdate():
  def __init__(self, bot):
    bot.loop.create_task(self.changePresence())
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

  async def changePresence(self):
    await self.bot.wait_until_ready()
    kaomoji_req = urllib.request.Request(url='http://kaomoji.ru/en/', data=None, headers=SakanyaCore().headers)
    try:
      response = urllib.request.urlopen(kaomoji_req)
      tree = etree.HTML(response.read().decode('utf8'))
      kaomojis = tree.xpath('//table[@class="table_kaomoji"]//td/span/text()')
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
      print('Couldn\'t access kaomoji.ru. Error code: ' + str(e.code), None)
      kaomojis = ['Need help? ' + SakanyaCore().prefix + 'help']
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
        kaomoji = 'Need help? ' + SakanyaCore().prefix + 'help'
      else:
        # 15%
        kaomoji = random.choice(custom_presences)

      type = 0
      if random.random() < 0.5:
        # 50% chance of streaming instead of playing
        type = 1
      await self.bot.change_presence(game=discord.Game(name=kaomoji, type=type), status=None, afk=False)
      await asyncio.sleep(900) # 15 minutes

def setup(bot):
  bot.add_cog(PresenceUpdate(bot))