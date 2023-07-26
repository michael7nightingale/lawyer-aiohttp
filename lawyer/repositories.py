from sqlalchemy import Table
from aiopg.sa import Engine
from contextlib import asynccontextmanager
from abc import ABC, abstractmethod


class BaseRepository(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def create(self, *args, **kwargs):
        pass

    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abstractmethod
    def filter(self, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, *args, **kwargs):
        pass

    @abstractmethod
    def all(self, *args, **kwargs):
        pass


class AiopgRepository(BaseRepository):
    def __init__(self, db: Engine, model: Table):
        self._db = db
        self._model = model

    @property
    def db(self) -> Engine:
        return self._db

    @property
    def model(self) -> Table:
        return self._model

    @asynccontextmanager
    async def connection(self):
        async with self.db.acquire() as conn:
            yield conn

    async def create(self, **values):
        async with self.connection() as conn:
            await conn.execute(self.model.insert().values(**values))

    async def get(self, *args, **kwargs):
        if len(args) == 1:
            kwargs.update(id=args[0])
        else:
            raise ValueError("Kwargs expected")
        async with self.connection() as conn:
            expected = (
                getattr(self.model, k) == v for k, v in kwargs.items()
            )
            cur = await conn.execute(self.model.select().where(*expected))
            result = await cur.fetchone()
            return result

    async def delete(self, id_):
        async with self.connection() as conn:
            await conn.execute(self.model.delete(self.model.id == id_))

    async def all(self):
        async with self.connection() as conn:
            cur = await conn.execute(self.model.select())
            return await cur.fetchall()

    async def filter(self, **kwargs):
        async with self.connection() as conn:
            expected = (
                getattr(self.model, k) == v for k, v in kwargs.items()
            )
            cur = await conn.execute(self.model.select().where(*expected))
            result = await cur.fetchall()
            return result
