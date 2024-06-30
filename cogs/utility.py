from discord import User, Member, Embed
from discord.ext.commands import command, Context, Cog
from backend import BOT, SELF, USER
from backend.listeners import listeners
class utility(Cog):
    def __init__(self: SELF, bot: BOT):
        self.bot = bot

    @command(name = "afk", aliases=["away", "zzz"], description = "go away from discord")
    async def afk(self: SELF, ctx: Context, *, reason: str = None):
        reason = reason if reason else "AFK"
        await self.bot.db.execute("INSERT INTO afk (user_id, reason) VALUES ($1, $2)", ctx.author.id, reason)
        await ctx.success(f"{ctx.author.mention} you're now afk with reason: **{reason}**")

async def setup(bot: BOT):
    await bot.add_cog(utility(bot))
    awaut bot.add_cog(listeners(bot))

