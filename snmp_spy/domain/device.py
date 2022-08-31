from typing import List, Optional

import pydantic

from snmp_spy.domain import Identifier
from snmp_spy.util.mediator import Request, Response


class DeviceBase(pydantic.BaseModel):
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


class DeviceIn(Request, DeviceBase):
    pass


class Device(Response, DeviceBase, Identifier):
    class Config:
        schema_extra = {
            "example": {
                **DeviceIn.Config.schema_extra["example"],
                "identifier": "d4104a6e-e288-4d6d-b8cf-8f0b8eb03a56",
            }
        }
        orm_mode = True


class DeviceList(Response):
    devices: List[Device] = pydantic.Field(
        ...,
        title="Envelopes a list of devices.",
        description="Contains a list of devices",
    )


class DeviceIdentifier(Request, Identifier):
    pass


class ListDevices(Request):
    pass
