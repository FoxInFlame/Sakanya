# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import OrderedDict for an ordered dict (obviously)
from collections import OrderedDict

class Help():
  def __init__(self, bot):
    self.bot = bot


  commands_dict = [
    ('help', {
      'short_description': 'Show this Help Message',
      'description': 'I\'ll show you a help message where you can learn all the features I have inside me.\n(´｡• ᵕ •｡`) ♡',
      'usage': '>help'
    }),
    ('about', {
      'short_description': 'Learn more about me',
      'description': 'I\'ll show you a message which contains basic information about me, as well as some stats!\n(*♡∀♡)',
      'usage': '>about'
    }),
    ('waifu', {
      'short_description': 'An useless command that Fox put in (⁄ ⁄•⁄ω⁄•⁄ ⁄)',
      'description': 'It\'s some useless command that Fox put in me\n(⁄ ⁄•⁄ω⁄•⁄ ⁄)',
      'usage': '>waifu'
    }),
    ('love', {
      'short_description': 'Send your love to someone!',
      'description': '*The username is case-sensitive.*\nI\'ll pick a suitable love phrase for me to send your recipient. (´• ω •`) ♡',
      'usage': '>love [username]'
    }),
    ('robot', {
      'short_description': 'What do you look like as a robot?',
      'description': '(＃＞＜) It\'s another one of those useless utility commands that Fox added in...\nIf you give me any text, I\'ll quickly send a request to generate robot images from that.',
      'usage': '>robot [text]'
    }),
    ('saka', {
      'short_description': 'Reverse image search any picture',
      'description': 'I can reverse image search any image url you send me. SauceNao can find most lewd pictures and drawings, and WhatAnime can find sources for screenshots from anime! (The default is Saucenao if you don\'t specify). You can also attach images instead of pasting the URL if you find that easier.',
      'usage': '>saka [saucenao|whatanime] [url]'
    })
  ]

  commands_dict = OrderedDict(commands_dict)

  features_dict = [
    ('emoji', {
      'title': 'Emoji Suggestions',
      'short_description': 'Users can create and vote on emoji suggestions',
      'description': 'You can suggest an emoji to add by sending a message in <#341874607651029003> in the following format:\n```Emoji Suggestion - :newemojinamegoeshere:\n<imageurl>```\nWhen the message gets at least 5 thumbs up reactions, Fox will be reminded to create the emoji.'
    }),
    ('suggestionremoval', {
      'title': 'Suggestion Removal',
      'short_description': 'Delete messages in <#341874607651029003> when people decide it\'s not worthy.',
      'description': 'I remove any messages in <#341874607651029003> when the message gets at least 4 <:x:348390305248182272>s. ~(>_<~)'
    })
  ]

  features_dict = OrderedDict(features_dict)

  @commands.command()
  async def help(self, *, subcommand=None):
    """
    Show help messages on how to interact with Sakanya.
    
    Format:
      >help [section]

    Examples:
      >help
      >help about
      >help emojisuggestion
    """
    helpembed = discord.Embed(
      color = 15839636,
      type = 'rich',
      description = 'I\'m here to provide you some help on how I function!'
    )
    helpembed.set_author(name='🐟 Help: Sakanya', url=discord.Embed.Empty, icon_url=discord.Embed.Empty)
    if subcommand is None:
      helpembed.set_thumbnail(url='https://i.imgur.com/09lpIAL.png')
      commands_str = ''
      for key, value in self.commands_dict.items():
        commands_str = ''.join([commands_str, ''.join(['`', key, '` - ', value['short_description'], '\n'])])
      helpembed.add_field(name='Commands', value=commands_str)
      otherfeatures_str = ''
      for key, value in self.features_dict.items():
        otherfeatures_str = ''.join([otherfeatures_str, ''.join(['`', key, '` - ', value['short_description'], '\n'])])
      helpembed.add_field(name='Other Features', value=otherfeatures_str)
      helpembed.add_field(name='Learn More', value='Parameters surrounded by <> are required, and ones surrounded by [] are optional.\n*To learn more about each feature, type `>help <keyword>`.*')
    elif subcommand in self.commands_dict:
      helpembed.add_field(name=self.commands_dict[subcommand]['usage'], value=self.commands_dict[subcommand]['description'])
    elif subcommand in self.features_dict:
      helpembed.add_field(name=self.features_dict[subcommand]['title'], value=self.features_dict[subcommand]['description'])
    await self.bot.say(embed=helpembed)

def setup(bot):
  bot.add_cog(Help(bot))