import uuid
from typing import Any, Callable, Optional, Type

import sqlalchemy
import sqlalchemy_utils
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncSessionTransaction,
    create_async_engine,
)
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
        self.__active_transaction: Optional[AsyncSessionTransaction] = None

    async def __aenter__(self) -> AsyncSession:
        global session
        self.__session = session()
        self.__active_transaction = await self.__session.begin()
        return self.__session

    async def __aexit__(
        self, exc_type: Type[Exception], exc: Exception, tb: Any
    ) -> None:
        assert isinstance(self.__session, AsyncSession)
        assert isinstance(self.__active_transaction, AsyncSessionTransaction)

        if exc_type is None:
            await self.__active_transaction.commit()
        else:
            await self.__active_transaction.rollback()

        await self.__active_transaction.__aexit__(exc_type, exc, tb)
        await self.__session.__aexit__(exc_type, exc, tb)
