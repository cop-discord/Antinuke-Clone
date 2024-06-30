from discord import User, Member, Embed
from discord.ext.commands import command, group, Context, Cog
from backend import BOT, SELF, USER

class utility(Cog):
    def __init__(self: SELF, bot: BOT):
        self.bot = bot

    @command(name = "afk", aliases=["away", "zzz"], description = "go away from discord")
    async def afk(self: SELF, ctx: Context, *, reason: str = None):
        reason = reason if reason else "AFK"
        await self.bot.db.execute("INSERT INTO afk (user_id, reason) VALUES ($1, $2)", ctx.author.id, reason)
        await ctx.success(f"{ctx.author.mention} you're now afk with reason: **{reason}**")

    @Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        away = await self.bot.db.fetchval("SELECT reason FROM afk WHERE user_id = $1", message.author.id)
        if away:
            await self.bot.db.execute("DELETE FROM afk WHERE user_id = $1", message.author.id)
            embed = Embed(description=f"{message.author.mention} you're not longer **afk**", color=self.bot.color)
            await message.channel.send(embed=embed)
        for user in message.mentions:
            away = await self.bot.db.fetchval("SELECT reason FROM afk WHERE user_id = $1", user.id)
            if away:
                embed = Embed(description=f"{user.mention} is currently **{away}**", color=self.bot.color)
                await message.channel.send(embed=embed)

async def setup(bot: BOT):
    await bot.add_cog(utility(bot))
