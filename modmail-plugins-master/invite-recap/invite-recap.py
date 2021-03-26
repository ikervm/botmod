from discord import Member
from discord.ext import commands
import asyncio

class MyCog(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot
    self.joins = 0
    self.recap_channel = 698185668047667232

  @commands.command()
  async def inviterecapcr(self, ctx: commands.Context):
    async def task():
      while True:
        await self.bot.get_channel(self.recap_channel).send(f'> **{self.joins}** new members in the last hour')
        await asyncio.sleep(300)    
  
    await self.bot.loop.create_task(task())

  @commands.Cog.listener()
  async def on_member_join(self, member):
    self.joins = self.joins + 1

def setup(bot):
  bot.add_cog(MyCog(bot))
