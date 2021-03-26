import asyncio, discord
from   discord.ext import commands
from   discord     import Forbidden

class Channel(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    MediaChannel: int = 0
    
    @commands.group(aliases=["meida"], invoke_without_command=True)
    @commands.guild_only()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def media(self, ctx: commands.Context, mediaid: int):
        MediaChannel: int = mediaid
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == MediaChannel:
            await message.channel.send(len(message.content))

def setup(bot):
    bot.add_cog(Channel(bot))
