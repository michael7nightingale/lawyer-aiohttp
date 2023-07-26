from aiopg.sa import Engine
from typing import Type

from repositories import BaseRepository, MessageRepository


class BaseService:
    repository_class: Type[BaseRepository]

    def __init__(self, db: Engine):
        self.repository = self.repository_class(db)


class MessageService(BaseService):
    repository_class = MessageRepository

    async def create_message(self, **kwargs):
        await self.repository.create(**kwargs)
