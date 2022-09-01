from uuid import UUID

from fastapi import status
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

import snmp_spy.infrastructure.db as db
from snmp_spy.domain.device import Device, DeviceReadRequest
from snmp_spy.domain.exceptions import NotFoundError
from snmp_spy.util.mediator import Handler, mediator

from .db import Devices
from .router import router


class DeviceRead(Handler):
    async def handle(self, request: DeviceReadRequest) -> Device:
        """Reads a device from storage.

        Looks up a device based on the identifier provided and returns the details of
        that device if found. Raises a NotFoundError if the identifier were not found.
        """
        statement = select(Devices).where(Devices.identifier == request.identifier)

        async with db.session() as session:
            result = await session.execute(statement)
        try:
            rows = result.one()
        except NoResultFound as error:
            raise RuntimeError(NotFoundError(identifier=request.identifier)) from error
        device: Device = Device.from_orm(rows[0])
        return device


@router.get(
    "/devices/{identifier}",
    operation_id="read_device",
    summary="Read a device.",
    description="\n".join(
        line.lstrip() for line in (DeviceRead.handle.__doc__ or "").splitlines()
    ),
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
    return await mediator.send(DeviceReadRequest(identifier=identifier))
