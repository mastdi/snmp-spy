import uuid
from typing import Any

import databases
import sqlalchemy
import sqlalchemy_utils

metadata = sqlalchemy.MetaData()


def primary_key_column() -> sqlalchemy.Column:
    return sqlalchemy.Column(
        "identifier", sqlalchemy_utils.UUIDType(), primary_key=True, default=uuid.uuid4
    )


database: databases.Database


def init(
    database_url: str | databases.DatabaseURL,
    force_rollback: bool = False,
    **options: Any
) -> databases.Database:
    global database
    database = databases.Database(
        url=database_url, force_rollback=force_rollback, **options
    )
    return database


def create_all(database_url: str | databases.DatabaseURL) -> None:
    # TODO: Figure out a way to register this proper
    # flake8: noqa
    from snmp_spy.features.devices.database import devices

    engine = sqlalchemy.create_engine(
        database_url, connect_args={"check_same_thread": False}
    )
    metadata.create_all(engine)
