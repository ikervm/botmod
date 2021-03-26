from discord import Member
from discord.ext import commands

class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['calin', 'câlin'])
    @commands.guild_only()
    async def hug(self, ctx, member: Member):
        await ctx.send(f":information_source: {member.mention} tu a reçu un gros calin de la part de {ctx.author.mention} <a:awumpusheart:622779992258117674>")
        await ctx.message.delete()
    
    @commands.command(aliases=['bisou'])
    @commands.guild_only()
    async def kiss(self, ctx, member: Member):
        await ctx.send(f":information_source: {member.mention} tu a reçu un gros bisou de la part de {ctx.author.mention} <:SmileyKissing:616036828038037504>")
        await ctx.message.delete()
    
    @kiss.error
    async def kiss_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Désolé {ctx.author.mention}, mais je n'ai pas trouvé d'utilisateur à hug :(")
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"Désolé {ctx.author.mention}, mais il faut que tu mentionne ou que tu donne l'id de l'utilisateur à hug")
        else:
            print(error.__class__.__name__, ':', str(error))

    @hug.error
    async def hug_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Désolé {ctx.author.mention}, mais je n'ai pas trouvé d'utilisateur à hug :(")
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"Désolé {ctx.author.mention}, mais il faut que tu mentionne ou que tu donne l'id de l'utilisateur à hug")
        else:
            print(error.__class__.__name__, ':', str(error))
    
def setup(bot):
    bot.add_cog(MyCog(bot))
