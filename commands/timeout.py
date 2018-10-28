import json
from datetime import datetime, timedelta
import asyncio
import discord
from discord.ext import commands
from core import SakanyaCore

class Timeout():
  """
  This module is no longer used and is kept for archival purposes only.
  When it is ran, it could potentially delete server channels without warning. Don't use.
  (#announcements disappeared because of this.)
  """
  def __init__(self, bot):
    self.bot = bot
    self.timeouts_json = {}
    try:
      data_file = SakanyaCore().r.get('timeouts')
      self.timeouts_json = json.loads(data_file)
    except (IOError, TypeError, ValueError):
      self.timeouts_json = {}

  async def on_ready(self):
    self.bot.loop.create_task(self.check_timeout_expiries())

  async def make_all_channels_readonly(self, server, member):
    """
    Makes all the channels in the server read only for the specified member.
    """
    cantsend_perms = discord.PermissionOverwrite(send_messages=False)

    for channel in server.channels:
      await self.bot.edit_channel_permissions(channel, member, cantsend_perms)


  async def create_user_specific_channel(self, server, member):
    """
    Create a channel in the specified server, that only admins and the user can see.
    """
    cantread_perms = discord.PermissionOverwrite(read_messages=False)
    canread_perms = discord.PermissionOverwrite(read_messages=True)
    everyone_perms = discord.ChannelPermissions(
        target=server.default_role, overwrite=cantread_perms)
    member_perms = discord.ChannelPermissions(
        target=member, overwrite=canread_perms)
    sakanya_perms = discord.ChannelPermissions(
        target=server.me, overwrite=canread_perms)
    channel = await self.bot.create_channel(server, 'timeout-' + member.name, everyone_perms, member_perms, sakanya_perms)
    return channel

  @commands.command(pass_context=True)
  @commands.check(SakanyaCore().is_admin)
  async def timeout(self, context, member: discord.Member, minutes, *, reason):
    """
    Timeout a specific user for a set amount of time.
    When timeouts go active, the user is first sent to a channel dedicated to that person,
    where a message from Sakanya says that they are timed out.
    Once they agree to this by pressing a reaction, they are allowed to browse the channels but
    not post anything in them, until the timeout is reached, which is when they are given full
    permission to participate in the discussion again.

    By setting user as discord.Member, the command only triggers when a mention or an exact
    nickname/username match occurs.

    Format:
      >timeout <username> 30 [Reason goes here]

    Examples:
      >love @Cyan 15 You have been a bad boy! This command restricts them for 15 minutes.
    """

    expiry_date = datetime.now() + timedelta(minutes=int(minutes))

    if member.id in self.timeouts_json:
      self.timeouts_json[member.id]['expiry'] = expiry_date
    else:
      await self.make_all_channels_readonly(context.message.server, member)
      channel = await self.create_user_specific_channel(context.message.server, member)

      await self.bot.send_message(channel, (
          f'Hi there {member.mention}! You have been timed out for **{minutes} minutes** '
          f'for the following reason: ```{reason}```'
          'Here\'s a quick overview of how a timeout works: \n'
          '- You lose the ability to send messages to channels until the expiry time is reached. \n'
          '- You can still read messages and follow the conversation. \n'
          '- Depending on your acts during the timeout, the expiry time might be delayed more.'))
      await self.bot.move_channel(channel, 0)

      self.timeouts_json[member.id] = {
          'expiry': expiry_date.strftime('%Y-%m-%d %H:%M:%S'),
          'server': context.message.server.id,
          'channel': channel.id
      }

    SakanyaCore().r.set('timeouts', json.dumps(self.timeouts_json))

  async def delete_readonly_overwrite(self, server, member_id, channel_id):
    """
    Fix everything up so people are free!
    """
    member = server.get_member(member_id)
    channel = server.get_channel(channel_id)
    for channel in server.channels:
      await self.bot.delete_channel_permissions(channel, member)
    await self.bot.send_message(channel, 'You are now free!')
    asyncio.sleep(120)
    await self.bot.delete_channel(channel)


  async def check_timeout_expiries(self):
    """
    Check for timeout expiries, and release those members if they are expired.
    """
    while not self.bot.is_closed:
      if self.timeouts_json is not None or bool(self.timeouts_json) is True:
        for member_id, data in self.timeouts_json.items():
          expiry_date = datetime.strptime(data['expiry'], '%Y-%m-%d %H:%M:%S')
          if expiry_date <= datetime.now():
            await self.delete_readonly_overwrite(
                self.bot.get_server(data['server']),
                member_id,
                data['channel'])

      await asyncio.sleep(60)



def setup(bot):
  bot.add_cog(Timeout(bot))
