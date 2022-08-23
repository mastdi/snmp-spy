from typing import Dict, Type, get_type_hints

from .base_classes import Handler, Request, Response


class Mediator:
    def __init__(self) -> None:
        """Encapsulates how a set of objects interact."""
        self.__requests: Dict[Type[Request], Handler] = dict()

    def register_handler(self, handler: Handler) -> None:
        """Registers a new handler for the mediator.

        Uses the type hint of the handler to map an implementation of a Request model
        to the instance of the handler provided.

        :param handler: An instance of a handler.
        :raise TypeError: If the handler provided does not inherit :class:`Handler`
        :raise KeyError: If the :meth:`Handler.handle` is not proper type hinted.
        """
        if not isinstance(handler, Handler):
            raise TypeError("Request and handler must inherit proper parents.")

        type_hints = get_type_hints(handler.handle)
        if not ("request" in type_hints and issubclass(type_hints["request"], Request)):
            raise KeyError(
                "Handler.handle must be implemented with an arg named 'request' "
                "and the arg must inherit Request"
            )

        if type_hints["request"] in self.__requests:
            raise RuntimeError("Request of that type already have a handler.")

        self.__requests[type_hints["request"]] = handler

    async def send(self, request: Request) -> Response:
        """Locates the proper handler and returns the response of that handler.

        :param request: The request to handle.
        :return: The response of the handler.
        :raise TypeError: If not handler is found.
        """
        request_class = request.__class__
        if request_class not in self.__requests:
            raise TypeError(f"No handler for this request class: {request_class}.")

        return await self.__requests[request_class].handle(request)
