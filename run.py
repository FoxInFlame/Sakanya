# 
#    _____       __                          
#   / ___/____ _/ /______ _____  __  ______ _     _.-=-._     .-, 
#   \__ \/ __ `/ //_/ __ `/ __ \/ / / / __ `/   .'       "-.,' / 
#  ___/ / /_/ / ,< / /_/ / / / / /_/ / /_/ /   (          _.  <
# /____/\__,_/_/|_|\__,_/_/ /_/\__, /\__,_/     `=.____.="  `._\
#                             /____/         
# 
# A shy but energetic Discord bot written by FoxInFlame in Discord.py.
# Version 1.6.0

import discord
from discord.ext import commands
from core import SakanyaCore

bot = commands.Bot(
    command_prefix=[
        SakanyaCore().prefix + ' ',
        SakanyaCore().prefix,
        'saka:',
        '!'  # Replacement of André
    ],
    description=SakanyaCore().description
)
bot.remove_command('help') # Remove default help command

startup_errors = ''

@bot.event
async def on_ready():
  owner = await bot.get_user_info('202501452596379648')
  startup_errors_message = 'None' if startup_errors == '' else '```' + startup_errors + '```'
  await bot.send_message(owner, content=(
      f'Sakanya is now online as {bot.user.name}! Prefix is `{SakanyaCore().prefix}`. \n'
      f'Errors while starting: {startup_errors_message}'
  ))
  print('---------------------------------------------------')
  print(f'Sakanya by FoxInFlame has logged into Discord as {bot.user.name} ({bot.user.id})')
  print('---------------------------------------------------')

@bot.event
async def on_message(message):
  """
  Process commands that we have built.
  """
  await bot.process_commands(message)

@bot.event
async def on_command_error(error, context):
  if isinstance(error, commands.CommandNotFound):
    if context.message.channel is None:
      # DM
      return
    if context.message.content[:3] != (SakanyaCore().prefix * 3): # Check if 3 prefixes are in a row
      return
    # Otherwise quote
    quote = discord.Embed(
        type='rich',
        color=SakanyaCore().embed_color,
        description=context.message.content.strip()[3:]
    )
    quote.set_author(
        name=f'{context.message.author.name} quoted:',
        icon_url=context.message.author.avatar_url
    )
    await bot.send_message(context.message.channel, embed=quote)
    try:
      await bot.delete_message(context.message)
    except discord.errors.Forbidden:
      return
    return

if __name__ == '__main__':
  for extension in SakanyaCore().startup_extensions:
    try:
      bot.load_extension(extension)
    except Exception as e:
      startup_errors += (
          f'Failed to load extension {extension}\n'
          f'{type(e).__name__}: {str(e)} \n')

  print('') # Empty line in case of continuous execution
  print('Loaded Modules: ', tuple(bot.extensions))
  print('Connecting to Discord...')
  try:
    bot.run(SakanyaCore().bot_token()) # True or empty/False for debug
  except Exception:
    print('Crash.')
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
