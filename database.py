from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from config import SQLLITE_DATABASE_URI
from models import Model


async_engine = create_async_engine(SQLLITE_DATABASE_URI, pool_pre_ping=True)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        finally:
            session.close()

async def create_tables():
    async with async_engine.begin() as conn:
        try:
            await conn.run_sync(Model.metadata.create_all)
            print("Created tables")
        except Exception as ex:
            print(f"Eexception occurred: {ex}")
            return

async def delete_tables():
    async with async_engine.begin() as conn:
        try:
            await conn.run_sync(Model.metadata.drop_all)
            print("Cleared tables")
        except Exception as ex:
            print(f"Eexception occurred: {ex}")
            return
