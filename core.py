class SakanyaCore():

  # Some basic info
  version = '1.5.0'
  prefix = '>'
  debug = False
  debug_server = '344957370901856266'
  debug_channel = '344957370901856268'
  production_server = '317924870950223872'
  production_channel = '317924870950223872'
  name = 'Sakanya'
  embed_color = 15839636
  description = 'A reverse image search bot made for The Nulls.'
  self_introduction = ('I\'m a Discord bot created by the hands of FoxInFlame#9833 '
                       'using *discord.py*. Although I may not be a girl in real life, '
                       'I would love it if you could still treat me as a normal girl here '
                       'on Discord. I wish I were born in real life... \n(｡•́︿•̀｡)')
  colourrestrictions = False
  presenceupdate_timer = 1800 # seconds
  self_assigned_roles = {
      'lewd': '350190393607847937',
      'ama': '349277559449452545',
      'ready for events at all times': '381412270481342465',
      'playing houkai3rd': '397940005735104512'
  }

  startup_extensions = [
      'commands.love',
      'commands.about',
      'commands.restart',
      'commands.saka',
      'commands.help',
      'commands.robot',
      'commands.update',
      'commands.iam',
      'commands.ping',
      'commands.stats',
      'commands.stats2',
      'commands.modules',
      'commands.addreaction',
      'other.filemanagement',
      'other.suggestioncontrol',
      'other.mentioninteraction',
      'other.uselessinteractions',
      'other.presenceupdate',
      'other.rolecolour',
      'other.botchains',
      'other.definitelynotaprilfools',
      'stats.messagecounter',
      'stats.reactioncounter',
      'stats.lastactivity'
  ]
  headers = {
      'User-Agent': ('Mozilla/5.0 (Windows NT 6.1) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/41.0.2228.0 Safari/537.36')
  }

  # Actual core code stuff
  def server_id(self):
    """
    Return main server ID:
    "The Nulls" if production, "Testing Server" if debug.
    """
    if self.debug is True:
      return self.debug_server
    return self.production_server

  def channel_id(self):
    """
    Return the main channel ID for #general:
    Depends on debug mode.
    """
    if self.debug is True:
      return self.debug_channel
    return self.production_channel

  def bot_token(self):
    """
    Returns the bot token to use.
    Sakanya if production, Reverser if debug.
    """
    if self.debug is True:
      return '***REMOVED***'
    return '***REMOVED***'

  # Function Decorators
  def command_botowner_only(self):
    async def check_sender(f):
      async def new_f(*args, **kwargs):
        if 'message' in args[1]:
          assert args[1].message.author.id == '202501452596379648', \
          await args[0].bot.add_reaction(args[1].message, '✅')
      new_f.func_name = f.func_name
      return await new_f
    return check_sender
