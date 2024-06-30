from discord import User, Member, Embed
from discord.ext.commands import command, group, Context, Cog
from backend import BOT, SELF, USER

class utility(Cog):
    def __init__(self: SELF, bot: BOT):
        self.bot = bot

    @command(name = "afk", aliases=["away", "zzz"], description = "finally get away from discord")
    async def afk(self: SELF, ctx: Context, *, user: USER):


async def setup(bot: BOT):
    await bot.add_cog(utility(bot))
