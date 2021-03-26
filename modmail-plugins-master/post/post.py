import typing
import re
import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel


class PostPlugin(commands.Cog):
    """
    Easily create plain text or embedded post
    """

    def __init__(self, bot):
        self.bot = bot
        self.db = bot.plugin_db.get_partition(self)

    @commands.group(aliases=["p"], invoke_without_command=True)
    @commands.guild_only()
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def post(self, ctx: commands.Context):
        """
        Make Post Easily
        """
        await ctx.send_help(ctx.command)

    @post.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def start(
        self,
        ctx: commands.Context,
        role: typing.Optional[discord.Role]
    ):
        """
        Start an interactive session to create post
        Add the role in the command if you want to enable mentions

        **Example:**
        __Post with role mention:__
        {prefix}post start everyone

        __Post without role mention__
        {prefix}post start
        """

        role_mention = f"<@&{role.id}>" if role else ""

        # TODO: Enable use of reactions
        def check(msg: discord.Message):
            return ctx.author == msg.author and ctx.channel == msg.channel

        # def check_reaction(reaction: discord.Reaction, user: discord.Member):
        #     return ctx.author == user and (str(reaction.emoji == "✅") or str(reaction.emoji) == "❌")

        def title_check(msg: discord.Message):
            return (
                ctx.author == msg.author
                and ctx.channel == msg.channel
                and (len(msg.content) < 256)
            )

        def description_check(msg: discord.Message):
            return (
                ctx.author == msg.author
                and ctx.channel == msg.channel
                and (len(msg.content) < 2048)
            )

        def footer_check(msg: discord.Message):
            return (
                ctx.author == msg.author
                and ctx.channel == msg.channel
                and (len(msg.content) < 2048)
            )

        # def author_check(msg: discord.Message):
        #     return (
        #             ctx.author == msg.author and ctx.channel == msg.channel and (len(msg.content) < 256)
        #     )

        def cancel_check(msg: discord.Message):
            if msg.content == "cancel" or msg.content == f"{ctx.prefix}cancel":
                return True
            else:
                return False

        if role:
            guild: discord.Guild = ctx.guild
            grole: discord.Role = guild.get_role(role.id)
            await grole.edit(mentionable=True)

        await ctx.send("Starting an interactive process to create an post")

        await ctx.send(
            embed=await self.generate_embed("Do you want it to be an embed? `[y/n]`")
        )

        embed_res: discord.Message = await self.bot.wait_for("message", check=check)
        if cancel_check(embed_res) is True:
            await ctx.send("Cancelled!")
            return
        elif cancel_check(embed_res) is False and embed_res.content.lower() == "n":
            await ctx.send(
                embed=await self.generate_embed(
                    "Okay, let's do a no-embed post."
                    "\nWhat's the post?"
                )
            )
            post = await self.bot.wait_for("message", check=check)
            if cancel_check(post) is True:
                await ctx.send("Cancelled!")
                return
            else:
                await ctx.send(
                    embed=await self.generate_embed(
                        "To which channel should I send the post?"
                    )
                )
                channel: discord.Message = await self.bot.wait_for(
                    "message", check=check
                )
                if cancel_check(channel) is True:
                    await ctx.send("Cancelled!")
                    return
                else:
                    if channel.channel_mentions[0] is None:
                        await ctx.send("Cancelled as no channel was provided")
                        return
                    else:
                        await channel.channel_mentions[0].send(
                            f"{role_mention}\n{post.content}"
                        )
        elif cancel_check(embed_res) is False and embed_res.content.lower() == "y":
            embed = discord.Embed()
            await ctx.send(
                embed=await self.generate_embed(
                    "Should the embed have a title? `[y/n]`"
                )
            )
            t_res = await self.bot.wait_for("message", check=check)
            if cancel_check(t_res) is True:
                await ctx.send("Cancelled")
                return
            elif cancel_check(t_res) is False and t_res.content.lower() == "y":
                await ctx.send(
                    embed=await self.generate_embed(
                        "What should the title of the embed be?"
                        "\n**Must not exceed 256 characters**"
                    )
                )
                tit = await self.bot.wait_for("message", check=title_check)
                embed.title = tit.content
            await ctx.send(
                embed=await self.generate_embed(
                    "Should the embed have a description?`[y/n]`"
                )
            )
            d_res: discord.Message = await self.bot.wait_for("message", check=check)
            if cancel_check(d_res) is True:
                await ctx.send("Cancelled")
                return
            elif cancel_check(d_res) is False and d_res.content.lower() == "y":
                await ctx.send(
                    embed=await self.generate_embed(
                        "What do you want as the description for the embed?"
                        "\n**Must not exceed 2048 characters**"
                    )
                )
                des = await self.bot.wait_for("message", check=description_check)
                embed.description = des.content

            await ctx.send(
                embed=await self.generate_embed(
                    "Should the embed have a thumbnail?`[y/n]`"
                )
            )
            th_res: discord.Message = await self.bot.wait_for("message", check=check)
            if cancel_check(th_res) is True:
                await ctx.send("Cancelled")
                return
            elif cancel_check(th_res) is False and th_res.content.lower() == "y":
                await ctx.send(
                    embed=await self.generate_embed(
                        "What'sthe thumbnail of the embed? Enter a " "valid URL"
                    )
                )
                thu = await self.bot.wait_for("message", check=check)
                embed.set_thumbnail(url=thu.content)

            await ctx.send(
                embed=await self.generate_embed("Should the embed have a image?`[y/n]`")
            )
            i_res: discord.Message = await self.bot.wait_for("message", check=check)
            if cancel_check(i_res) is True:
                await ctx.send("Cancelled")
                return
            elif cancel_check(i_res) is False and i_res.content.lower() == "y":
                await ctx.send(
                    embed=await self.generate_embed(
                        "What's the image of the embed? Enter a " "valid URL"
                    )
                )
                i = await self.bot.wait_for("message", check=check)
                embed.set_image(url=i.content)

            await ctx.send(
                embed=await self.generate_embed("Will the embed have a footer?`[y/n]`")
            )
            f_res: discord.Message = await self.bot.wait_for("message", check=check)
            if cancel_check(f_res) is True:
                await ctx.send("Cancelled")
                return
            elif cancel_check(f_res) is False and f_res.content.lower() == "y":
                await ctx.send(
                    embed=await self.generate_embed(
                        "What do you want the footer of the embed to be?"
                        "\n**Must not exceed 2048 characters**"
                    )
                )
                fooo = await self.bot.wait_for("message", check=footer_check)
                embed.set_footer(text=fooo.content)

            await ctx.send(
                embed=await self.generate_embed(
                    "Do you want it to have a color?`[y/n]`"
                )
            )
            c_res: discord.Message = await self.bot.wait_for("message", check=check)
            if cancel_check(c_res) is True:
                await ctx.send("Cancelled!")
                return
            elif cancel_check(c_res) is False and c_res.content.lower() == "y":
                await ctx.send(
                    embed=await self.generate_embed(
                        "What color should the embed have? "
                        "Please provide a valid hex color"
                    )
                )
                colo = await self.bot.wait_for("message", check=check)
                if cancel_check(colo) is True:
                    await ctx.send("Cancelled!")
                    return
                else:
                    match = re.search(
                        r"^#(?:[0-9a-fA-F]{3}){1,2}$", colo.content
                    )  # uwu thanks stackoverflow
                    if match:
                        embed.colour = int(
                            colo.content.replace("#", "0x"), 0
                        )  # Basic Computer Science
                    else:
                        await ctx.send(
                            "Failed! Not a valid hex color, get yours from "
                            "https://www.google.com/search?q=color+picker"
                        )
                        return

            await ctx.send(
                embed=await self.generate_embed(
                    "In which channel should I send the post?"
                )
            )
            channel: discord.Message = await self.bot.wait_for("message", check=check)
            if cancel_check(channel) is True:
                await ctx.send("Cancelled!")
                return
            else:
                if channel.channel_mentions[0] is None:
                    await ctx.send("Cancelled as no channel was provided")
                    return
                else:
                    schan = channel.channel_mentions[0]
            await ctx.send(
                "Here is how the embed looks like: Send it? `[y/n]`", embed=embed
            )
            s_res = await self.bot.wait_for("message", check=check)
            if cancel_check(s_res) is True or s_res.content.lower() == "n":
                await ctx.send("Cancelled")
                return
            else:
                await schan.send(f"{role_mention}", embed=embed)
        if role:
            guild: discord.Guild = ctx.guild
            grole: discord.Role = guild.get_role(role.id)
            if grole.mentionable is True:
                await grole.edit(mentionable=False)

    @post.command(aliases=["native", "n", "q"])
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def quick(
        self,
        ctx: commands.Context,
        channel: discord.TextChannel,
        role: typing.Optional[discord.Role],
        *,
        msg: str,
    ):
        """
        An old way of making post

        **Usage:**
        {prefix}post quick #channel <OPTIONAL role> message
        """
        if role:
            guild: discord.Guild = ctx.guild
            grole: discord.Role = guild.get_role(role.id)
            await grole.edit(mentionable=True)

        role_mention = f"<@&{role.id}>" if role else ""

        await channel.send(f"{role_mention}\n{msg}")

        if role:
            guild: discord.Guild = ctx.guild
            grole: discord.Role = guild.get_role(role.id)
            if grole.mentionable is True:
                await grole.edit(mentionable=False)

    @post.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def edit(
        self,
        ctx: commands.Context,
        role: typing.Optional[discord.Role],
        messageedit: int
    ):
        """
        Edit an existen bot messagge with an interactive session to create post
        Add the role in the command if you want to enable mentions

        **Example:**
        __Post with role mention:__
        {prefix}post edit everyone 639866916432773120

        __Post without role mention__
        {prefix}post edit 639866916432773120
        """
        if messageedit:
            guild: discord.Guild = ctx.guild
            message = ""
            for channel in guild.text_channels:
                message = channel.fetch_message(messageedit)
            if message:
                pass
            else:
                await ctx.send("Cancelled : You don't put a valid message.")
                return
        else:
            await ctx.send("Cancelled : You don't put a valid message.")
            return

        role_mention = f"<@&{role.id}>" if role else ""

        # TODO: Enable use of reactions
        def check(msg: discord.Message):
            return ctx.author == msg.author and ctx.channel == msg.channel

        # def check_reaction(reaction: discord.Reaction, user: discord.Member):
        #     return ctx.author == user and (str(reaction.emoji == "✅") or str(reaction.emoji) == "❌")

        def title_check(msg: discord.Message):
            return (
                ctx.author == msg.author
                and ctx.channel == msg.channel
                and (len(msg.content) < 256)
            )

        def description_check(msg: discord.Message):
            return (
                ctx.author == msg.author
                and ctx.channel == msg.channel
                and (len(msg.content) < 2048)
            )

        def footer_check(msg: discord.Message):
            return (
                ctx.author == msg.author
                and ctx.channel == msg.channel
                and (len(msg.content) < 2048)
            )

        # def author_check(msg: discord.Message):
        #     return (
        #             ctx.author == msg.author and ctx.channel == msg.channel and (len(msg.content) < 256)
        #     )

        def cancel_check(msg: discord.Message):
            if msg.content == "cancel" or msg.content == f"{ctx.prefix}cancel":
                return True
            else:
                return False

        if role:
            guild: discord.Guild = ctx.guild
            grole: discord.Role = guild.get_role(role.id)
            await grole.edit(mentionable=True)

        await ctx.send("Starting an interactive process to create an post")

        await ctx.send(
            embed=await self.generate_embed("Do you want it to be an embed? `[y/n]`")
        )

        embed_res: discord.Message = await self.bot.wait_for("message", check=check)
        if cancel_check(embed_res) is True:
            await ctx.send("Cancelled!")
            return
        elif cancel_check(embed_res) is False and embed_res.content.lower() == "n":
            await ctx.send(
                embed=await self.generate_embed(
                    "Okay, let's do a no-embed post."
                    "\nWhat's the post?"
                )
            )
            post = await self.bot.wait_for("message", check=check)
            if cancel_check(post) is True:
                await ctx.send("Cancelled!")
                return
            else:
                await ctx.send(
                    embed=await self.generate_embed(
                        "To which channel should I send the post?"
                    )
                )
                channel: discord.Message = await self.bot.wait_for(
                    "message", check=check
                )
                if cancel_check(channel) is True:
                    await ctx.send("Cancelled!")
                    return
                else:
                    if channel.channel_mentions[0] is None:
                        await ctx.send("Cancelled as no channel was provided")
                        return
                    else:
                        await channel.channel_mentions[0].send(
                            f"{role_mention}\n{post.content}"
                        )
        elif cancel_check(embed_res) is False and embed_res.content.lower() == "y":
            embed = discord.Embed()
            await ctx.send(
                embed=await self.generate_embed(
                    "Should the embed have a title? `[y/n]`"
                )
            )
            t_res = await self.bot.wait_for("message", check=check)
            if cancel_check(t_res) is True:
                await ctx.send("Cancelled")
                return
            elif cancel_check(t_res) is False and t_res.content.lower() == "y":
                await ctx.send(
                    embed=await self.generate_embed(
                        "What should the title of the embed be?"
                        "\n**Must not exceed 256 characters**"
                    )
                )
                tit = await self.bot.wait_for("message", check=title_check)
                embed.title = tit.content
            await ctx.send(
                embed=await self.generate_embed(
                    "Should the embed have a description?`[y/n]`"
                )
            )
            d_res: discord.Message = await self.bot.wait_for("message", check=check)
            if cancel_check(d_res) is True:
                await ctx.send("Cancelled")
                return
            elif cancel_check(d_res) is False and d_res.content.lower() == "y":
                await ctx.send(
                    embed=await self.generate_embed(
                        "What do you want as the description for the embed?"
                        "\n**Must not exceed 2048 characters**"
                    )
                )
                des = await self.bot.wait_for("message", check=description_check)
                embed.description = des.content

            await ctx.send(
                embed=await self.generate_embed(
                    "Should the embed have a thumbnail?`[y/n]`"
                )
            )
            th_res: discord.Message = await self.bot.wait_for("message", check=check)
            if cancel_check(th_res) is True:
                await ctx.send("Cancelled")
                return
            elif cancel_check(th_res) is False and th_res.content.lower() == "y":
                await ctx.send(
                    embed=await self.generate_embed(
                        "What'sthe thumbnail of the embed? Enter a " "valid URL"
                    )
                )
                thu = await self.bot.wait_for("message", check=check)
                embed.set_thumbnail(url=thu.content)

            await ctx.send(
                embed=await self.generate_embed("Should the embed have a image?`[y/n]`")
            )
            i_res: discord.Message = await self.bot.wait_for("message", check=check)
            if cancel_check(i_res) is True:
                await ctx.send("Cancelled")
                return
            elif cancel_check(i_res) is False and i_res.content.lower() == "y":
                await ctx.send(
                    embed=await self.generate_embed(
                        "What's the image of the embed? Enter a " "valid URL"
                    )
                )
                i = await self.bot.wait_for("message", check=check)
                embed.set_image(url=i.content)

            await ctx.send(
                embed=await self.generate_embed("Will the embed have a footer?`[y/n]`")
            )
            f_res: discord.Message = await self.bot.wait_for("message", check=check)
            if cancel_check(f_res) is True:
                await ctx.send("Cancelled")
                return
            elif cancel_check(f_res) is False and f_res.content.lower() == "y":
                await ctx.send(
                    embed=await self.generate_embed(
                        "What do you want the footer of the embed to be?"
                        "\n**Must not exceed 2048 characters**"
                    )
                )
                fooo = await self.bot.wait_for("message", check=footer_check)
                embed.set_footer(text=fooo.content)

            await ctx.send(
                embed=await self.generate_embed(
                    "Do you want it to have a color?`[y/n]`"
                )
            )
            c_res: discord.Message = await self.bot.wait_for("message", check=check)
            if cancel_check(c_res) is True:
                await ctx.send("Cancelled!")
                return
            elif cancel_check(c_res) is False and c_res.content.lower() == "y":
                await ctx.send(
                    embed=await self.generate_embed(
                        "What color should the embed have? "
                        "Please provide a valid hex color"
                    )
                )
                colo = await self.bot.wait_for("message", check=check)
                if cancel_check(colo) is True:
                    await ctx.send("Cancelled!")
                    return
                else:
                    match = re.search(
                        r"^#(?:[0-9a-fA-F]{3}){1,2}$", colo.content
                    )  # uwu thanks stackoverflow
                    if match:
                        embed.colour = int(
                            colo.content.replace("#", "0x"), 0
                        )  # Basic Computer Science
                    else:
                        await ctx.send(
                            "Failed! Not a valid hex color, get yours from "
                            "https://www.google.com/search?q=color+picker"
                        )
                        return

            await ctx.send(
                "Here is how the embed looks like: Send it? `[y/n]`", embed=embed
            )
            s_res = await self.bot.wait_for("message", check=check)
            if cancel_check(s_res) is True or s_res.content.lower() == "n":
                await ctx.send("Cancelled")
                return
            else:
                guild: discord.Guild = ctx.guild
                message = discord.Message
                channelv = discord.TextChannel
                for channel in guild.text_channels:
                    message: discord.Message = channel.fetch_message(messageedit)
                    channelv: discord.TextChannel = channel
                await ctx.send(
                    embed=await self.generate_embed("Edited ! (https://discordapp.com/channels/{}/{}/{})".format(guild.id, channelv.id, message.id))
                )
                await message.edit(embed=embed)
        if role:
            guild: discord.Guild = ctx.guild
            grole: discord.Role = guild.get_role(role.id)
            if grole.mentionable is True:
                await grole.edit(mentionable=False)
    @commands.Cog.listener()
    async def on_ready(self):
        pass
    @staticmethod
    async def generate_embed(description: str):
        embed = discord.Embed()
        embed.colour = discord.Colour.blurple()
        embed.description = description

        return embed


def setup(bot):
    bot.add_cog(PostPlugin(bot))
