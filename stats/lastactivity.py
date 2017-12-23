# Import discord
import discord
# Import os to use relative file names
import os
# Import JSON to read lastmessage.json
import json
# Import Sakanya Core
from __main__ import SakanyaCore
# Import datetime
import datetime
# Import asynchronous waiting 
import asyncio

class Stats_LastActivity():
  """
  Take note of the last actions by each user.
  """
  
  def __init__(self, bot):
    self.bot = bot
    try:
      with open(os.path.join(os.path.dirname(__file__), 'lastactivity.json'), 'r') as data_file:
        try:
          self.dates_json = json.load(data_file)
        except ValueError as e:
          self.dates_json = {}
    except IOError:
      self.dates_json = {}

  async def on_ready(self):
    self.bot.loop.create_task(self.checkForInactiveUsers())

    # So that get_server is usable
    if self.dates_json == {}:
      server = self.bot.get_server(SakanyaCore().server_id())
      self.dates_json = {}
      for member in server.members:
        if member.bot is False:
          self.dates_json[member.id] = str(datetime.datetime.utcnow())

  async def updateActivity(self, user):
    self.dates_json[user] = str(datetime.datetime.utcnow())

    with open(os.path.join(os.path.dirname(__file__), 'lastactivity.json'), 'w') as file: # Then overwrite the file
      file.write(json.dumps(self.dates_json, indent=2))

  async def on_socket_response(self, jsonmsg):
    # Filtering out just The nulls is hard (because server id is not returned - only channel id)
    # So just keep it to all :)
    if jsonmsg['t'] == 'TYPING_START':
      await self.updateActivity(jsonmsg['d']['user_id'])
    elif jsonmsg['t'] == 'MESSAGE_CREATE':
      await self.updateActivity(jsonmsg['d']['author']['id'])
    elif jsonmsg['t'] == 'MESSAGE_REACTION_ADD':
      await self.updateActivity(jsonmsg['d']['user_id'])
    elif jsonmsg['t'] == 'MESSAGE_REACTION_REMOVE':
      await self.updateActivity(jsonmsg['d']['user_id'])
    elif jsonmsg['t'] == 'MESSAGE_UPDATE':
      if 'author' in jsonmsg['d']:
        await self.updateActivity(jsonmsg['d']['author']['id'])
    # This can be canged by the admins as well (e.g. roles, nickname) so don't detect.
    #elif jsonmsg['t'] == 'GUILD_MEMBER_UPDATE':
    #  await self.updateActivity(jsonmsg['d']['user']['id'])
    elif jsonmsg['t'] == 'VOICE_STATE_UPDATE':
      await self.updateActivity(jsonmsg['d']['user_id'])
    elif jsonmsg['t'] == 'GUILD_MEMBER_ADD':
      await self.updateActivity(jsonmsg['d']['user']['id'])
    elif jsonmsg['t'] == 'GUILD_MEMBER_REMOVE':
      self.dates_json.pop(jsonmsg['d']['user']['id'])
      with open(os.path.join(os.path.dirname(__file__), 'lastactivity.json'), 'w') as file: # Then overwrite the file
        file.write(json.dumps(self.dates_json, indent=2))

  async def checkForInactiveUsers(self):
    while not self.bot.is_closed:
      currenttime = datetime.datetime.utcnow()
      for member_id, timestamp_naive in list(self.dates_json.items()):
        timestamp = datetime.datetime.strptime(timestamp_naive, '%Y-%m-%d %H:%M:%S.%f')
        timedelta = currenttime - timestamp
        if timedelta.total_seconds() >= 86400 * 30:
          """
          # Over a month ago. Kick!
          channel = self.bot.get_channel(SakanyaCore().channel_id())
          server = self.bot.get_server(SakanyaCore().server_id())
          invite_url = await self.bot.create_invite(channel, max_uses=1)
          member = self.bot.get_server(SakanyaCore().server_id()).get_member(member_id)
          if member is None: # Member is gone, remove from JSON
            self.dates_json.pop(member_id, None)
            continue
          user = await self.bot.get_user_info(member_id)
          if user.bot is True: # Member is bot somehow (even though it's supposed to be filtered), remove from JSON
            self.dates_json.pop(member_id, None)
            continue
          try:
            if member.id == server.owner.id:
              continue
            await self.bot.send_message(user, embed=discord.Embed(
              title = 'Kicked due to inactivity',
              type = 'rich',
              color = SakanyaCore().embed_color,
              description = 'Hey ' + user.name + '.\n\n**__What\'s happening?__**\nYou seem to have been inactive in `' + channel.server.name + '` for the past 30 days. To keep the server clean, any user who hasn\'t shown activity on the server for more than 30 days are kicked automatically by me. Unfortunately, you have been deemed as one of these users, and therefore have been **kicked from the server**.\n\nNow that you\'re kicked, you cannot join with the public link on the club page anymore. If you want to join the Discord server once more, please use the invite link below.\n\n**__Rejoin (one-time link)__**\n' + invite_url.url + '\n\n**__If you believe this is a false claim__**\nPlease rejoin and contact FoxInFlame to get the bug fixed.'
            ))
            await self.bot.kick(member)
            # Will be removed in the event handler in function above
            await self.bot.send_message(channel, embed=discord.Embed(
              title = 'Kicked due to inactivity',
              type = 'rich',
              color = SakanyaCore().embed_color,
              description = 'Sad to say, ' + user.name + ' has just been kicked by me due to their inactivity on this server for the past 30 days. They have received a new invite link in case they want to rejoin, so not much harm has been done!'
            ))
          except discord.errors.Forbidden as e:
            # No Permissions, user is admin or something. Just ignore
            print(e)
            continue
          """
          server = self.bot.get_server(SakanyaCore().server_id())
          member = self.bot.get_server(SakanyaCore().server_id()).get_member(member_id)
          user = await self.bot.get_user_info(member_id)
          await self.bot.send_message(server, embed=discord.Embed(
            title = 'Inactive user',
            type = 'rich',
            color = SakanyaCore().embed_color,
            description = 'So, ' + user.name + ' has been inactive in this server for the past 30 days. This would\'ve resulted in a kick with a rejoin link, however there has been many oppositions, and therefore that feature has been disabled. They are still in this server! :)'
          ))

      await asyncio.sleep(86400) # one day!


def setup(bot):
  bot.add_cog(Stats_LastActivity(bot))