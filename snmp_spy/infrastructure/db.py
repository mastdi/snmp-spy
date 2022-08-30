import uuid
from typing import Any, Callable, Optional, Type

import sqlalchemy
import sqlalchemy_utils
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeMeta, declarative_base, sessionmaker

__all__ = ["Base", "primary_key_column", "session", "init_db", "SessionContext"]

# noinspection PyTypeChecker
Base: DeclarativeMeta = declarative_base()


def primary_key_column() -> sqlalchemy.Column:
    return sqlalchemy.Column(
        "identifier", sqlalchemy_utils.UUIDType(), primary_key=True, default=uuid.uuid4
    )


session: Callable[..., AsyncSession]


async def init_db(
    database_url: str,
    echo: bool = False,
    create_all: bool = False,
    expire_on_commit: bool = False,
) -> None:
    engine = create_async_engine(
        database_url,
        echo=echo,
    )

    if create_all:
        from snmp_spy.features.devices.db import Devices  # noqa: F401

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    # expire_on_commit=False will prevent attributes from being expired
    # after commit.
    global session
    session = sessionmaker(
        engine, expire_on_commit=expire_on_commit, class_=AsyncSession
    )


class SessionContext:
    def __init__(self) -> None:
        self.__session: Optional[AsyncSession] = None

    async def __aenter__(self) -> AsyncSession:
        global session
        self.__session = session()
        return self.__session

    async def __aexit__(
        self, exc_type: Type[Exception], exc: Exception, tb: Any
    ) -> None:
        print(type(exc_type))
        print(type(exc))
        print(type(tb))
        assert isinstance(self.__session, AsyncSession)
        if exc_type is None:
            await self.__session.commit()
        else:
            await self.__session.rollback()
