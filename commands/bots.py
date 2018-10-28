from collections import OrderedDict
import discord
from discord.ext import commands


class Bots():
  """
  This class provides functions for the command `>bots`.
  """

  def __init__(self, bot):
    self.bot = bot

  bots_dict = [
      ('Kaneda', {
          'author': 'Benpai',
          'tag': '9772',
          'description': 'It offers a lot of general utility commands.',
          'detail_command': 'k/about',
          'help_command': 'k/help'
      }),
      ('Sakanya', {
          'author': 'FoxInFlame',
          'tag': '9833',
          'description': (
              'Its primary goal is to reverse-search images, however it also offers utility '
              'commands, some of which help Fox manage this server efficiently.'),
          'detail_command': '>about',
          'help_command': '>help'
      }),
      ('Margarine', {
          'author': 'Butterstroke',
          'tag': '7150',
          'description': 'It\'s a lovely and helpful bot(he can\'t math though).',
          'detail_command': 'm~about',
          'help_command': 'm~help'
      }),
      ('trigger_chan', {
          'author': 'trigger_death',
          'tag': '3846',
          'description': (
              'It offers support for spoilers! Plus some utility commands and unique reaction '
              'commands.'),
          'detail_command': 't/about',
          'help_command': 't/help'
      })
  ]

  bots_dict = OrderedDict(bots_dict)


  @commands.command()
  async def bots(self):
    """
    Shows list of bots.

    Format:
      >bots

    Examples:
      >bots
    """
    text = ''
    for key, value in self.bots_dict.items():
      text += (
          f'**{key}** is a bot made by **{value["author"]}**#{value["tag"]}.\n'
          f'{value["description"]}\n'
          f'For more details, type `{value["detail_command"]}`.\n'
          f'For a list of {key}\'s commands, type `{value["help_command"]}`.\n\n')
    self.bot.say(text)


def setup(bot):
  bot.add_cog(Bots(bot))
