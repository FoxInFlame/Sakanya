# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import Sakanya Core
from __main__ import SakanyaCore

class IAm():
  def __init__(self, bot):
    self.bot = bot

  SelfAssignedRoles = {
    'lewd': '350190393607847937',
    'ama': '349277559449452545'
  }

  @commands.command(pass_context=True)
  async def iam(self, context, role=None):
    """
    Add a role to the user. If no role is specified, list all.
    
    Format:
      >iam <role>

    Examples:
      >iam lewd
      >iam ama
    """
    if context.message.server == None:
      await self.bot.say('I\'m sorry, but this command isn\'t available in DMs.')
      return
    if role is None:
      message = context.message.author.name + '\'s Self-Assigned Roles:'
      for userrole in context.message.author.roles:
        if userrole.id in list(self.SelfAssignedRoles.values()):
          # This role exists in SelfAssignedRoles
          message = message + '\n- **' + list(self.SelfAssignedRoles.keys())[list(self.SelfAssignedRoles.values()).index(userrole.id)] + '**'
      if message == 'Your Self-Assigned Roles:':
        # Nothing has changed, no role was present
        message = '(ू˃̣̣̣̣̣̣︿˂̣̣̣̣̣̣ ू) You have no self-assigned roles.'
      await self.bot.say(embed=discord.Embed(
        color = SakanyaCore().embed_color,
        type = 'rich',
        description = message
      ))
      return
    if role.lower() in self.SelfAssignedRoles:
      # Role exists (case-insensitive)
      roleRole = discord.utils.get(context.message.server.roles, id=self.SelfAssignedRoles[role.lower()])
      if roleRole in context.message.author.roles:
        await self.bot.say(embed=discord.Embed(
          color = SakanyaCore().embed_color,
          type = 'rich',
          description = 'You already have that role!'
        ))
        return
      await self.bot.add_roles(context.message.author, roleRole)
      await self.bot.say(embed=discord.Embed(
        color = SakanyaCore().embed_color,
        type = 'rich',
        description = '（＾³＾）～♪ You now have the role **' + role.lower() + '**.'
      ))
      return
    else:
      await self.bot.say(embed=discord.Embed(
        color = SakanyaCore().embed_color,
        type = 'rich',
        description = '(ᗒᗩᗕ) I couldn\'t find a role called ' + role + '...'
      ))

  @commands.command(pass_context=True)
  async def iamnot(self, context, role=None):
    """
    Remove a role from the user. If no role is specified, throw an error.
    
    Format:
      >iamnot <role>

    Examples:
      >iamnot lewd
      >iamnot ama
    """
    if context.message.server == None:
      await self.bot.say('I\'m sorry, but this command isn\'t available in DMs.')
      return
    if role is None:
      await self.bot.say(embed=discord.Embed(
        color = SakanyaCore().embed_color,
        type = 'rich',
        description = '（＾ω＾） You have to specify what role you don\'t want to be!'
      ))
      return
    if role.lower() in self.SelfAssignedRoles:
      # Role exists in self assigned roles (case-insensitive)
      roleRole = discord.utils.get(context.message.server.roles, id=self.SelfAssignedRoles[role.lower()])
      if roleRole not in context.message.author.roles:
        # User doesn't have it
        await self.bot.say(embed=discord.Embed(
          color = SakanyaCore().embed_color,
          type = 'rich',
          description = 'You can\'t remove a role you don\'t have!'
        ))
        return
      await self.bot.remove_roles(context.message.author, roleRole)
      await self.bot.say(embed=discord.Embed(
        color = SakanyaCore().embed_color,
        type = 'rich',
        description = '( ´･ω･) You no longer have the role **' + role.lower() + '**.'
      ))
      return
    else:
      await self.bot.say(embed=discord.Embed(
        color = SakanyaCore().embed_color,
        type = 'rich',
        description = '(ᗒᗩᗕ) I couldn\'t find a role called ' + role + '...'
      ))
def setup(bot):
  bot.add_cog(IAm(bot))