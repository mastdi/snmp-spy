from fastapi import FastAPI

from snmp_spy.util.mediator import Mediator

from .create import DeviceCreate
from .read import DeviceRead
from .router import router

__all__ = ["register_handlers", "register_routes"]


def register_handlers(mediator: Mediator) -> None:
    mediator.register_handler(DeviceCreate())
    mediator.register_handler(DeviceRead())


def register_routes(app: FastAPI) -> None:
    app.include_router(router)
