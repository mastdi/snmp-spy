from typing import Any, List, Optional

import pydantic

from snmp_spy.domain import Identifier, make_optional
from snmp_spy.util.mediator import Request, Response


class _DeviceBase(pydantic.BaseModel):
    name: str = pydantic.Field(
        ...,
        title="The name of the device.",
        description="A unique visible name of the device.",
        min_length=1,
        max_length=128,
    )
    description: Optional[str] = pydantic.Field(
        title="Description of the device",
        description="An text describing the device.",
        max_length=65536,
    )

    class Config:
        schema_extra = {
            "example": {
                "name": "DiskStation DS220+",
                "description": "A compact network-attached storage solution designed "
                "to streamline the data and multimedia management.",
            }
        }


class DeviceIn(Request, _DeviceBase):
    """Properties needed to create a new device."""


class Device(Response, _DeviceBase, Identifier):
    """Representation of a device."""

    class Config:
        schema_extra = {
            "example": {
                **DeviceIn.Config.schema_extra["example"],
                "identifier": "d4104a6e-e288-4d6d-b8cf-8f0b8eb03a56",
            }
        }
        orm_mode = True


class DeviceList(Response):
    """Envelopes a list of devices."""

    devices: List[Device] = pydantic.Field(
        ...,
        title="Envelopes a list of devices.",
        description="Contains a list of devices",
    )


class DeviceReadRequest(Request, Identifier):
    """Request used to read a device from storage via the mediator."""


class DeviceDeleteRequest(Request, Identifier):
    """Request used to delete a device from storage via the mediator."""


class ListDevices(Request):
    """Request used to list all devices from storage via the mediator."""


DeviceInOptional: Any = make_optional(DeviceIn)
DeviceInOptional.__doc__ = """Properties possible to update."""


class DeviceUpdateRequest(Request, DeviceInOptional, Identifier):
    """Request used to update a device in storage via the mediator."""
