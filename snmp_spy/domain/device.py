from typing import Optional

import pydantic

from snmp_spy.domain import Identifier
from snmp_spy.util.mediator import Request, Response


class DeviceBase(pydantic.BaseModel):
    name: str = pydantic.Field(
        ...,
        title="The name of the device.",
        description="A unique visible name of the device.",
    )
    description: Optional[str] = pydantic.Field(
        title="Description of the device", description="An text describing the device."
    )


class DeviceIn(Request, DeviceBase):
    pass


class DeviceOut(Response, DeviceBase, Identifier):
    pass
