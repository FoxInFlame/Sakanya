import time
import discord
from discord.ext import commands


class Ping():
  """
  This class provides functions for the command `>ping`.
  """

  def __init__(self, bot):
    self.bot = bot

  @commands.command(pass_context=True)
  async def ping(self, context):
    """
    Ping the Discord server and see the time.

    Format:
      >ping

    Examples:
      >ping
    """
    channel = context.message.channel
    time1_1 = time.perf_counter()
    await self.bot.send_typing(channel)
    time1_2 = time.perf_counter()
    diff = time1_2 - time1_1
    time2_1 = time.perf_counter()
    message = await self.bot.send_message(channel, f'|᛫    | Ping! (**{round(diff * 1000)}ms**)')
    time2_2 = time.perf_counter()
    diff = diff + ((time2_2 - time2_1) - diff) / 2
    time3_1 = time.perf_counter()
    await self.bot.edit_message(message, f'| ᛫   | Ping! (**{round(diff * 1000)}ms**)')
    time3_2 = time.perf_counter()
    diff = diff + ((time3_2 - time3_1) - diff) / 3
    time4_1 = time.perf_counter()
    await self.bot.edit_message(message, f'|  ᛫  | Ping! (**{round(diff * 1000)}ms**)')
    time4_2 = time.perf_counter()
    diff = diff + ((time4_2 - time4_1) - diff) / 4
    time5_1 = time.perf_counter()
    await self.bot.edit_message(message, f'|   ᛫ | Ping! (**{round(diff * 1000)}ms**)')
    time5_2 = time.perf_counter()
    diff = diff + ((time5_2 - time5_1) - diff) / 5
    time6_1 = time.perf_counter()
    await self.bot.edit_message(message, f'|    ᛫| Ping! (**{round(diff * 1000)}ms**)')
    time6_2 = time.perf_counter()
    diff = diff + ((time6_2 - time6_1) - diff) / 6
    # Apparently there's a thing called rate-limiting, and thus no more requests can be made.
    
    await self.bot.edit_message(message, f'Pong! (Average **{round(diff * 1000)}ms**)')

def setup(bot):
  bot.add_cog(Ping(bot))
