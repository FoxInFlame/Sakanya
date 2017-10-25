# 
#    _____       __                          
#   / ___/____ _/ /______ _____  __  ______ _     _.-=-._     .-, 
#   \__ \/ __ `/ //_/ __ `/ __ \/ / / / __ `/   .'       "-.,' / 
#  ___/ / /_/ / ,< / /_/ / / / / /_/ / /_/ /   (          _.  <
# /____/\__,_/_/|_|\__,_/_/ /_/\__, /\__,_/     `=.____.="  `._\
#                             /____/         
# 
# A shy Discord bot written by FoxInFlame in Discord.py.
# Version 1.0.14
# Changelog:
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

class SakanyaCore():
  # Some basic info
  version = '1.0.14'
  prefix = '.'
  debug = False
  debug_server = '344957370901856266'
  production_server = '317924870950223872'
  name = 'Sakanya'
  embed_color = 15839636
  description = 'A reverse image search bot made for The nulls of MAL.'
  self_introduction = 'I\'m a Discord bot created by the hands of FoxInFlame#9833 using *discord.py*. Although I may not be a girl in real life, I would love it if you could still treat me as a normal girl here on Discord. I wish I were born in real life... \n(｡•́︿•̀｡)'

  # Actual core code stuff
  def server_id(self):
    if self.debug is True:
      return self.debug_server
    else:
      return self.production_server

  def bot_token(self):
    if self.debug is True:
      return '***REMOVED***'
    else:
      return '***REMOVED***'
  startup_extensions = ['commands.love', 'commands.about', 'commands.restart', 'commands.saka', 'commands.help', 'commands.robot', 'commands.update', 'commands.iam', 'commands.ping', 'other.filemanagement', 'other.suggestioncontrol', 'other.mentioninteraction', 'other.uselessinteractions', 'other.presenceupdate', 'other.rolecolour']
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

bot = commands.Bot(command_prefix=SakanyaCore().prefix, description=SakanyaCore().description)
bot.remove_command('help') # Remove default help command

startup_errors = ''

@bot.event
async def on_ready():
  owner = await bot.get_user_info('202501452596379648')
  await bot.send_message(owner, content='Sakanya is now online as ' + bot.user.name + '! Prefix is `' + SakanyaCore().prefix + '`.\nErrors while starting: ' + ('None' if startup_errors == '' else '```' + startup_errors + '```'))
  print('---------------------------------------------------')
  print('Sakanya by FoxInFlame has logged into Discord as')
  print('@' + bot.user.name)
  print(bot.user.id)
  print('---------------------------------------------------')

@bot.event
async def on_message(message):
  await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    return

if __name__ == "__main__":
  for extension in SakanyaCore().startup_extensions:
    try:
      bot.load_extension(extension)
    except Exception as e:
      startup_errors += 'Failed to load extension {0}\n{1}: {2}'.format(extension, type(e).__name__, e)

  print('') # Empty line in case of continuous execution
  print(startup_errors)
  print(tuple(bot.extensions))
  print('Connecting...')
  bot.run(SakanyaCore().bot_token()) # True or empty/False for debug

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