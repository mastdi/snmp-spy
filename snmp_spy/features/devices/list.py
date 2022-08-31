from fastapi import status
from sqlalchemy import select

import snmp_spy.infrastructure.db as db
from snmp_spy.domain.device import Device, DeviceList, ListDevices
from snmp_spy.util.mediator import Handler, mediator

from .db import Devices
from .router import router


class DevicesList(Handler):
    async def handle(self, request: ListDevices) -> DeviceList:
        statement = select(Devices).where(Devices.deleted.is_(None))

        async with db.session() as session:
            cursor = await session.execute(statement)
            rows = cursor.scalars()

        return DeviceList(devices=[Device.from_orm(row) for row in rows])


@router.get(
    "/devices",
    operation_id="list_device",
    summary="List all devices",
    description="Lists all device from storage.",
    response_model=DeviceList,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "List of all devices found.",
        }
    },
)
async def list_device() -> Device:
    return await mediator.send(ListDevices())
