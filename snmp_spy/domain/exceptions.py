import hashlib
from typing import Any
from uuid import UUID, uuid5

import pydantic
from fastapi import status

_NAMESPACE = UUID(bytes=hashlib.shake_256(b"snmp_spy").digest(16))
NOT_FOUND_IDENTIFIER = str(uuid5(_NAMESPACE, "NotFound"))
RESOURCE_ALREADY_EXISTS_IDENTIFIER = str(uuid5(_NAMESPACE, "ResourceAlreadyExists"))


class ExceptionBase(pydantic.BaseModel):
    message: str = pydantic.Field(..., title="Human readable message of the error.")
    error_identifier: str = pydantic.Field(
        ..., title="Unique machine readable identifier of the error."
    )
    status_code: int = pydantic.Field(..., title="The corresponding HTTP status code.")


class NotFoundError(ExceptionBase):
    """Used when a specific resource is not found."""

    def __init__(self, identifier: UUID, **data: Any) -> None:
        data["message"] = f"Resource with identifier '{identifier}' not found."
        data["status_code"] = status.HTTP_404_NOT_FOUND
        data["error_identifier"] = NOT_FOUND_IDENTIFIER
        super().__init__(**data)

    class Config:
        schema_extra = {
            "example": {
                "status_code": status.HTTP_404_NOT_FOUND,
                "error_identifier": NOT_FOUND_IDENTIFIER,
                "message": "Resource with identifier "
                "'608195e9-f99f-4df1-96d2-f675204affab' not found.",
            }
        }


class AlreadyExistsError(ExceptionBase):
    """Used when a resource with would violate a unique constraint."""

    def __init__(self, name: str, **data: Any) -> None:
        data["message"] = f"Resource with unique property '{name}' already exists."
        data["status_code"] = status.HTTP_409_CONFLICT
        data["error_identifier"] = RESOURCE_ALREADY_EXISTS_IDENTIFIER
        super().__init__(**data)

    class Config:
        schema_extra = {
            "example": {
                "status_code": status.HTTP_409_CONFLICT,
                "error_identifier": RESOURCE_ALREADY_EXISTS_IDENTIFIER,
                "message": "Resource with unique property 'name' already exists.",
            }
        }
