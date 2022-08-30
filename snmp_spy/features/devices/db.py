import datetime

from sqlalchemy import Column, DateTime, String

from snmp_spy.infrastructure.db import Base, primary_key_column

__all__ = ["Devices"]


class Devices(Base):
    __tablename__ = "devices"

    identifier = primary_key_column()
    name = Column(String(length=128), unique=True)
    description = Column(String(length=65536))
    created = Column(DateTime(), default=datetime.datetime.utcnow)
    updated = Column(DateTime(), default=datetime.datetime.utcnow)
    deleted = Column(DateTime(), default=None)
