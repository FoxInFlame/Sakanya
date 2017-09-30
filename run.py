# 
#    _____       __                          
#   / ___/____ _/ /______ _____  __  ______ _     _.-=-._     .-, 
#   \__ \/ __ `/ //_/ __ `/ __ \/ / / / __ `/   .'       "-.,' / 
#  ___/ / /_/ / ,< / /_/ / / / / /_/ / /_/ /   (          _.  <
# /____/\__,_/_/|_|\__,_/_/ /_/\__, /\__,_/     `=.____.="  `._\
#                             /____/         
# 
# A shy Discord bot written by FoxInFlame in Discord.py.
# Version 1.0.10
# Changelog:
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
# import random for randomness (used in setting presence)
import random
# Import asynchronous waiting 
import asyncio


# Import URLlib.request for requests
import urllib.request
# Import URLlib.parse to manipulate URLs
import urllib.parse
# Import URLlib.error to handle error
import urllib.error
# Import lxml to parse XML and HTML
from lxml import etree

prefix = '>'
description = 'A reverse image search bot made for The nulls of MAL.'

startup_extensions = ['commands.love', 'commands.waifu', 'commands.about', 'commands.restart', 'commands.saka', 'commands.help', 'commands.robot', 'commands.update', 'commands.iam', 'other.filemanagement', 'other.suggestioncontrol', 'other.mentioninteraction', 'other.storytime', 'other.uselessinteractions']
bot = commands.Bot(command_prefix=prefix, description=description)
bot.remove_command('help') # Remove default help command

scheduler = sched.scheduler(time.time, time.sleep)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

custom_presences = [
  'No Poverty',
  'Zero Hunger',
  'Good Health and Well-being',
  'Quality Education',
  'Gender Equality',
  'Clean Water and Sanitation',
  'Affordable and Clean Energy',
  'Decent Work and Economic Growth',
  'Industry, Innovation and Infrastructure',
  'Reduced Inequality',
  'Sustainable Cities and Communities',
  'Responsible Consumption and Production',
  'Climate Action',
  'Life Below Water',
  'Life on Land',
  'Peace, Justice and Strong Institutions',
  'Partnerships for the Goals'
]

@bot.event
async def on_ready():
  foxinflame = await bot.get_user_info('202501452596379648')
  await bot.send_message(foxinflame, content='Sakanya is now online as ' + bot.user.name + '! Prefix is `' + prefix + '`.')
  print('Sakanya by FoxInFlame has logged into Discord as')
  print('@' + bot.user.name)
  print(bot.user.id)
  print('------')

async def changePresence():
  await bot.wait_until_ready()
  kaomoji_req = urllib.request.Request(url='http://kaomoji.ru/en/', data=None, headers=headers)
  try:
    response = urllib.request.urlopen(kaomoji_req)
    tree = etree.HTML(response.read().decode('utf8'))
    kaomojis = tree.xpath('//table[@class="table_kaomoji"]//td/span/text()')
  except (urllib.error.HTTPError, urllib.error.URLError) as e:
    print('Couldn\'t access kaomoji.ru. Error code: ' + str(e.code), None)
    kaomojis = ['Need help? >help']
  counter = 0
  while not bot.is_closed:
    random_kaomoji = random.random()
    if random_kaomoji < 0.5:
      # 50%
      if len(kaomojis) <= counter:
        counter = 0
      kaomoji = kaomojis[counter]
      counter += 1
    elif random_kaomoji < 0.85:
      # 35%
      kaomoji = 'Need help? >help'
    else:
      # 15%
      kaomoji = random.choice(custom_presences)

    type = 0
    if random.random() < 0.5:
      # 50% chance of streaming instead of playing
      type = 1
    await bot.change_presence(game=discord.Game(name=kaomoji, type=type), status=None, afk=False)
    await asyncio.sleep(900) # 15 minutes

@bot.event
async def on_message(message):
  await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    return

if __name__ == "__main__":
  for extension in startup_extensions:
    try:
      bot.load_extension(extension)
    except Exception as e:
      print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name, e))

  print('') # Empty line in case of continuous execution
  print('Connecting...')
  bot.loop.create_task(changePresence())
  bot.run('***REMOVED***')
  # Sakanya: ***REMOVED***
  # Reverser: ***REMOVED***

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