# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import Sakanya Core
from __main__ import SakanyaCore
# Import random for shuffling positions
import random
# Import copy to deep copy dictionaries
import copy
# Import sched and time
import asyncio, time


class AprilFools():

  def __init__(self, bot):
    self.bot = bot
    self.running = False
    self.original_position_local = [
      {
        'id': '344957370901856268',
        'name': 'general',
        'order': '0'
      },
      {
        'id': '364358830068596736',
        'name': 'test',
        'order': '1'
      },
      {
        'id': '428587910493765660',
        'name': 'test2',
        'order': '2'
      },
      {
        'id': '428587942324469790',
        'name': 'test3',
        'order': '3'
      },
      {
        'id': '429645984818003998',
        'name': 'test4',
        'order': '5'
      }
    ]

    self.original_position = [
      {
        'id': '319721090274295809',
        'name': 'announcements',
        'order': '0'
      },
      {
        'id': '317924870950223872',
        'name': 'general',
        'order': '1'
      },
      {
        'id': '317933848203755521',
        'name': 'programming',
        'order': '2'
      },
      {
        'id': '342686142237507584',
        'name': 'languages',
        'order': '3'
      },
      {
        'id': '320219158593667072',
        'name': 'anime',
        'order': '4'
      },
      {
        'id': '342393014985031681',
        'name': 'games',
        'order': '5'
      },
      {
        'id': '379473083267940354',
        'name': 'cooking',
        'order': '6'
      },
      {
        'id': '344362535996227585',
        'name': 'music',
        'order': '7'
      },
      {
        'id': '341874607651029003',
        'name': 'suggestions',
        'order': '9'
      },
      {
        'id': '321430399643418634',
        'name': 'bot-and-spam',
        'order': '10'
      }
    ]

  @commands.command(pass_context=True)
  async def aprilfools(self, context, control):
    """
    Control shuffling the channels every 10 minutes.
    
    Format:
      >aprilfools <start|end|pause>

    Examples:
      >aprilfools start
    """
    
    if context.message.author.id != '202501452596379648':
      await self.bot.add_reaction(context.message, '❎')  # Add x mark
      return

    #possible_controls = {
    #  'start': self.start,
    #  'end': self.end,
    #  'pause': self.pause
    #}
    possible_controls = ('start', 'end', 'pause')
    if control not in possible_controls:
      await self.bot.add_reaction(context.message, '❎')  # Add x mark
      return
    
    if control == 'start':
      if self.running is False:
        await self.bot.say('Starting April Fools...')
        self.bot.loop.create_task(self.shuffleChannels())
        self.aprilfools_context = context
        self.running = True
    elif control == 'pause':
      self.running = False
      await self.bot.say('April Fools has been paused.')
    elif control == 'end':
      self.running = False
      new_order = self.original_position
      for index, channel in enumerate(new_order):
        server_channel = context.message.server.get_channel(channel['id'])
        previous_channel = next((item for item in self.original_position.copy() if item['order'] == channel['order']), None)
        await self.bot.edit_channel(server_channel, name=previous_channel['name'])
        await self.bot.move_channel(server_channel, int(channel['order']))
      await self.bot.say('April Fools has been stopped and reset.')

  async def shuffleChannels(self):

    while not self.bot.is_closed and self.running is True:
      try:
        new_order = self.shuffleOrder()
        for index, channel in enumerate(new_order):
          server_channel = self.aprilfools_context.message.server.get_channel(channel['id'])
          previous_channel = next((item for item in self.original_position.copy() if item['order'] == channel['order']), None)
          await self.bot.edit_channel(server_channel, name=previous_channel['name'])
          await self.bot.move_channel(server_channel, int(channel['order']))
      except Exception as e:
        owner = await self.bot.get_user_info('202501452596379648')
        await self.bot.send_message(owner, content=str(e))

      await asyncio.sleep(595) # 9 minuttes 55 seconds


  def shuffleOrder(self):

    orders = [x['order'] for x in self.original_position]
    random.shuffle(orders)
    
    new_position = copy.deepcopy(self.original_position)
    for index, channel in enumerate(new_position):
      new_position[index]['order'] = orders[index]
  
    return new_position


def setup(bot):
  bot.add_cog(AprilFools(bot))
