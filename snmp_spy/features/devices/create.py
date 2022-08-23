import uuid

from snmp_spy.domain.device import DeviceIn, DeviceOut
from snmp_spy.util.mediator import Handler


class DeviceCreate(Handler):
    # SHAKE-256 hexadecimal digest of length 16 of "Device"
    __NAMESPACE = uuid.UUID("0d85308a-79d8-a880-4cc9-322c7b66006c")

    async def handle(self, request: DeviceIn) -> DeviceOut:
        return DeviceOut(
            identifier=uuid.uuid5(DeviceCreate.__NAMESPACE, request.name),
            name=request.name,
            description=request.description,
        )
