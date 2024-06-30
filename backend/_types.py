from discord.ext.commands import Bot, AutoShardedBot, Author
from typing import Union, Optional
from discord import Member, User
from typing_extensions import Self

SELF = Self
BOT = Union[Bot, AutoShardedBot]
USER = Optional[Union[Member, User]]