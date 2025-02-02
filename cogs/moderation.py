
from discord import User, Member, Embed, PermissionOverwrite
from discord.ext.commands import command, Context, Cog, Group, group, has_permissions
from backend import BOT, SELF, USER
from backend.links import linky
import re

class Moderation(Cog):
    def __init__(self: SELF, bot: BOT):
        self.bot = bot
        
    @group(name="clear", invoke_without_command=True)
    @has_permissions(manage_messages=True)
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
        await ctx.channel.purge(limit=limit, check=lambda m: word in m.content, reason=f"the messages containing the word '{word}' was purged by {ctx.author}")
        
    @clear.command(name="images", aliases=["image"], description="clear images from chat")
    async def images(self: SELF, ctx: Context, limit: int):
        if limit > 100:
            await ctx.fail("you can only delete 100 messages at a time")
            return
        await ctx.channel.purge(limit=limit, check=lambda m: m.attachments, reason=f"purged by {ctx.author}")

    @command(name="rmute", aliases=["rm"], description="remove permissions to add reaction in all channels")
    @has_permissions(manage_messages=True)
    async def rmute(self: SELF, ctx: Context, user: USER):
        muted = all(channel.overwrites_for(user).add_reactions is False for channel in ctx.guild.channels)
        if muted:
            await ctx.fail(f"{user.mention} is already reaction muted in all channels")
        else:
            for channel in ctx.guild.channels:
                if channel.overwrites_for(user).add_reactions is not False:
                    await channel.set_permissions(user, add_reactions=False)
            await ctx.success(f"{user.mention} has been revoked from adding reactions anywhere")

    @command(name="runmute", aliases=["ru"], description="unreaction mute a discordian")
    @has_permissions(manage_messages=True)
    async def runmute(self: SELF, ctx: Context, user: USER):
        muted = all(channel.overwrites_for(user).add_reactions is False for channel in ctx.guild.channels)
        if not muted:
            await ctx.fail(f"{user.mention} is not reaction muted")
        else:
            for channel in ctx.guild.channels:
                if channel.overwrites_for(user).add_reactions is False:
                    await channel.set_permissions(user, overwrite=None)
            await ctx.success(f"{user.mention} has allowed to react again")

async def setup(bot: BOT):
    await bot.add_cog(Moderation(bot))
