from sqlalchemy import Table
from aiopg.sa import Engine
from contextlib import asynccontextmanager

from db import message


class BaseRepository:
    model: Table

    def __init__(self, db: Engine):
        self._db = db

    @property
    def db(self) -> Engine:
        return self._db

    @asynccontextmanager
    async def connection(self):
        async with self.db.acquire() as conn:
            yield conn

    async def create(self, **values):
        async with self.connection() as conn:
            await conn.execute(self.model.insert().values(**values))


class MessageRepository(BaseRepository):
    model = message
