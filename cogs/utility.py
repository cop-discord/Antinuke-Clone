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

    @command(name="rmute", aliases=["rm"], description="remove permissions to add reaction in all channels")
    async def rmute(self: SELF, ctx: Context, user: USER):
        for channel in ctx.guild.channels:
            await channel.set_permissions(user, add_reactions=False)
        await ctx.success(f"{user.mention} has been revoked from adding reactions anywhere")

    @command(name="rmute", aliases=["ru"], description="unreaction mute a discordian")
    async def runmute(self: SELF, ctx: Context, user: USER):
        for channel in ctx.guild.channels:
            await channel.set_permissions(user, overwrite=None)
        await ctx.success(f"{user.mention} has allowed to react again")

async def setup(bot: BOT):
    await bot.add_cog(Utility(bot))
    await bot.add_cog(listeners(bot))
