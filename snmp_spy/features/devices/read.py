from uuid import UUID

from fastapi import status

from snmp_spy.domain.device import Device, DeviceIdentifier
from snmp_spy.util.mediator import Handler, mediator

from ...domain.exceptions import NotFoundError
from .database import devices
from .router import router


class DeviceRead(Handler):
    async def handle(self, request: DeviceIdentifier) -> Device:
        # TODO: Figure out how the architecture should look like to avoid circular
        #       imports
        from snmp_spy.infrastructure.database import database

        query = devices.select().where(devices.c.identifier == request.identifier)
        result = await database.fetch_one(query)
        if result is None:
            raise RuntimeError(NotFoundError(identifier=request.identifier))
        return Device(**dict(result))


@router.get(
    "/devices/{identifier}",
    operation_id="read_device",
    summary="Read a new device.",
    description="Read a new device from storage.",
    response_model=Device,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "Device found.",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": NotFoundError,
            "summary": "Device not found.",
            "description": "Device with the given identifier not found.",
        },
    },
)
async def read_device(identifier: UUID) -> Device:
    return await mediator.send(DeviceIdentifier(identifier=identifier))
