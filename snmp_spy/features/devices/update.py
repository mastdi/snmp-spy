from uuid import UUID

from fastapi import status
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError

import snmp_spy.infrastructure.db as db
from snmp_spy.domain.device import (
    Device,
    DeviceIdentifier,
    DeviceInOptional,
    DeviceOptional,
)
from snmp_spy.domain.exceptions import AlreadyExistsError, NotFoundError
from snmp_spy.util.mediator import Handler, mediator

from .db import Devices
from .router import router


class DeviceUpdate(Handler):
    async def handle(self, request: DeviceOptional) -> Device:
        patch_values = request.dict(
            exclude_defaults=True, exclude_none=True, exclude={"identifier"}
        )
        if len(patch_values) == 0:
            # Nothing to patch
            return await mediator.send(DeviceIdentifier(identifier=request.identifier))

        async with db.SessionContext() as session:
            try:
                await session.execute(
                    (
                        update(Devices)
                        .where(Devices.identifier == request.identifier)
                        .values(patch_values)
                    )
                )
            except IntegrityError as error:
                raise RuntimeError(AlreadyExistsError(name=request.name)) from error

        # Return the updated device
        return await mediator.send(DeviceIdentifier(identifier=request.identifier))


@router.patch(
    "/devices/{identifier}",
    operation_id="update_device",
    summary="Update a device.",
    description="Update a device in storage.",
    response_model=Device,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "Device found and updated.",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": NotFoundError,
            "summary": "Device not found.",
            "description": "Device with the given identifier not found.",
        },
    },
)
async def read_device(identifier: UUID, device: DeviceInOptional) -> Device:
    return await mediator.send(
        DeviceOptional(**{"identifier": identifier, **device.dict()})
    )
