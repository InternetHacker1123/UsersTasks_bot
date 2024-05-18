#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import BigInteger, String, Integer
from dotenv import load_dotenv
import os

load_dotenv('.env')
engine = create_async_engine(url=os.getenv("SQLALCHEMY_URL"))

async_session = async_sessionmaker(engine)

# базовый класс


class Base(AsyncAttrs, DeclarativeBase):
    pass

# модель таблицы tasks


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(BigInteger)
    task_number = mapped_column(Integer)
    task = mapped_column(String(300))


# подключение к БД
async def async_main():
    async with engine.begin() as connect:
        print("connect")
        await connect.run_sync(Base.metadata.create_all)
