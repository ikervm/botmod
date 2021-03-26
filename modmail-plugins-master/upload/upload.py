import asyncio, discord, re
from discord.ext import commands

class Upload(commands.Cog):

    def __init__(self, bot):
        self.bot = bot      

    @commands.command()
    @commands.guild_only()
    async def upload(self, ctx, *, links: str=None):
        message = ctx.message
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', links)
        if len(urls) > 0:
            buff = ''
            for url in urls:
                if len(url) + len(buff) > 1990:
                    await ctx.send('{}'.format(buff))
                    buff = ''
                buff += '\n{}'.format(url)
            if not buff:
                return
            
            return await ctx.send('{}'.format(buff))
        elif len(message.attachments) > 0:
            await ctx.channel.send(message.attachments[0])
        else:
            await ctx.channel.send("Merci de renseigner une image à upload")
            

def setup(bot):
    bot.add_cog(Upload(bot))
