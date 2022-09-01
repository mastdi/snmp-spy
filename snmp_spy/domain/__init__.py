from typing import Optional, Type
from uuid import UUID

import pydantic
from pydantic import create_model

from snmp_spy.util.mediator import Response


class Identifier(pydantic.BaseModel):
    identifier: UUID = pydantic.Field(
        ...,
        title="The identifier of the resource.",
        description="A unique identifier of the resource. "
        "No assumptions about the format of this field should be made.",
        exclusiveMinimum=1,
        exclusiveMaximum=64,
    )


class EmptyResponse(Response):
    pass


EMPTY_RESPONSE = EmptyResponse()


def make_optional(baseclass: Type[pydantic.BaseModel]) -> Type[pydantic.BaseModel]:
    # Extracts the fields and validators from the baseclass and make fields optional
    fields = baseclass.__fields__
    validators = {"__validators__": baseclass.__validators__}
    optional_fields = {
        key: (Optional[item.type_], None) for key, item in fields.items()
    }
    model: Type[pydantic.BaseModel] = create_model(
        f"{baseclass.__name__}Optional", **optional_fields, __validators__=validators
    )
    return model
