# 
#    _____       __                          
#   / ___/____ _/ /______ _____  __  ______ _     _.-=-._     .-, 
#   \__ \/ __ `/ //_/ __ `/ __ \/ / / / __ `/   .'       "-.,' / 
#  ___/ / /_/ / ,< / /_/ / / / / /_/ / /_/ /   (          _.  <
# /____/\__,_/_/|_|\__,_/_/ /_/\__, /\__,_/     `=.____.="  `._\
#                             /____/         
# 
# A shy but energetic Discord bot written by FoxInFlame in Discord.py.
# Version 1.5.0
# Changelog:
# 1.5.0
# - Moved to Heroku using Free Dynos (1000 hours/month) because IATGOF's server lost its DB.
# - Commands added: >override_messagecount, >override_reactioncount
# 1.4.0
# - Added April Fools channel shuffling
# 1.3.0
# - 1.3.4
# - - Fix half broken logic regarding suggestion control. One message could have 10 upvotes and 5 downvotes.
# - 1.3.3
# - - Quote function requires 3 characters prefix
# - - Now counts reaction add/remove for emoji counter
# - - Suggestioncontrol works with Force Completion by FoxInFlame
# - 1.3.2
# - - Return of the graph statistics
# - - While also maintaining the text based statistics
# - - New emoji statistics
# - 1.3.1
# - - Fixed stats problems Drutol and IATGOF kept negging about
# - - Removed unused definitions in stats.py
# - Reformatted >stats for simpler, more quicker layout that matches Andre's
# 1.2.0
# - Commands added: >addreaction
# - Added Admin help inside >help that only shows when Fox sends the message
# 1.1.2
# - Add support for !manga url detection.
# - Fix KeyError: 'emoji' in case Emoji didn't exist for some unknown Discord bug
# - Now watches random YT videos as well.
# 1.1.1
# - Disable Automatic Kicking System
# - Commands added: >modules, >reset_messagecount
# - Now changes presence to "Listening to" and "Watching" as well
# - Change font for matplotlib to Osaka (installed by IATGOF)
# - >readfile sends to Gist now
# - Fix restart now working
# - Rewrote logic for presence update randomness
# 1.1.0
# - Now automatically kicks users if they're inactive!
# 1.0.19
# - Add "hungry for new waifu" as the role to get notified by BobDono.
# - Reset messagecounter and change JSON format.
# 1.0.18
# - Automatically add roles to new users
# - Now counts messages sent by authors.
# - Commands added: >stats
# - Now supports quoting using >
# 1.0.17
# - Add botchain >hello
# 1.0.16
# - Rewrote >saka using aiohttp instead of urllib so that it no longer crashes
# 1.0.15
# - Added SakanyaCore boolean to disable colour restrictions
# 1.0.14
# - Added >colour random, and >colour remove
# - Update help message for >colour
# - Added contrast checker for >colour
# 1.0.13
# - Moved debug setting to Core.
# - Removed all of Saka's useless Xaetral emote interactions
# - Removed Saka's useless no-motsy interaction
# - Commands added: >colour
# 1.0.12
# - Comamnds added: ping
# - Animation + average for ping
# 1.0.11
# - - fix
#   - Fixed mistyping of SakanyCore to SakanyaCore
# - Fixed typing bug in mention.
# - Fixed user selection when mentioning with question mark.
# - Moved core code to SakanyaCore() class in __main__
# - Use SakanyaCore() class in other files instead of hardcoded values.
# - Moved PresenceUpdate function to individual file.
# - Output startup errors for modules if there were any to Discord.
# 1.0.10
# - Add 'n:cry' and 'n:motherofgod' to further mock Xae.
# - Confirmed that mentions in embeds don't notify mentioned users.
# - Changed response to mentioning André.
# - Add 3 more love messages.
# 1.0.9
# - Rename mockxaetral to uselessinteractions
# - Added response to Andy's 'No Motsy' message
# 1.0.8
# - Removed unneccessary new line in >update response
# - Fixed status message after update was aborted
# - Added a small command that you wouldn't notice :)
# 1.0.7
# - Update command now aborts restart if it's already up-to-date.
# 1.0.6
# - Properly handle help messages with nonexistent subcommands
# - New turquoise background in profile picture
# 1.0.5
# - Renamed suggestionremoval file and class to suggestioncontrol
# - Added auto-reacting to suggestions
# - Increased required x count to 5
# - Rename ReadFile class to FileManagement
# 1.0.4
# - Commands added: readfile, emptyfile
# 1.0.3
# - Output git pull response to chat
# - Commands added: iam, iamnot
# 1.0.2
# - -fix2
#   - Change switchversion to update
# - -fix
#   - Fix bugs in switchversion
#   - Print debug statuses
# - Added support for updating via Discord using the switchversion command
# 1.0.1
# - Now on a stable server
# - Commands added: robot
# - Moved commands to individual files and used cogs (advise from IATGOF)
# 1.0.0
# - Commands added: saka, restart, help, about, love, waifu
# - Emoji Suggestion
# - Suggestion Removal
# - Interaction with mentions


# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import sched and time to make a scheduler
import sched, time
# Import logging to view crash logs
import logging
logging.basicConfig(filename='log.log', level=logging.WARNING)
# Import OS for file systems
import os

import ssl

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
  description = 'A reverse image search bot made for The nulls of MAL.'
  self_introduction = 'I\'m a Discord bot created by the hands of FoxInFlame#9833 using *discord.py*. Although I may not be a girl in real life, I would love it if you could still treat me as a normal girl here on Discord. I wish I were born in real life... \n(｡•́︿•̀｡)'
  colourrestrictions = False
  presenceupdate_timer = 1800 # seconds
  self_assigned_roles = {
    'lewd': '350190393607847937',
    'ama': '349277559449452545',
    'ready for events at all times': '381412270481342465',
    'playing houkai3rd': '397940005735104512'
  }

  # Actual core code stuff
  def server_id(self):
    if self.debug is True:
      return self.debug_server
    else:
      return self.production_server

  def channel_id(self):
    if self.debug is True:
      return self.debug_channel
    else:
      return self.production_channel

  def bot_token(self):
    if self.debug is True:
      return '***REMOVED***'
    else:
      return '***REMOVED***'

  startup_extensions = ['commands.love', 'commands.about', 'commands.restart', 'commands.saka', 'commands.help', 'commands.robot', 'commands.update', 'commands.iam', 'commands.ping', 'commands.stats', 'commands.stats2', 'commands.modules', 'commands.addreaction', 'other.filemanagement', 'other.suggestioncontrol', 'other.mentioninteraction', 'other.uselessinteractions', 'other.presenceupdate', 'other.rolecolour', 'other.botchains', 'other.definitelynotaprilfools', 'stats.messagecounter', 'stats.reactioncounter', 'stats.lastactivity'] 
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

bot = commands.Bot(command_prefix=[SakanyaCore().prefix + ' ', SakanyaCore().prefix, 'saka:'], description=SakanyaCore().description)
bot.remove_command('help') # Remove default help command

startup_errors = ''

@bot.event
async def on_ready():
  owner = await bot.get_user_info('202501452596379648')
  await bot.send_message(owner, content='Sakanya is now online as ' + bot.user.name + '! Prefix is `' + SakanyaCore().prefix + '`.\n' + ssl.OPENSSL_VERSION + 'Errors while starting: ' + ('None' if startup_errors == '' else '```' + startup_errors + '```'))
  print('---------------------------------------------------')
  print('Sakanya by FoxInFlame has logged into Discord as')
  print('@' + bot.user.name + ' ID' + bot.user.id)
  print('---------------------------------------------------')

@bot.event
async def on_message(message):
  await bot.process_commands(message)

@bot.event
async def on_command_error(error, context):
  if isinstance(error, commands.CommandNotFound):
    if context.message.channel is None:
      return
    if context.message.content[:3] != (SakanyaCore().prefix * 3):
      return
    quote = discord.Embed(
      type = 'rich',
      color = SakanyaCore().embed_color,
      description = context.message.content.strip()[3:]
    )
    quote.set_author(name=context.message.author.name + ' quoted:', icon_url=context.message.author.avatar_url)
    await bot.send_message(context.message.channel, embed=quote)
    try: 
      await bot.delete_message(context.message)
    except discord.errors.Forbidden:
      return
    return

if __name__ == "__main__":
  for extension in SakanyaCore().startup_extensions:
    try:
      bot.load_extension(extension)
    except Exception as e:
      startup_errors += 'Failed to load extension {0}\n{1}: {2}\n'.format(extension, type(e).__name__, str(e))

  print('') # Empty line in case of continuous execution
  try:
    with open(os.path.join(os.path.dirname(__file__), 'log.log'), 'r') as data_file:
      data = data_file.read();
      startup_errors += data
      with open(os.path.join(os.path.dirname(__file__), 'log.log'), 'w') as file:
        file.write('')
  except IOError:
    pass
  print('Loaded Modules:', tuple(bot.extensions))
  print('Connecting to Discord...')
  try:
    bot.run(SakanyaCore().bot_token()) # True or empty/False for debug
  except Exception as e:
    logging.exception('Crash.')
    raise SystemExit


# End of file.
# 
#                                   ____
#                                /\|    ~~\
#                              /'  |   ,-. `\
#                             |       | X |  |
#                            _|________`-'   |X
#                          /'          ~~~~~~~~~,
#                        /'             ,_____,/_
#                     ,/'        ___,'~~         ;
# ~~~~~~~~|~~~~~~~|---          /  X,~~~~~~~~~~~~,
#         |       |            |  XX'____________'
#         |       |           /' XXX|            ;
#         |       |        --x|  XXX,~~~~~~~~~~~~,
#         |       |          X|     '____________'
#         |   o   |---~~~~\__XX\             |XX
#         |       |          XXX`\          /XXXX
# ~~~~~~~~'~~~~~~~'               `\xXXXXx/' \XXX
#                                  /XXXXXX\
#                                /XXXXXXXXXX\
#                              /XXXXXX/^\XDCAU\
#                             ~~~~~~~~   ~~~~~~~
