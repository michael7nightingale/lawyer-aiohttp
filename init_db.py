from sqlalchemy import MetaData, create_engine

from lawyer.settings import config
from lawyer.db import Message


DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"


def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[Message])


if __name__ == "__main__":
    db_url = DSN.format(**config['postgres'])
    engine_ = create_engine(db_url)
    create_tables(engine_)
