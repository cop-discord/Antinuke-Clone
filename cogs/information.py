from discord import User, Member, Embed, ButtonStyle
from discord.ui import View, Button, button
from discord.ext.commands import command, group, Context, Cog
from backend import BOT, SELF, USER

class Information(Cog):
    def __init__(self: SELF, bot: BOT):
        self.bot = bot

    @command(name = "avatar", description = "get the avatar of a user or member")
    async def avatar(self: SELF, ctx: Context, *, user: USER):
        embed = Embed(color = self.bot.color, title = f"{user.name}'s avatar", url = f"https://discord.com/users/{user.id}")
        embed.set_author(name = str(ctx.author), icon_url = ctx.author.display_avatar.url)
        embed.set_image(url = user.display_avatar.url)
        embed.set_footer(text = f"server: {str(ctx.guild.name)}, ,avatar (user id)")
        view = View()
        view.add_item(Button(label = "PNG", url = user.display_avatar.with_format("PNG").url))
        view.add_item(Button(label = "WEBP", url = user.display_avatar.with_format("WEBP").url))
        view.add_item(Button(label = "JPG", url = user.display_avatar.with_format("JPG").url))
        return await ctx.send(embed = embed, view = view)
    
    @command(name = "banner", description = "get the banner of a user or member")
    async def banner(self: SELF, ctx: Context, *, user: USER):
        user = await self.bot.fetch_user(user.id)
        if not user.banner:
            return await ctx.fail(f"{ctx.author.mention}, **{user.name}** doesn't have a banner.")
        embed = Embed(color = self.bot.color, title = f"{user.name}'s banner", url = f"https://discord.com/users/{user.id}")
        embed.set_author(name = str(ctx.author), icon_url = ctx.author.display_avatar.url)
        embed.set_image(url = user.banner.url)
        embed.set_footer(text = f"server: {str(ctx.guild.name)}, ,avatar (user id)")
        view = View()
        view.add_item(Button(label = "PNG", url = user.banner.with_format("PNG").url))
        view.add_item(Button(label = "WEBP", url = user.banner.with_format("WEBP").url))
        view.add_item(Button(label = "JPG", url = user.banner.with_format("JPG").url))
        return await ctx.send(embed = embed, view = view)

    @command(name = "userinfo", description = "fetch basic information on a given userid or username")
    async def userinfo(self, ctx: Context, *, user: User = None):
        if user is None:
            if ctx.message.mentions:
                user = ctx.message.mentions[0]
            else:
                user = await self.bot.fetch_user(ctx.message.content.split()[-1])
        mutual_guilds = [guild for guild in self.bot.guilds if guild.get_member(user.id)]
        embed = Embed(color=self.bot.color)
        embed.set_thumbnail(url=user.avatar.url)
        embed.add_field(name="Joined Discord", value=f"<t:{int(user.created_at.timestamp())}:f>")
        if isinstance(user, Member):
            embed.title = f"{user.display_name} @{user.name}"
            embed.add_field(name="joined server", value=f"<t:{int(user.joined_at.timestamp())}:f>")
        else:
            embed.title = f"{user.name}"
        embed.set_footer(text=f"mutual guilds: {len(mutual_guilds)}")
        embed.set_author(name=str(user.id), icon_url=user.avatar.url)
        await ctx.send(embed=embed)


async def setup(bot: BOT):
    await bot.add_cog(Information(bot))

