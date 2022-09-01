from uuid import UUID

from fastapi import status
from sqlalchemy import delete

from snmp_spy.domain import EMPTY_RESPONSE, EmptyResponse
from snmp_spy.domain.device import DeviceDeleteRequest
from snmp_spy.infrastructure.db import SessionContext
from snmp_spy.util.mediator import Handler, mediator

from .db import Devices
from .router import router


class DeviceDelete(Handler):
    """Delete device handler."""

    async def handle(self, request: DeviceDeleteRequest) -> EmptyResponse:
        """Deletes a device from storage.

        The result after calling this endpoint would ensure that no devices with the
        given identifier are found. This endpoint will still succeed even if the there
        is no device with the given identifier (since there will be no device found
        afterwards).
        """
        async with SessionContext() as session:
            await session.execute(
                (delete(Devices).where(Devices.identifier == request.identifier))
            )
        return EMPTY_RESPONSE


@router.delete(
    "/devices/{identifier}",
    operation_id="delete_device",
    summary="Delete a device.",
    description="\n".join(
        line.lstrip() for line in (DeviceDelete.handle.__doc__ or "").splitlines()
    ),
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Device deleted.",
        }
    },
)
async def delete_device(identifier: UUID) -> None:
    await mediator.send(DeviceDeleteRequest(identifier=identifier))
