# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import os to use relative file names
import os
# Import JSON to read roles.json
import json
# Import matplotlib to plot stuff
# import matplotlib
# Force matplotlib to not use any XWindows backend (removing will result in "no $display environment variable" error)
# matplotlib.use('Agg') 
# Say, "the default sans-serif font is COMIC SANS"
# matplotlib.rcParams['font.sans-serif'] = "Osaka"
# Then, "ALWAYS use sans-serif fonts"
# matplotlib.rcParams['font.family'] = "sans-serif"

# import matplotlib.pyplot as plot
# Import ticker to set ticks to integer
# from matplotlib.ticker import MaxNLocator
# Import operator to use on getting values while sorting dictionaries by value
import operator
# Import asynchronous waiting
import asyncio
# Import Sakanya Core
from __main__ import SakanyaCore

class Stats2():
  
  def __init__(self, bot):
    self.bot = bot
    #ax = plot.figure().gca()
    #ax.yaxis.set_major_locator(MaxNLocator(integer=True))

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
  async def stats2(self, context, argument=None):
    #await self.bot.send_message(context.message.author, "\n".join(sorted(set([f.name for f in matplotlib.font_manager.fontManager.ttflist]))))
    if argument is None:
      await self.bot.say('Try `' + SakanyaCore().prefix + 'help stats2`.')
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

      # sort alphabetically: sorted(graph_data, key=str.lower)
      for item in sorted(graph_data.items(), key=operator.itemgetter(1), reverse=True):
        # It is impossible to sort a dictionary, thus the dictionary is converted to a tuple upon
        # sorting. Each item in the tuple is a tuple with the first value being the key and second
        # being the value. 
        embed_graph += '**' + item[0] + '**: ' + str(item[1]) + \
        ' (' + "%.2f" % round(item[1] / total_messages * 100, 2) + '%)' + '\n'

      embed.title = '❯ Messages sent by users (ordered by amount descending)'
      embed.description = embed_graph
        
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

      # sort alphabetically: sorted(graph_data, key=str.lower)
      for item in sorted(graph_data.items(), key=operator.itemgetter(1), reverse=True):
        # It is impossible to sort a dictionary, thus the dictionary is converted to a tuple upon
        # sorting. Each item in the tuple is a tuple with the first value being the key and second
        # being the value. 
        embed_graph += '**' + item[0] + '**: ' + str(item[1]) + \
        ' (' + "%.2f" % round(item[1] / total_messages * 100, 2) + '%)' + '\n'

      # Fix if length is over the limit
      if len(embed_graph) > 2048:
        embed_graph = embed_graph[:2044] + '...'
      
      embed.title = '❯ Messages sent by bots (ordered by amount descending)'
      embed.description = embed_graph
        
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

      # sort alphabetically: sorted(graph_data, key=str.lower)
      for item in sorted(graph_data.items(), key=operator.itemgetter(1), reverse=True):
        # It is impossible to sort a dictionary, thus the dictionary is converted to a tuple upon
        # sorting. Each item in the tuple is a tuple with the first value being the key and second
        # being the value. 
        embed_graph += '**' + item[0] + '**: ' + str(item[1]) + \
        ' (' + "%.2f" % round(item[1] / total_messages * 100, 2) + '%)' + '\n'

      # Fix if length is over the limit
      if len(embed_graph) > 2048:
        embed_graph = embed_graph[:2044] + '...'

      embed.title = '❯ Messages sent by everyone (ordered by amount descending)'
      embed.description = embed_graph

    elif argument == 'emojis':

      data = await self.loadStatFile('reactions.json')
      graph_data = {}
      total_emojis = 0
      for key, value in list(data.items()):
        total_emojis += value
        graph_data[':' + key.split(':')[1] * ':'] = value
      
      if not graph_data:
        await self.bot.send_message(context.message.channel, 'Data malformed...')
      
      embed_graph = ''

      # sort alphabetically: sorted(graph_data, key=str.lower)
      for item in sorted(graph_data.items(), key=operator.itemgetter(1), reverse=True):
        # It is impossible to sort a dictionary, thus the dictionary is converted to a tuple upon
        # sorting. Each item in the tuple is a tuple with the first value being the key and second
        # being the value.
        embed_graph += '**' + item[0] + '**: ' + str(item[1]) + \
            ' (' + "%.2f" % round(item[1] / total_emojis * 100, 2) + '%)' + '\n'

      # Fix if length is over the limit
      if len(embed_graph) > 2048:
        embed_graph = embed_graph[:2044] + '...'

      embed.title = '❯ Emojis used (ordered by amount descending)'
      embed.description = embed_graph

    else:
      await self.bot.send_message(context.message.channel, 'Statistics for `' + argument + '` could not be found within me...')
      return
    
    await self.bot.send_message(context.message.channel, embed=embed)
  
def setup(bot):
  bot.add_cog(Stats2(bot))
