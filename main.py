from discord.ext.commands import Bot, Context, CommandError, MissingPermissions, when_mentioned_or  # noqa: F401
from discord import Embed, Message, Guild, Intents, User
import config
import traceback, asyncio, discord
from pathlib import Path
from loguru import logger
from sys import stdout
from tools import ratelimit, lock  # noqa: F401
from backend.database import Database
from backend.browser import Session
import os

os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_FORCE_PAGINATOR"] = "True"
os.environ["JISHAKU_RETAIN"] = "True"

async def success(self: Context, message: str) -> Message:
    return await self.send(embed = Embed(color = self.bot.color, description = message))

async def fail(self: Context, message: str) -> Message:
    return await self.send(embed = Embed(color = self.bot.color, description = message))

Context.success = success
Context.fail = fail
logger.remove()
logger.add(
        stdout,
        level="INFO",
        colorize=True,
        enqueue=True,
        backtrace=True,
        format="<cyan>[</cyan><blue>{time:YYYY-MM-DD HH:MM:SS}</blue><cyan>]</cyan> (<magenta>Antinuke:{function}</magenta>) <yellow>@</yellow> <fg #BBAAEE>{message}</fg #BBAAEE>",
    )

class Antinuke(Bot):
    def __init__(self, **kwargs):
        self.color = 0x000001
        self.config = config
        self.browser = Session()
        self.db = Database(self.config.uri)
        kwargs["command_prefix"] = self.get_prefix
        kwargs["auto_update"] = False
        kwargs["anti_cloudflare_ban"] = True
        super().__init__(**kwargs)
        activity = discord.CustomActivity(name="Antiduke ready to nuke")

    async def on_guild_join(self: "Antinuke", guild: Guild) -> None:
        if channel := self.get_channel(self.config.CHANNEL):
            await channel.send(embed = Embed(color = self.color, description = f"Joined **{guild.name}**\n**Members:** {len(guild.members)}\n**Owner:** {str(guild.owner)}\n**ID:** {guild.id}"))

    async def process_commands(self: "Antinuke", message: Message):
        if not message.guild:
            return
        if message.author.bot:
            return

        check = await self.db.fetchrow(
            """
            SELECT * FROM blacklist 
            WHERE (object_id = $1 AND object_type = $2) 
            OR (object_id = $3 AND object_type = $4)
        """,
            message.author.id,
            "user_id",
            message.guild.id,
            "guild_id",
        )

        if check:
            return
        if not self.is_ready():
            return

        return await super().process_commands(message)
    
    async def is_owner(self, user: User):
        if user.id in self.owner_ids:  # Implement your own conditions here
            return True

        # Else fall back to the original
        return await super().is_owner(user)
    
    async def get_prefix(self: "Antinuke", message: Message):
        server = await self.db.fetchval(
            """SELECT prefix
            FROM prefixes
            WHERE guild_id = $1""",
            message.guild.id,
        )
        return when_mentioned_or(server or ",")(self, message)

    async def on_message(self: "Antinuke", message: Message):
        if message.author.bot:
            return
        if not message.guild:
            return
        prefix = await self.db.fetchval(
            """SELECT prefix
            FROM prefixes
            WHERE guild_id = $1""",
            message.guild.id,
        ) or ","
        @ratelimit("prefix_message:{message.guild.id}", 1, 5)
        async def prefix_message(message: Message, prefix: str = ","):
            return await message.channel.send(embed = Embed(color = self.color, description = f"My current prefix is `{prefix}`"))
        if message.mentions_bot(strict = True):
            return await prefix_message(message, prefix)
        await self.process_commands(message)


    async def load_cog(self: "Antinuke", path: str):
        try:
            await self.load_extension(path)
            logger.info(f"Successfully loaded {path.split('.')[-1].title()}")
        except Exception as e:
            tb = "".join(traceback.format_exception(type(e), e, e.__traceback__))
            logger.error(f"Failed to load {path.split('.')[-1].title()} due to the following exception: \n{tb}")

    async def load_cogs(self: "Antinuke") -> None:
        cogs = [
            f'cogs.{str(c).split("/")[-1].split(".")[0]}'
            for c in Path("cogs/").glob("*.py")
        ]
        logger.info(cogs)
        await asyncio.gather(*[self.load_cog(c.replace("cogs\\", "")) for c in cogs])


    async def setup_hook(self: "Antinuke"):
        await self.db.connect()
        with open("install/schema.sql", "r") as file:
            tables = file.read().split(";")
        for table in tables:
            try:
                await self.db.execute(f"{table};")
            except:
                pass
        try:
            await self.browser.launch()
        except:
            pass
        await self.load_cogs()
        await self.load_extension("jishaku")


    async def on_command_error(self: "Antinuke", ctx: Context, error: Exception):
        if isinstance(error, MissingPermissions):
            return await ctx.fail(f"missing permissions")
        tb = "".join(traceback.format_exception(type(error), error, error.__traceback__))
        logger.info(f"{ctx.command.qualified_name} raised {tb}")
        
bot = Antinuke(intents = Intents().all(), help_command = None, owner_ids = [352190010998390796, 153643814605553665])
if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(bot.run(config.TOKEN))


    





