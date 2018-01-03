# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import os to use relative file names
import os
# Import JSON to read roles.json
import json
# Import matplotlib to plot stuff
import matplotlib
# Force matplotlib to not use any XWindows backend (removing will result in "no $display environment variable" error)
matplotlib.use('Agg') 
import matplotlib.pyplot as plot
# Import ticker to set ticks to integer
from matplotlib.ticker import MaxNLocator
# Import asynchronous waiting
import asyncio
# Import Sakanya Core
from __main__ import SakanyaCore

class Stats():
  
  def __init__(self, bot):
    self.bot = bot
    ax = plot.figure().gca()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

  async def updateProgressBar(self, message, percentage, comment=''):
    """
    Update the progress bar message with a cute little kaomoji.
    """
    await self.bot.send_typing(message.channel)
    if message is None: return
    if percentage == 100:
      await self.bot.delete_message(message=message)
      return
    outoften = round(percentage / 10)
    #await self.bot.edit_message(message=message, new_content='`' + ('__' * outoften)[:-1] + 'φ(．．) ' + comment + '`')
    await self.bot.edit_message(message=message, new_content='`' + ('__' * outoften) + 'φ(．．) ' + comment + '`')


  async def loadStatFile(self, statfilename):
    try:
      with open(os.path.join(os.path.join(os.path.join(os.path.dirname(__file__), '..'), 'stats'), statfilename), 'r') as data_file:
        try:
          data = json.load(data_file)
          return data
        except ValueError as e:
          return {}
    except IOError:
      return {}

  @commands.command(pass_context=True)
  async def stats(self, context, argument=None):
    if argument is None:
      await self.bot.say('Try `' + SakanyaCore().prefix + 'help stats`.')
      return
    if argument == 'messages_byusers':
      tmpmsg = await self.bot.send_message(context.message.channel, 'Generating chart...')
      progressmsg = await self.bot.say('`φ(．．)`')
      data = await self.loadStatFile('authors.json')
      await self.updateProgressBar(progressmsg, 20)
      graph_data = {}
      for count, (key, value) in enumerate(list(data.items()), 1):
        if isinstance(value, int):
          continue
        if value["bot"] is False:
          graph_data[value["name"]] = value["count"]
          await self.updateProgressBar(progressmsg, 20 + (50 / len(data) * count), 'Analysing ' + value["name"])
      if(len(graph_data) == 0):
        await self.bot.send_message(context.message.channel, 'Data malformed...')
        return
      plot.bar(range(len(graph_data)), graph_data.values(), align='center')
      plot.xticks(range(len(graph_data)), list(graph_data.keys()), rotation='vertical')
      plot.margins(0.08)
      plot.title('Messages sent by users')
      plot.tight_layout()
      #plot.subplots_adjust(top=0.09) # Bottom is 0.1 by default, and top cannot be >= to bottom
      location = os.path.join(os.path.join(os.path.join(os.path.dirname(__file__), '..'), 'stats'), 'tmp.png')
    elif argument == 'messages_bybots':
      tmpmsg = await self.bot.send_message(context.message.channel, 'Generating chart...')
      progressmsg = await self.bot.say('`φ(．．)`')
      data = await self.loadStatFile('authors.json')
      await self.updateProgressBar(progressmsg, 20)
      graph_data = {}
      for count, (key, value) in enumerate(list(data.items()), 1):
        if isinstance(value, int):
          continue
        if value["bot"] is True:
          graph_data[value["name"]] = value["count"]
          await self.updateProgressBar(progressmsg, 20 + (50 / len(data) * count), 'Analysing ' + value["name"])
      if(len(graph_data) == 0):
        await self.bot.send_message(context.message.channel, 'Data malformed...')
        return
      plot.bar(range(len(graph_data)), graph_data.values(), align='center')
      plot.xticks(range(len(graph_data)), list(graph_data.keys()), rotation='vertical')
      plot.margins(0.08)
      plot.title('Messages sent by bots')
      plot.tight_layout()
      #plot.subplots_adjust(top=0.09) # Bottom is 0.1 by default, and top cannot be >= to bottom
      location = os.path.join(os.path.join(os.path.join(os.path.dirname(__file__), '..'), 'stats'), 'tmp.png')
    elif argument == 'messages_byeveryone':
      tmpmsg = await self.bot.send_message(context.message.channel, 'Generating chart...')
      progressmsg = await self.bot.say('`φ(．．)`')
      data = await self.loadStatFile('authors.json')
      await self.updateProgressBar(progressmsg, 20)
      graph_data = {}
      for count, (key, value) in enumerate(list(data.items()), 1):
        if isinstance(value, int):
          continue
        graph_data[value["name"]] = value["count"]
        await self.updateProgressBar(progressmsg, 20 + (50 / len(data) * count), 'Analysing ' + value["name"])
        await asyncio.sleep(1)
      if(len(graph_data) == 0):
        await self.bot.send_message(context.message.channel, 'Data malformed...')
        return
      plot.bar(range(len(graph_data)), graph_data.values(), align='center')
      plot.xticks(range(len(graph_data)), list(graph_data.keys()), rotation='vertical')
      plot.margins(0.08)
      plot.title('Messages sent by everyone')
      plot.tight_layout()
      #plot.subplots_adjust(top=0.09) # Bottom is 0.1 by default, and top cannot be >= to bottom
      location = os.path.join(os.path.join(os.path.join(os.path.dirname(__file__), '..'), 'stats'), 'tmp.png')
    else:
      await self.bot.send_message(context.message.channel, 'Statistics for `' + argument + '` could not be found within me...')
      return

    await self.updateProgressBar(progressmsg, 80)
    plot.savefig(location)
    plot.close("all")
    await self.updateProgressBar(progressmsg, 100)
    await self.bot.delete_message(tmpmsg)

    await self.bot.send_file(context.message.channel, location)

  
def setup(bot):
  bot.add_cog(Stats(bot))
