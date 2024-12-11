from .Async_DB_Connection import async_engine, metadata
from sqlalchemy import Table


async def get_users_table():
    async with async_engine.connect() as connection:
        await connection.run_sync(metadata.reflect)
        return Table('users', metadata, autoload_with=connection)


async def get_owners_table():
    async with async_engine.connect() as connection:
        await connection.run_sync(metadata.reflect)
        return Table('owners', metadata, autoload_with=connection)