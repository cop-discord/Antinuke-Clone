from discord import Member, User, Embed, utils
from discord.ext.commands import group, Context, Cog, AutoShardedBot, Bot, Author, command
from datetime import datetime
from backend import SELF, BOT, USER

class utility(Cog):
    def __init__(self: SELF, bot: BOT):
        self.bot = bot

    @command(name="userinfo", aliases=["ui", "user"], description="fetch basic info from a given user id or username")
    async def userinfo(self, ctx: Context, *, user: USER = Author):
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

async def setup(bot):
    await bot.add_cog(utility(bot))
