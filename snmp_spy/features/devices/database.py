import datetime

import sqlalchemy

from snmp_spy.infrastructure.database import metadata, primary_key_column

devices = sqlalchemy.Table(
    "devices",
    metadata,
    primary_key_column(),
    sqlalchemy.Column("name", sqlalchemy.String(length=128), unique=True),
    sqlalchemy.Column("description", sqlalchemy.String(length=65536)),
    sqlalchemy.Column(
        "created", sqlalchemy.DateTime(), default=datetime.datetime.utcnow
    ),
    sqlalchemy.Column(
        "updated", sqlalchemy.DateTime(), default=datetime.datetime.utcnow
    ),
    sqlalchemy.Column("deleted", sqlalchemy.DateTime(), default=None),
)
