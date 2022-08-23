from snmp_spy.util.mediator import Mediator

from .create import DeviceCreate


def register_handlers(mediator: Mediator) -> None:
    mediator.register_handler(DeviceCreate())
