from discord import Embed, Message
from backend import SELF, BOT
from discord.ext.commands import Cog

class listeners(Cog):
    def __init__(self: SELF, bot: BOT):
        self.bot = bot

    @Cog.listener()
    async def on_message(self: SELF, message: Message):
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
