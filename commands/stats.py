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
# Say, "the default sans-serif font is COMIC SANS"
matplotlib.rcParams['font.sans-serif'] = "Osaka"
# Then, "ALWAYS use sans-serif fonts"
matplotlib.rcParams['font.family'] = "sans-serif"

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
    #await self.bot.send_message(context.message.author, "\n".join(sorted(set([f.name for f in matplotlib.font_manager.fontManager.ttflist]))))
    if argument is None:
      await self.bot.say('Try `' + SakanyaCore().prefix + 'help stats`.')
      return
    

    embed = discord.Embed(
      color = SakanyaCore().embed_color,
      type = 'rich'
    ).set_author(name='🐟 Statistics', url=discord.Embed.Empty, icon_url=discord.Embed.Empty)

    if argument == 'messages_byusers':

      data = await self.loadStatFile('authors.json')
      graph_data = {}
      total_messages = 0
      for count, (key, value) in enumerate(list(data.items()), 1):
        if not isinstance(value, int) and value['bot'] is False:
          total_messages += value['count']
          graph_data[value['name']] = value['count']
      if not graph_data:
        await self.bot.send_message(context.message.channel, 'Data malformed...')
        return

      embed_graph = ''

      for item in sorted(graph_data, key=str.lower):
        embed_graph += '**' + item + '**: ' + str(graph_data[item]) + \
        ' (' + "%.2f" % round(graph_data[item] / total_messages * 100, 2) + '%)' + '\n'

      embed.add_field(name='❯ Messages sent by users',
                      value=embed_graph, inline=False)
        
    elif argument == 'messages_bybots':

      data = await self.loadStatFile('authors.json')
      graph_data = {}
      total_messages = 0
      for count, (key, value) in enumerate(list(data.items()), 1):
        if not isinstance(value, int) and value['bot'] is True:
          total_messages += value['count']
          graph_data[value['name']] = value['count']
      if not graph_data:
        await self.bot.send_message(context.message.channel, 'Data malformed...')
        return

      embed_graph = ''

      for item in sorted(graph_data, key=str.lower):
        embed_graph += '**' + item + '**: ' + str(graph_data[item]) + \
        ' (' + "%.2f" % round(graph_data[item] / total_messages * 100, 2) + '%)' + '\n'

      embed.add_field(name='❯ Messages sent by bots',
                      value=embed_graph, inline=False)
        
    elif argument == 'messages_byeveryone':

      data = await self.loadStatFile('authors.json')
      graph_data = {}
      total_messages = 0
      for count, (key, value) in enumerate(list(data.items()), 1):
        if not isinstance(value, int):
          total_messages += value['count']
          graph_data[value['name']] = value['count']
      if not graph_data:
        await self.bot.send_message(context.message.channel, 'Data malformed...')
        return

      embed_graph = ''

      for item in sorted(graph_data, key=str.lower):
        embed_graph += '**' + item + '**: ' + str(graph_data[item]) + \
        ' (' + "%.2f" % round(graph_data[item] / total_messages * 100, 2) + '%)' + '\n'

      embed.add_field(name='❯ Messages sent by everyone',
                      value=embed_graph, inline=False)

    else:
      await self.bot.send_message(context.message.channel, 'Statistics for `' + argument + '` could not be found within me...')
      return
    
    await self.bot.send_message(context.message.channel, embed=embed)
  
def setup(bot):
  bot.add_cog(Stats(bot))
