import datetime
import uuid
from http import HTTPStatus

from fastapi import status

from snmp_spy.domain.device import Device, DeviceIn
from snmp_spy.util.mediator import Handler, mediator

from ...domain.exceptions import NameAlreadyExistsError
from .database import devices
from .router import router


class DeviceCreate(Handler):
    async def handle(self, request: DeviceIn) -> Device:
        # TODO: Figure out how the architecture should look like to avoid circular
        #       imports
        from snmp_spy.infrastructure.database import database

        query = devices.insert()
        # TODO: Figure out a way to do this automatically
        now = datetime.datetime.utcnow()
        identifier = uuid.uuid4()

        try:
            await database.execute(
                query,
                values={
                    "identifier": identifier,
                    "created": now,
                    "updated": now,
                    **request.dict(),
                },
            )
        except Exception as exception:
            if "devices.name" in repr(exception):
                # TODO: Figure out a way to do this better
                raise RuntimeError(
                    NameAlreadyExistsError(name=request.name)
                ) from exception
            raise exception
        return Device(
            identifier=identifier,
            name=request.name,
            description=request.description,
        )


@router.post(
    "/devices",
    operation_id="create_device",
    summary="Create a new device.",
    description="Creates a new device that can act as an SNMP spy.",
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
            "model": NameAlreadyExistsError,
            "description": "Device with the given name already exists.",
        },
    },
)
async def create_device(device: DeviceIn) -> Device:
    return await mediator.send(device)
