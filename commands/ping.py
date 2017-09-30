# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import time for ping time
import time
# Import Sakanya Core
from __main__ import SakanyaCore

class Ping():
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
    message = await self.bot.send_message(channel, '|᛫    | Ping! (**{0}ms**)'.format(round(diff * 1000)))
    time2_2 = time.perf_counter()
    diff = diff + ((time2_2 - time2_1) - diff) / 2
    time3_1 = time.perf_counter()
    await self.bot.edit_message(message, '| ᛫   | Ping! (**{0}ms**)'.format(round(diff * 1000)))
    time3_2 = time.perf_counter()
    diff = diff + ((time3_2 - time3_1) - diff) / 3
    time4_1 = time.perf_counter()
    await self.bot.edit_message(message, '|  ᛫  | Ping! (**{0}ms**)'.format(round(diff * 1000)))
    time4_2 = time.perf_counter()
    diff = diff + ((time4_2 - time4_1) - diff) / 4
    time5_1 = time.perf_counter()
    await self.bot.edit_message(message, '|   ᛫ | Ping! (**{0}ms**)'.format(round(diff * 1000)))
    time5_2 = time.perf_counter()
    diff = diff + ((time5_2 - time5_1) - diff) / 5
    time6_1 = time.perf_counter()
    await self.bot.edit_message(message, '|    ᛫| Ping! (**{0}ms**)'.format(round(diff * 1000)))
    time6_2 = time.perf_counter()
    diff = diff + ((time6_2 - time6_1) - diff) / 6
    # Apparently there's a thing called rate-limiting, and thus the following block of code cannot be executed together with the above
    
    # time7_1 = time.perf_counter()
    # await self.bot.edit_message(message, '|    ᛫| Ping! (**{0}ms**)'.format(round(diff * 1000)))
    # time7_2 = time.perf_counter()
    # diff = diff + ((time7_2 - time7_1) - diff) / 7
    # time8_1 = time.perf_counter()
    # await self.bot.edit_message(message, '|   ᛫ | Ping! (**{0}ms**)'.format(round(diff * 1000)))
    # time8_2 = time.perf_counter()
    # diff = diff + ((time8_2 - time8_1) - diff) / 8
    # time9_1 = time.perf_counter()
    # await self.bot.edit_message(message, '|  ᛫  | Ping! (**{0}ms**)'.format(round(diff * 1000)))
    # time9_2 = time.perf_counter()
    # diff = diff + ((time9_2 - time9_1) - diff) / 9
    # time10_1 = time.perf_counter()
    # await self.bot.edit_message(message, '| ᛫   | Ping! (**{0}ms**)'.format(round(diff * 1000)))
    # time10_2 = time.perf_counter()
    # diff = diff + ((time10_2 - time10_1) - diff) / 10
    # time11_1 = time.perf_counter()
    # await self.bot.edit_message(message, '|᛫    | Ping! (**{0}ms**)'.format(round(diff * 1000)))
    # time11_2 = time.perf_counter()
    # diff = diff + ((time11_2 - time11_1) - diff) / 11
    await self.bot.edit_message(message, 'Pong! (Average **{0}ms**)'.format(round(diff * 1000)))

def setup(bot):
  bot.add_cog(Ping(bot))