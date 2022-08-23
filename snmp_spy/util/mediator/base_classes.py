"""Exposes the base classes for the mediator
"""
import pydantic


class Request(pydantic.BaseModel):
    """Base model of any requests handled by the mediator."""


class Response(pydantic.BaseModel):
    """Base model of any response the mediator will return after a request have been
    handled.
    """


class Handler:
    """Base class for handlers."""

    async def handle(self, request: Request) -> Response:
        """Performs certain actions to convert a Request to a Response.

        Actual implementation defined in each handler.
        :param request: The request
        :return: The response
        """
        raise NotImplementedError("Must be overridden by the parent class.")
