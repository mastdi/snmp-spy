import hashlib
from typing import Any
from uuid import UUID, uuid5

import pydantic
from fastapi import status

_NAMESPACE = UUID(bytes=hashlib.shake_256(b"snmp_spy").digest(16))
_NOT_FOUND = str(uuid5(_NAMESPACE, "NotFound"))


class ExceptionBase(pydantic.BaseModel):
    message: str = pydantic.Field(..., title="Human readable message of the error.")
    error_identifier: str = pydantic.Field(
        ..., title="Unique machine readable identifier of the error."
    )
    status_code: int = pydantic.Field(..., title="The corresponding HTTP status code.")


class NotFound(ExceptionBase):
    def __init__(self, **data: Any) -> None:
        identifier: UUID = data.pop("identifier")
        data["message"] = f"Resource with identifier '{identifier}' not found."
        data["status_code"] = status.HTTP_404_NOT_FOUND
        data["error_identifier"] = _NOT_FOUND
        super().__init__(**data)

    class Config:
        schema_extra = {
            "example": {
                "status_code": status.HTTP_404_NOT_FOUND,
                "error_identifier": "a568b777-71cc-5322-ba48-1f9bcad496d4",
                "message": "Resource with identifier "
                "'608195e9-f99f-4df1-96d2-f675204affab' not found.",
            }
        }
