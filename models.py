import datetime
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase , Mapped, mapped_column
from sqlalchemy import Integer, DateTime, String, func

POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

PG_DSN = f'postgres+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}:{POSTGRES_DB}'

engine = create_async_engine(PG_DSN)

Session = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase, AsyncAttrs):
    pass

class User(Base):
    __tablename__ = 'users'

    id = Mapped[int] = mapped_column(Integer, primary_key=True)
    name = Mapped[str] = mapped_column(String, unique=True)
    password = Mapped[str] = mapped_column(String(64))
    registration_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())


    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'password': self.password,
            'registration_time': int(self.registration_time.timestamp()),
        }

async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
