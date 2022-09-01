from http import HTTPStatus

from fastapi import status
from sqlalchemy import insert
from sqlalchemy.engine import CursorResult
from sqlalchemy.exc import IntegrityError

import snmp_spy.infrastructure.db as db
from snmp_spy.domain.device import Device, DeviceIn
from snmp_spy.domain.exceptions import AlreadyExistsError
from snmp_spy.util.mediator import Handler, mediator

from .db import Devices
from .router import router

__all__ = ["DeviceCreate"]


class DeviceCreate(Handler):
    async def handle(self, request: DeviceIn) -> Device:
        """Creates a new device in storage.

        The device is able to act as an SNMP Spy and hence imitate the SNMP responses
        a normal network-connected device would have.
        """
        statement = insert(Devices).values(**request.dict())

        async with db.SessionContext() as session:
            try:
                cursor: CursorResult = await session.execute(statement)
                identifier = cursor.inserted_primary_key.identifier
            except IntegrityError as error:
                raise RuntimeError(AlreadyExistsError(name=request.name)) from error

        return Device(
            identifier=identifier,
            name=request.name,
            description=request.description,
        )


@router.post(
    "/devices",
    operation_id="create_device",
    summary="Create a new device.",
    description="\n".join(
        line.lstrip() for line in (DeviceCreate.handle.__doc__ or "").splitlines()
    ),
    response_model=Device,
    status_code=HTTPStatus.CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Device created.",
            "links": {
                "GetDeviceById": {
                    "operationId": "read_device",
                    "parameters": {"identifier": "$response.body#/identifier"},
                    "description": "The `identifier` value returned in the response can"
                    "be used as the `identifier` parameter in "
                    "`GET /devices/{identifier}`.",
                },
                "UpdateDeviceById": {
                    "operationId": "update_device",
                    "parameters": {"identifier": "$response.body#/identifier"},
                    "description": "The `identifier` value returned in the response can"
                    "be used as the `identifier` parameter in "
                    "`PATCH /devices/{identifier}`.",
                },
                "DeleteDeviceById": {
                    "operationId": "update_device",
                    "parameters": {"identifier": "$response.body#/identifier"},
                    "description": "The `identifier` value returned in the response can"
                    "be used as the `identifier` parameter in "
                    "`DELETE /devices/{identifier}`.",
                },
            },
        },
        status.HTTP_409_CONFLICT: {
            "model": AlreadyExistsError,
            "description": "Device with the given name already exists.",
        },
    },
)
async def create_device(device: DeviceIn) -> Device:
    return await mediator.send(device)
