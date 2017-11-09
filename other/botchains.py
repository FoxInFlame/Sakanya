# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import Sakanya Core
from __main__ import SakanyaCore

class BotChains():
  def __init__(self, bot):
    self.bot = bot
    self.times = 5

  @commands.command(pass_context=True, aliases=['poke', 'hello'])
  async def chain(self, context):
    """
    Part of a bot chain - Sends message to n:hello.
    
    Format:
      >hello

    Examples:
      >hello
    """
    await self.bot.say('n:hello')

  @commands.command(pass_context=True)
  async def helloreset(self, context):
    if context.message.author.id == '202501452596379648':
      self.times = 3

  async def on_message(self, message):
    if message.author.id == '270198146020278272' and message.content == 'k/hello':
      self.times = self.times - 1
      if self.times >= 0:
        await self.bot.send_message(message.channel, 'n:hello')


def setup(bot):
  bot.add_cog(BotChains(bot))