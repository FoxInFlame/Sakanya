# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import OrderedDict for an ordered dict (obviously)
from collections import OrderedDict
# Import Sakanya Core
from __main__ import SakanyaCore

class Help():
  def __init__(self, bot):
    self.bot = bot

  commands_dict = [
    ('help', {
      'module': 'commands.help',
      'short_description': 'Show this Help Message',
      'description': 'I\'ll show you a help message where you can learn all the features I have inside me.\n(´｡• ᵕ •｡`) ♡',
      'usage': 'help [keyword]',
      'admin': False
    }),
    ('about', {
      'module': 'commands.about',
      'short_description': 'Learn more about me',
      'description': 'I\'ll show you a message which contains basic information about me, as well as some stats!\n(*♡∀♡)',
      'usage': 'about',
      'admin': False
    }),
    ('love', {
      'module': 'commands.love',
      'short_description': 'Send your love to someone!',
      'description': '*The username is case-sensitive.*\nI\'ll pick a suitable love phrase for me to send your recipient. (´• ω •`) ♡',
      'usage': 'love <username>',
      'admin': False
    }),
    ('robot', {
      'module': 'commands.robot',
      'short_description': 'What do you look like as a robot?',
      'description': '(＃＞＜) It\'s another one of those useless utility commands that Fox added in...\nIf you give me any text, I\'ll quickly send a request to generate robot images from that.',
      'usage': 'robot [text]',
      'admin': False
    }),
    ('saka', {
      'module': 'commands.saka',
      'short_description': 'Reverse image search any picture',
      'description': 'I can reverse image search any image url you send me. SauceNao can find most lewd pictures and drawings, and WhatAnime can find sources for screenshots from anime! (The default is Saucenao if you don\'t specify). You can also attach images instead of pasting the URL if you find that easier.',
      'usage': 'saka [saucenao|whatanime] [url]',
      'admin': False
    }),
    ('iam', {
      'module': 'commands.iam',
      'short_description': 'Add yourself a self-assigned role',
      'description': 'You can describe yourself using roles, and access role-specific channels using them!\n\nIf you have the **AMA** role, you will be mentioned with someone needs help or wants to ask a question.\n\nThe **lewd** role will give access to the #nsfw channel.\n\nHaving the **hungry for new waifus** role will make Bob notify you when a new waifu war stage is initiated.\n\nIf no role is specified, I will list all the self-assigned roles you have.',
      'usage': 'iam ({})'.format(' | '.join(list(SakanyaCore().self_assigned_roles))),
      'admin': False
    }),
    ('iamnot', {
      'module': 'commands.iam',
      'short_description': 'Remove a self-assigned role from yourself',
      'description': 'You can remove a self-assigned role from yourself. To see which roles you have, do `>iam`.',
      'usage': 'iamnot ({})'.format(' | '.join(list(SakanyaCore().self_assigned_roles))),
      'admin': False
    }),
    ('colour', {
      'module': 'other.rolecolour',
      'short_description': 'Set your display colour on this server',
      'description': 'You can let me update your display colour on this server to any colour you want! There is of course also an alias `color` for anyone feeling American. Supported formats are hex and rgb, and the text values `random` for a random colour, and `remove` to refer back to the default colour.' + ('\nYour colour will be denied if I deem it illegible on Discord Dark Mode. On the contrary, no one cares about light mode anyway, so you can set it however light you want.' if SakanyaCore().colourrestrictions is True else ''),
      'usage': 'colour|color (#000000 | rgb(0, 0, 0) | random | remove)',
      'admin': False
    }),
    ('stats', {
      'module': 'commands.stats',
      'short_description': 'View various stats about this server',
      'description': 'I record quite a lot of things (more as Fox implements more!), and you can view a visualised representation of these stats. Currently, `messages_byeverone`, `messages_byusers`, and `messages_bybots` is available for you to use with me! These charts take quite a while to load, so please be patient and don\'t spam me out of rage - I\'ll just crash out of stress.',
      'usage': 'stats <stat_name>',
      'admin': False
    }),
    ('ping', {
      'module': 'commands.ping',
      'short_description': 'Ping the Discord server and check the response time',
      'description': 'I will send 5 requests to Discord with an animation, and report back the average response time.',
      'usage': 'ping',
      'admin': False
    }),
    ('modules', {
      'module': 'commands.modules',
      'short_description': 'View a list of modules, enable modules, or disable modules',
      'description': '**Fox only:** You can see the list of enabled modules I run on, enable certain modules, or disable others. Useful when a certain module is causing a havoc and you want to temporarily disable it while you work on the solution.',
      'usage': 'modules [enable|disable] [modulename]',
      'admin': True
    }),
    ('update', {
      'module': 'commands.update',
      'short_description': 'Updates me to the latest version',
      'description': '**Fox only:** This command will make me download the latest commit from my git repository, and restart myself.',
      'usage': 'update',
      'admin': True
    }),
    ('restart', {
      'module': 'commands.restart',
      'short_description': 'Makes me restart',
      'description': '**Fox only:** This command will make me restart.',
      'usage': 'restart',
      'admin': True
    }),
    ('addreaction', {
      'module': 'commands.addreaction',
      'short_description': 'Add a reaction to a specific message',
      'description': '**Fox only:** I can react to a specific message with an emoji of your choice. Unfortunately you will have to go through the process of gathering message and channel ids.',
      'usage': 'addreaction <channelid> <messageid> <reaction>',
      'admin': True
    })
  ]

  commands_dict = OrderedDict(commands_dict)

  features_dict = [
    ('suggestioncontrol', {
      'module': 'other.suggestioncontrol',
      'title': 'Suggestion Control',
      'short_description': 'Control messages in <#341874607651029003> as neccessary.',
      'description': 'I remove any messages in <#341874607651029003> when the message gets at least 5 <:x:348390305248182272>s, or when it gets one ✅ by the author of the message. ~(>_<~)',
      'admin': False
    }),
    ('quote', {
      'module': 'commands.modules', # Just a random one because it's in the main file
      'title': 'Quote',
      'short_description': 'Passively quote messages in chats.',
      'description': 'When a message starting with the Saka prefix (' + SakanyaCore().prefix + ') is posted, and I can\'t find a matching command, I will take that message as a quote and create an embed out of it. This feature is one of the most disliked features I have inside of me, apparently.\n(´。＿。｀)',
      'admin': False
    })
  ]

  """,
    ('automatickick', {
      'module': 'stats.lastactivity',
      'title': 'Automatic Kick System',
      'short_description': 'I kick users automatically if they have been deemed inactive.',
      'description': 'When users on this server have been inactive for over 30 days, I will automatically kick the users. Specifically, I will consider you as inactive when all of these are true for 30 days:\n- Not showing any "typing..."\n- Not sending any messages\n- Not adding or removing reactions to any messages\n- Not editing any existing messages\n- Not joining any voice channel\nBasically, everything that happens when you\'re actually inactive.\nヽ(´ー` )┌\n\nHere\'s a random situation you might be worried about. You went on a trip to the North Pole for 3 months and come back, to find yourself kicked. Kicked users cannot join using the public invite URL on the club page any more. Oh no! What should you do?\nヽ(´∀｀。ヽ) Worry no longer, because I will provide you a one-time invite code in case you want to rejoin! Go enjoy your North Pole!',
      'admin': False
      })
  """

  features_dict = OrderedDict(features_dict)

  @commands.command(pass_context=True)
  async def help(self, context, *, subcommand=None):
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
      color = SakanyaCore().embed_color,
      type = 'rich',
      description = 'I\'m here to provide you some help on how I function!'
    )
    helpembed.set_author(name='🐟 Help: ' + SakanyaCore().name, url=discord.Embed.Empty, icon_url=discord.Embed.Empty)
    if subcommand is None:
      print('hi')
      helpembed.set_thumbnail(url='https://i.imgur.com/09lpIAL.png')
      commands_str = ''
      for key, value in self.commands_dict.items():
        if value['module'] in tuple(self.bot.extensions) and value['admin'] is False:
          commands_str = ''.join([commands_str, ''.join(['`', key, '` - ', value['short_description'], '\n'])])
      helpembed.add_field(name='Commands', value=commands_str)
      otherfeatures_str = ''
      for key, value in self.features_dict.items():
        if value['module'] in tuple(self.bot.extensions) and value['admin'] is False:
          otherfeatures_str = ''.join([otherfeatures_str, ''.join(['`', key, '` - ', value['short_description'], '\n'])])
      helpembed.add_field(name='Other Features', value=otherfeatures_str)
      helpembed.add_field(name='Learn More', value='Parameters surrounded by <> are required, and ones surrounded by [] are optional.\n*To learn more about each feature, type `' + SakanyaCore().prefix + 'help <keyword>`.*')
    elif subcommand in self.commands_dict:
      if self.commands_dict[subcommand]['admin'] is False or context.message.author.id == '202501452596379648':
        helpembed.add_field(name=SakanyaCore().prefix + self.commands_dict[subcommand]['usage'], value=self.commands_dict[subcommand]['description'])
    elif subcommand in self.features_dict:
      if self.features_dict[subcommand]['admin'] is False or context.message.author.id == '202501452596379648':
        helpembed.add_field(name=self.features_dict[subcommand]['title'], value=self.features_dict[subcommand]['description'])
    else:
      helpembed.add_field(name='Not Found!', value='The keyword you specified (' + subcommand +') could not be found in my little list of features!')
    await self.bot.say(embed=helpembed)

def setup(bot):
  bot.add_cog(Help(bot))