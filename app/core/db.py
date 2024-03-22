from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker

from core.config import settings

CON_URL = settings.DB_URL
# print(CON_URL)
Base = declarative_base()
engine = create_async_engine(url=CON_URL)
# AsyncLocalSession = sessionmaker(
#     autoflush=False, autocommit=False, bind=engine, class_=AsyncSession
# )
AsyncLocalSession = async_sessionmaker(
    autoflush=False, autocommit=False, bind=engine, class_=AsyncSession
)


async def get_db():
    async with AsyncLocalSession() as async_session:
        yield async_session


async def init_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
