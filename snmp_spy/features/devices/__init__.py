from fastapi import FastAPI

from snmp_spy.util.mediator import Mediator

from .create import DeviceCreate
from .router import router


def register_handlers(mediator: Mediator) -> None:
    mediator.register_handler(DeviceCreate())


def register_routes(app: FastAPI) -> None:
    app.include_router(router)
