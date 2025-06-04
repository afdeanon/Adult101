import contextlib
from typing import AsyncIterator
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, AsyncConnection,create_async_engine

class Base(DeclarativeBase):
    pass

class DatabaseSessionManager:
    def __init__(self):
        self._engine:AsyncEngine|None = None
        self._sessionmaker:AsyncSession|None = None

    async def init(self, host:str, reset_tables:bool = True):
        self._engine = create_async_engine(host)
        self._sessionmaker = async_sessionmaker(self._engine)
        if reset_tables:
            async with self._engine.begin() as conn:
                await self.drop_all(conn)
                await self.create_all(conn)
    
    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager not initalized")
        async with self._engine.begin() as conn:
            try:
                yield conn
            except Exception:
                await conn.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) ->AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager not initalized")
        session:AsyncSession = self._sessionmaker
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
        
    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager not initalized")
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None
    
    async def create_all(self, conn:AsyncConnection):
        await conn.run_sync(Base.metadata.create_all)
        
    async def drop_all(self, conn:AsyncConnection):
        await conn.run_sync(Base.metadata.drop_all)

sessionmanager = DatabaseSessionManager()

async def get_db():
    async with sessionmanager.session() as db:
        yield db