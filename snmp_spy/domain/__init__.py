from uuid import UUID

import pydantic


class Identifier(pydantic.BaseModel):
    identifier: UUID = pydantic.Field(
        ...,
        title="The identifier of the resource.",
        description="A unique identifier of the resource. "
        "No assumptions about the format of this field should be made.",
        exclusiveMinimum=1,
        exclusiveMaximum=64,
    )
