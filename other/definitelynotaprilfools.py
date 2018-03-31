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
# Import pretty print for debug
import pprint


class AprilFools():

  def __init__(self, bot):
    self.bot = bot
    self.running = False
    self.original_position_local = [
      {
        'id': '344957370901856268',
        'name': 'general',
        'topic': 'general goes here',
        'order': '0',
        'shuffle': False
      },
      {
        'id': '364358830068596736',
        'name': 'test',
        'topic': 'test goes here\n\ni think.',
        'order': '1',
        'shuffle': True
      },
      {
        'id': '428587910493765660',
        'name': 'test2',
        'topic': '',
        'order': '2',
        'shuffle': True
      },
      {
        'id': '428587942324469790',
        'name': 'test3',
        'topic': '',
        'order': '3',
        'shuffle': True
      },
      {
        'id': '429645923476439050',
        'name': 'channel2',
        'topic': '',
        'order': '4',
        'shuffle': False
      },
      {
        'id': '429645984818003998',
        'name': 'test4',
        'topic': '',
        'order': '5',
        'shuffle': True
      }
    ]

    self.original_position = [
      {
        'id': '319721090274295809',
        'name': 'announcements',
        'topic': '',
        'order': '0',
        'shuffle': True
      },
      {
        'id': '317924870950223872',
        'name': 'general',
        'topic': '',
        'order': '1',
        'shuffle': True
      },
      {
        'id': '317933848203755521',
        'name': 'programming',
        'topic': 'Is it not obvious? Here\'s the place to talk code.',
        'order': '2',
        'shuffle': True
      },
      {
        'id': '342686142237507584',
        'name': 'languages',
        'topic': '[No programming languages] Learn, teach, discuss, and explain language to other multilingual individuals. ;)',
        'order': '3',
        'shuffle': True
      },
      {
        'id': '320219158593667072',
        'name': 'anime',
        'topic': 'To talk about anime. Not games - there\'s #games for that.',
        'order': '4',
        'shuffle': True
      },
      {
        'id': '342393014985031681',
        'name': 'games',
        'topic': 'All about Houkai 3rd right now, but technically everything related to games (whether that be computer ones, board ones, or even outdoor ones) go here.\n\nEroge (if any) unfortunately would have to be posted in #nsfw due to obvious reasons.',
        'order': '5',
        'shuffle': True
      },
      {
        'id': '379473083267940354',
        'name': 'cooking',
        'topic': 'This channel is for showcasing some delicious meals you made and you want to show off. Also can be used to share recipes.',
        'order': '6',
        'shuffle': True
      },
      {
        'id': '344362535996227585',
        'name': 'music',
        'topic': 'For posting, discussing, and listening to music.',
        'order': '7',
        'shuffle': True
      },
      {
        'id': '342393181251436556',
        'name': 'nsfw',
        'topic': 'So apparently we really need a nsfw channel - for really lewd stuff.',
        'order': '8',
        'shuffle': False
      },
      {
        'id': '341874607651029003',
        'name': 'suggestions',
        'topic': 'For suggesting things to the Discord server, Discord bots, the MAL club, or other members.',
        'order': '9',
        'shuffle': True
      },
      {
        'id': '321430399643418634',
        'name': 'bot-and-spam',
        'topic': '',
        'order': '10',
        'shuffle': True
      },
      {
        'id': '376544021234843658',
        'name': 'admin-bot-spam',
        'topic': 'Purely for testing and sending IDs and stuff',
        'order': '11',
        'shuffle': False
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
      try:
        new_order = self.original_position
        for index, channel in enumerate(new_order):
          server_channel = context.message.server.get_channel(channel['id'])
          previous_channel = next((item for item in self.original_position.copy() if item['order'] == channel['order']), None)
          await self.bot.edit_channel(server_channel, name=previous_channel['name'], topic=previous_channel['topic'])
          await self.bot.move_channel(server_channel, int(channel['order']))
          await asyncio.sleep(0.5)
        await self.bot.say('April Fools has been stopped and reset.')
      except Exception as e:
        owner = await self.bot.get_user_info('202501452596379648')
        await self.bot.send_message(owner, content=str(e))

  async def shuffleChannels(self):

    while not self.bot.is_closed and self.running is True:
      try:
        new_order = await self.shuffleOrder()
        for index, channel in enumerate(new_order):
          server_channel = self.aprilfools_context.message.server.get_channel(channel['id'])
          previous_channel = next((item for item in self.original_position.copy() if item['order'] == channel['order']), None)
          await self.bot.edit_channel(server_channel, name=previous_channel['name'], topic=previous_channel['topic'])
          await self.bot.move_channel(server_channel, int(channel['order']))
          await asyncio.sleep(0.5)
      except Exception as e:
        owner = await self.bot.get_user_info('202501452596379648')
        await self.bot.send_message(owner, content=str(e))

      await asyncio.sleep(595) # 9 minuttes 55 seconds


  async def shuffleOrder(self):

    # orders = [x['order'] for x in self.original_position]
    shuffle_orders = [x['order'] for x in self.original_position if x['shuffle'] is True]
    random.shuffle(shuffle_orders)
    
    new_position = copy.deepcopy(self.original_position)
    count = 0
    for index, channel in enumerate(new_position):
      if new_position[index]['shuffle'] is True:
        new_position[index]['order'] = shuffle_orders[count]
        count += 1

    owner = await self.bot.get_user_info('202501452596379648')
    await self.bot.send_message(owner, content=pprint.pformat(new_position))
    return new_position


def setup(bot):
  bot.add_cog(AprilFools(bot))
