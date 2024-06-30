
from discord import User, Member, Embed, PermissionOverwrite
from discord.ext.commands import command, Context, Cog, Group
from backend import BOT, SELF, USER
from backend.links import linky

class Moderation(Cog):
    def __init__(self: SELF, bot: BOT):
        self.bot = bot
        
    @group(name="clear", invoke_without_command=True)
    async def clear(self: SELF, ctx: Context):
        return
#        return await ctx.pages() # you do the fucking pages nigger

    @clear.command(name="links", aliases=["link"], description="clear all links from chat")
    async def links(self: SELF, ctx: Context, limit: int):
        if limit > 100:
            await ctx.fail("you can only delete 100 messages at a time")
            return
        await ctx.channel.purge(limit=limit, check=lambda m: linky(m.content), reason=f"purged by {ctx.author}")

    @clear.command(name="invites", aliases=["invite"], description="clear all discord invites")
    async def invites(self: SELF, ctx: Context, limit: int):
        if limit > 100:
            await ctx.fail("you can only delete 100 messages at a time")
            return
        regex = r"discord(?:\.com|app\.com|\.gg)/(?:invite/)?([a-zA-Z0-9\-]{2,32})"
        await ctx.channel.purge(limit=limit, check=lambda m: re.search(regex, m.content), reason=f"purged by {ctx.author}")
        
    @clear.command(name="contains", aliases=["has"], description="clear messages containing a specific phrase")
    async def contains(self: SELF, ctx: Context, limit: int, *, word: str):
        if limit > 100:
            await ctx.fail("you can only delete 100 messages at a time")
            return
        await ctx.channel.purge(limit=limit, check=lambda m: word in m.content, reason=f"the messages containing the word'{word}' was purged by {ctx.author}")
        
    @clear.command(name="images", aliases=["image"], description="clear images from chat")
    async def images(self: SELF, ctx: Context, limit: int):
        if limit > 100:
            await ctx.fail("you can only delete 100 messages at a time")
            return
        await ctx.channel.purge(limit=limit, check=lambda m: m.attachments, reason=f"purged by {ctx.author}")

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
    await bot.add_cog(Moderation(bot))
