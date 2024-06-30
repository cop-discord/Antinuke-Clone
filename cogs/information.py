from discord import User, Member, Embed, ButtonStyle, Permissions, utils, SelectOption, Interaction
from discord.ui import View, Button, button, Select
from discord.ext.commands import command, group, Context, Cog, Command, Group, Author
from backend import BOT, SELF, USER
from typing import Dict, Any

class Help(Select):
    def __init__(self: SELF, bot: BOT, author: USER, options: Dict[str, Any]):
        self._options = options
        self.author = author
        options = [
            SelectOption(label = _, description = f"{_} cmds") for _ in options
        ]
        super().__init__(custom_id = "help", placeholder="commands", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        if interaction.user != self.author:
            return await interaction.response.send_message("you aren't the author of this command", ephemeral = True)
        value = self.values[0]
        await interaction.message.edit(embed = self._options[value])
        return await interaction.response.defer()



class Information(Cog):
    def __init__(self: SELF, bot: BOT):
        self.bot = bot

    @command(name = "avatar", description = "get the avatar of a user or member")
    async def avatar(self: SELF, ctx: Context, *, user: User = Author):
        embed = Embed(color = self.bot.color, title = f"{user.name}'s avatar", url = f"https://discord.com/users/{user.id}")
        embed.set_author(name = str(ctx.author), icon_url = ctx.author.display_avatar.url)
        embed.set_image(url = user.display_avatar.url)
        embed.set_footer(text = f"server: {str(ctx.guild.name)}, ,avatar (user id)")
        view = View()
        view.add_item(Button(label = "PNG", url = user.display_avatar.with_format("png").url))
        view.add_item(Button(label = "WEBP", url = user.display_avatar.with_format("webp").url))
        view.add_item(Button(label = "JPG", url = user.display_avatar.with_format("jpg").url))
        return await ctx.send(embed = embed, view = view)
    
    @command(name = "banner", description = "get the banner of a user or member")
    async def banner(self: SELF, ctx: Context, *, user: User = Author):
        user = await self.bot.fetch_user(user.id)
        if not user.banner:
            return await ctx.fail(f"{ctx.author.mention}, **{user.name}** doesn't have a banner.")
        embed = Embed(color = self.bot.color, title = f"{user.name}'s banner", url = f"https://discord.com/users/{user.id}")
        embed.set_author(name = str(ctx.author), icon_url = ctx.author.display_avatar.url)
        embed.set_image(url = user.banner.url)
        kwargs = {"text": f"server: {str(ctx.guild.name)}, ,avatar (user id)"}
        if ctx.guild.icon:
            kwargs["icon_url"] = ctx.guild.icon.url
        embed.set_footer(**kwargs)
        view = View()
        view.add_item(Button(label = "PNG", url = user.banner.with_format("png").url))
        view.add_item(Button(label = "WEBP", url = user.banner.with_format("webp").url))
        view.add_item(Button(label = "JPG", url = user.banner.with_format("jpg").url))
        return await ctx.send(embed = embed, view = view)
    
    @command(name = "help", description = "get the command list")
    async def help(self: SELF, ctx: Context):
        embed = Embed()
        view = View()
        embed.set_author(name = str(ctx.author), icon_url = ctx.author.display_avatar.url)
        embed.description = f"used by over **{len(self.bot.users)}** users in **{len(self.bot.guilds)}** servers\n**prefix:** `{ctx.prefix}`"
        kwargs = {"text": f"server: {str(ctx.guild.name)}"}
        if ctx.guild.icon:
            kwargs["icon_url"] = ctx.guild.icon.url
        embed.set_footer(**kwargs)
        view.add_item(Button(label = "invite", url = utils.oauth_url(self.bot.user.id, permissions = Permissions(8), scopes = ["bot"])))
        view.add_item(Button(label = "socials", url = "https://rival.rocks/"))
        cogs = sorted(
            (
                cog for cog in self.bot.cogs.values()
                if cog.get_commands() and getattr(cog, "hidden", False) is False
                and cog.qualified_name not in ("Jishaku", "Developer")
            ), 
            key=lambda cog: cog.qualified_name
        )

        cog_count = len(cogs)
        embeds = {"back": embed}
        embeds.update({cog.qualified_name:
            (
                Embed(
                    color=self.bot.color,
                    title=f"{cog.qualified_name}",
                    description=f"```{', '.join(cmd.name + ('*' if isinstance(cmd, Group) else '') for cmd in cog.get_commands())}```",
                )
                .set_author(
                    name=f"{str(ctx.author)}", 
                    icon_url=ctx.author.display_avatar
                )
                .set_footer(text=f"server: {ctx.guild.name}")
            )
            for index, cog in enumerate(cogs, start=2)
        })
        dropdown = Help(self.bot, ctx.author, embeds)
        view.add_item(dropdown)
        return await ctx.send(embed = embed, view = view)

    
async def setup(bot: BOT):
    await bot.add_cog(Information(bot))
