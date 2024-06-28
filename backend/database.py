from __future__ import annotations

import loguru
from types import TracebackType
from typing import Any, Optional, Protocol, Union
from typing import Iterable, Sequence
import ujson
from asyncpg import Connection, Pool, Record as DefaultRecord, create_pool

log: loguru.logger = loguru.logger


class Record(DefaultRecord):
    def __getattr__(self: "Record", name: Union[str, Any]) -> Any:
        attr: Any = self[name]
        return attr

    def __dict__(self: "Record") -> dict[str, Any]:
        return dict(self)


class ConnectionContextManager(Protocol):
    async def __aenter__(self) -> Connection: ...

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None: ...


class Database:
    def __init__(self, uri: str):
        self.uri: str = uri
        self.pool: Optional[Pool] = None

    def encoder(self, *data: Any):
        return ujson.dumps(data[1])

    def decoder(self, *data: Any):
        return ujson.loads(data[1])

    async def settings(self, connection: Connection) -> None:
        await connection.set_type_codec(
            "json",
            encoder=self.encoder,
            decoder=self.decoder,
            schema="pg_catalog",
        )

    async def create(self) -> Pool:
        pool: Pool = await create_pool(
            dsn=self.uri, init=self.settings, record_class=Record
        )
        log.info(f"Initialized database connection {pool.__hash__()}")
        return pool

    async def connect(self) -> Pool:
        self.pool = await self.create()
        return self.pool

    async def close(self) -> None:
        if self.pool:
            await self.pool.close()
            log.info(f"Closed database connection {self.pool.__hash__()}")


    async def fetch(self, sql: str, *args):
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                data = await conn.fetch(sql, *args)
        return data
            
    async def fetchiter(self, sql: str, *args):
        output = await self.fetch(sql, *args)
        for row in output:
            yield row

    async def fetchrow(self, sql: str, *args):
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                data = await conn.fetchrow(sql, *args)
        return data

    async def fetchval(self, sql: str, *args):
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                data = await conn.fetchval(sql, *args)
        return data

    async def execute(self, sql: str, *args) -> Optional[Any]:
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                _ = await conn.fetchval(sql, *args)
        return _

    async def executemany(self, sql: str, args: Iterable[Sequence]) -> Optional[Any]:
        async with self._pool.acquire() as conn:
            async with conn.transaction():
                _ = await conn.executemany(sql, args)
        return _