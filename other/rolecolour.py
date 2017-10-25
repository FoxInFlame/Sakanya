# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import Sakanya Core
from __main__ import SakanyaCore
# Import colour to use colours
import colour
# Import os to use relative file names
import os
# Import JSON to read roles.json
import json
# Import re for regular expression search (rgb)
import re
# Import math to round.
import math
# Import random to random colours
import random

class RoleColour():
  def __init__(self, bot):
    self.bot = bot
    with open(os.path.join(os.path.dirname(__file__), 'roles.json')) as data_file:
      try:
        self.roles_json = json.load(data_file)
      except ValueError as e:
        self.roles_json = {}

  def luminance(self, r, g, b):
    def rgb_map(v):
      v /= 255
      return (v / 12.92) if (v <= 0.03928) else ((v + 0.055) / 1.055)**2.4
    a = list(map(rgb_map, [r, g, b]))
    return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722

  def contrast(self, rgb1, rgb2):
    return (self.luminance(rgb1[0], rgb1[1], rgb1[2]) + 0.05) / (self.luminance(rgb2[0], rgb2[1], rgb2[2]) + 0.05)


  @commands.command(pass_context=True, aliases=['color'])
  async def colour(self, context, *, argument=None):
    """
    @everyone
    Set the colour of the user's role to what they specify.
    Admin:
    Pair users with roles, and send all roles of servers.
    
    Format:
      >color|colour <most colours>
      >color|colour admin:<pair|send_ids>

    Examples:
      >color #ff8a65
      >colour rgb(25, 123, 19)
      >color 51ab21
    """
    if argument is None:
      await self.bot.say('Try `' + SakanyaCore().prefix + 'help colour`.')
      return
    if 'admin:' in argument:
      if context.message.author.id != '202501452596379648':
        await self.bot.say('☆⌒(>。<) You don\'t have the right to execute this command...')
        return
      argument = argument[6:] # Remove the admin section so we can handle it properly

      if argument == 'send_ids':
        msg = ''
        for role in context.message.server.roles:
          if role.name == '@everyone': 
            continue
          msg += 'Role Name: ' + role.name + '\nRole Id: ' + role.id + '\nRole Colour:' + str(role.colour.value) + '\n'
        owner = await self.bot.get_user_info('202501452596379648')
        if len(msg) > 1800:
          n = 1800
          msgs = [msg[i:i+n] for i in range(0, len(msg), n)]
          for x in msgs:
            await self.bot.send_message(owner, content=x)
        else:
          await self.bot.send_message(owner, content=msg)
        await self.bot.say('*DEBUG*: Sent.')
      elif argument == 'pair':
        pairing_message = await self.bot.say(embed=discord.Embed(
          color = SakanyaCore().embed_color,
          type = 'rich',
          title = 'Pairing',
          description = 'Enter a user ID:'
        ))
        message_userid = await self.bot.wait_for_message(author=context.message.author)
        try:
          userInstance_global = await self.bot.get_user_info(message_userid.content)
          await self.bot.edit_message(pairing_message, embed=discord.Embed(
            color = SakanyaCore().embed_color,
            type = 'rich',
            title = 'Pairing',
            description = '**' + userInstance_global.name + '** was found with the ID specified.\n\nPlease specifiy the role ID this person should have, or type `cancel` to cancel.'
          ))
          message_roleid = await self.bot.wait_for_message(author=context.message.author)
          if message_roleid.content.lower() == 'cancel':
            await self.bot.edit_message(pairing_message, embed=discord.Embed(
              color = SakanyaCore().embed_color,
              type = 'rich',
              title = 'Pairing',
              description = 'Pairing process cancelled.'
            ))
            return
          server = self.bot.get_server(SakanyaCore().server_id())
          roles_server = server.roles
          roleInstance_server = next((role for role in roles_server if role.id == message_roleid.content), None)
          if roleInstance_server is None:
            await self.bot.edit_message(pairing_message, embed=discord.Embed(
              color = SakanyaCore().embed_color,
              type = 'rich',
              title = 'Pairing',
              description = 'A role with the specified ID could not be found.'
            ))
            return
          discordColour = roleInstance_server.colour.value
          if discordColour != 0:
            discordColour = "{0:x}".format(discordColour)
          else:
            discordColour = '0'
          self.roles_json.setdefault(userInstance_global.id, {
            "role": roleInstance_server.id,
            "colour": discordColour,
            "name": userInstance_global.name
          })
          with open(os.path.join(os.path.dirname(__file__), 'roles.json'), 'w') as file: # Then overwrite the file
            file.write(json.dumps(self.roles_json, indent=2))
          await self.bot.edit_message(pairing_message, embed=discord.Embed(
            color = SakanyaCore().embed_color,
            type = 'rich',
            title = 'Pairing',
            description = '**' + userInstance_global.name + '** has been paired with the role *' + roleInstance_server.name + '*.'
          ))
        except Exception as e:
          await self.bot.edit_message(pairing_message, embed=discord.Embed(
            color = SakanyaCore().embed_color,
            type = 'rich',
            title = 'Pairing',
            description = 'User could not be found. Error: ' + e
          ))
      return
    try:
      # Check if the message contains an rgb(), which isn't natively supported by the colour package
      expression = re.compile('rgb\(([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5]), ?([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5]), ?([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])\)')
      search = expression.search(argument)
      if argument.lower() == 'remove':
        new_colour = colour.Color(rgb=(0, 0, 0))
      elif argument.lower() == 'random':
        new_colour = colour.Color(rgb=(random.random(), random.random(), random.random()))
      elif search is not None:
        new_colour = colour.Color(rgb=(int(search.group(1))/255, int(search.group(2))/255, int(search.group(3))/255))
      else:
        # Raises exceptions automatically in case it's not a colour (we catch it later)
        new_colour = colour.Color(argument)
        if self.contrast([new_colour.red * 255, new_colour.green * 255, new_colour.blue * 255], [54, 57, 62]) < 4:
          await self.bot.say('☆(＃××) Your colour has **NOT** been applied. ' + new_colour.hex_l + ' is not legible enough on Discord Dark Mode! ')
          return

      if context.message.author.id in self.roles_json:
        # If the author already has a role then change it
        server = self.bot.get_server(SakanyaCore().server_id()) # Get the server
        roles_server = server.roles # Get the roles in the server
        roleInstance_server = next((role for role in roles_server if role.id == self.roles_json[context.message.author.id]['role']), None) # Get the specific role that the author has for themselves in the server
        if roleInstance_server is None: 
          # The role is in the JSON but doesn't exist - most likely removed.
          await self.bot.say('(ノ_<。)ヾ(´ ▽ ` ) The role paired with you has been removed. Let\'s mention Fox so that he can somehow fix it. \n<@202501452596379648>')
          return
        await self.bot.edit_role(server, roleInstance_server, colour=discord.Colour(value=int(new_colour.hex_l[1:], 16))) # Without the "0x" part before the hex string, python cannot know if it should convert to decimal. But using ",16" makes it forcibly decimal (which is what discord.py wants)
        self.roles_json[context.message.author.id]['colour'] = new_colour.hex_l[1:] # Update the JSON
        with open(os.path.join(os.path.dirname(__file__), 'roles.json'), 'w') as file: # Then overwrite the file
          file.write(json.dumps(self.roles_json, indent=2))
        if new_colour.hex_l == '#000000':
          await self.bot.say('*<@' + context.message.author.id + '> ٩(｡•́‿•̀｡)۶ You have removed your role-specific colour!*') # Send confirmation message
        else:
          await self.bot.say('*<@' + context.message.author.id + '> ٩(｡•́‿•̀｡)۶ You have changed your colour to ' + new_colour.hex_l + '!*') # Send confirmation message
      else:
        await self.bot.say('(-_-;)・・・ Your username is not yet bound to a specifc role. Let\'s mention Fox so that he can do that for you. \n<@202501452596379648>')

    except (ValueError, AttributeError) as e:
      print(e)
      await self.bot.say('☆ｏ(＞＜；)○ `' + argument + '` is not a valid colour...')
    except Exception as e:
      await self.bot.say('(-_-;)・・・ ' + e)
    
def setup(bot):
  bot.add_cog(RoleColour(bot))