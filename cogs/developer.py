from discord.ext.commands import command, group, Context, Cog
from backend import BOT, SELF, USER
from discord import Member, User, Guild, TextChannel
from typing import Union

class Developer(Cog):
    def __init__(self: SELF, bot: BOT):
        self.bot = bot

    async def cog_check(self: SELF, ctx: Context):
        if ctx.author.id not in self.bot.owner_ids:
            return False
        else:
            return True
        
    @command(name = "blacklist", description = "blacklist a user, channel, or guild", aliases = ("bl",))
    async def blacklist(self: SELF, ctx: Context, *, object_: Union[Member, User, Guild, TextChannel])
        object_type = str(type(object_)).split(".")[1].replace("member", "user")
        await self.bot.db.execute("""INSERT INTO blacklist (object_id, object_type) VALUES($1, $2) ON CONFLICT(object_id, object_type) DO NOTHING""", object_.id, object_type)
        return await ctx.success(f"successfully **blacklisted** {object_.mention if isinstance(object_, (Member, User)) else object_.id}")
    
    @command(name = "unblacklist", description = "unblacklist a user, channel, or guild", aliases = ("unbl", "ubl",))
    async def unblacklist(self: SELF, ctx: Context, *, object_: Union[Member, User, Guild, TextChannel]) -> None:
        object_type = str(type(object_)).split(".")[1].replace("member", "user")
        await self.bot.db.execute("""DELETE FROM blacklist WHERE object_id = $1 AND object_type = $2""", object_.id, object_type)
        return await ctx.success(f"Successfully **unblacklisted** {object_.mention if isinstance(object_, (Member, User)) else object_.id}")
    

async def setup(bot: BOT):
    await bot.add_cog(Developer(bot))