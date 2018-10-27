import sys
sys.path.append("..")
# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import sys to import from parent directory
# Import Sakanya Core
from core import SakanyaCore


class Timeout():
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  @commands.check(SakanyaCore().is_owner)
  async def timeout(self, user: discord.Member, minutes, *, reason):
    """
    Timeout a specific user for a set amount of time.
    When timeouts go active, the user is first sent to a channel dedicated to that person,
    where a message from Sakanya says that they are timed out.
    Once they agree to this by pressing a reaction, they are allowed to browse the channels but 
    not post anything in them, until the timeout is reached, which is when they are given full 
    permission to participate in the discussion again. 
    
    Format:
      >timeout <username> 30 [Reason goes here]

    Examples:
      >love @Cyan 15 You have been a bad boy! This command restricts them for 15 minutes.
    """
    print(user)


def setup(bot):
  bot.add_cog(Timeout(bot))
