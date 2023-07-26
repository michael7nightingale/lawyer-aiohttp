from aiopg.sa import Engine
from sqlalchemy import Table
from typing import Type
from abc import ABC, abstractmethod

from db import Message
from repositories import BaseRepository, AiopgRepository


class BaseService(ABC):
    repository_class: Type[BaseRepository]

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass


class AiopgService(BaseService):
    repository_class = AiopgRepository
    model: Table

    def __init__(self, db: Engine):
        self.repository = self.repository_class(db=db, model=self.model)


class MessageService(AiopgService):
    model = Message

    async def create_message(self, **kwargs):
        await self.repository.create(**kwargs)
