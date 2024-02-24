from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio  import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import QueuePool


from rinha_backend.settings import Settings

db_url = Settings().DATABASE_URL    #type:ignore

engine = create_engine(db_url)    # type: ignore

async_engine = create_async_engine(
    db_url, pool_size=45, max_overflow=40, poolclass=QueuePool
)


def get_session():
    with Session(engine) as session:
        return session


def get_async_session():
    return async_sessionmaker(async_engine, expire_on_commit=False)

