<<<<<<< HEAD
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
=======
from discord import User, Member, Embed, PermissionOverwrite
from discord.ext.commands import command, Context, Cog
from backend import BOT, SELF, USER
from backend.listeners import listeners

class Utility(Cog):
    def __init__(self: SELF, bot: BOT):
        self.bot = bot

    @command(name = "afk", aliases=["away", "zzz"], description = "go away from discord")
    async def afk(self: SELF, ctx: Context, *, reason: str = None):
        reason = reason if reason else "AFK"
        await self.bot.db.execute("INSERT INTO afk (user_id, reason) VALUES ($1, $2)", ctx.author.id, reason)
        await ctx.success(f"{ctx.author.mention} you're now afk with reason: **{reason}**")
>>>>>>> 50831cbdcf4914dd7554f1b201f65c9885459a9c

async def setup(bot: BOT):
    await bot.add_cog(Utility(bot))
    await bot.add_cog(listeners(bot))
