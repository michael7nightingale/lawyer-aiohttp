from sqlalchemy import Table, Column, MetaData, Text, DateTime, String
from datetime import datetime, timezone
from uuid import uuid4
import aiopg.sa


meta = MetaData()

message = Table(
    "message", meta,
    Column('id', String(255), primary_key=True, default=lambda: str(uuid4())),
    Column("name", String(255), nullable=False),
    Column("email", String(255), nullable=False),
    Column("phone", String(255), nullable=False),
    Column("text", Text, nullable=False),
    Column("time_send", DateTime(timezone=True), default=lambda: datetime.now(tz=timezone.utc))
)


async def pg_context(app):
    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(**conf)
    app['db'] = engine

    yield

    app['db'].close()
    await app['db'].wait_closed()
