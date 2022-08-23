import pytest

from .base_classes import Handler, Request, Response
from .mediator import Mediator


class _Example:
    class DoAddOneRequest(Request):
        """Request the handler to add one to the number"""

        number: int

    class AddedOneResponse(Response):
        """Response after adding one to the number"""

        number: int

    class AddOneHandler(Handler):
        async def handle(
            self, request: "_Example.DoAddOneRequest"
        ) -> "_Example.AddedOneResponse":
            return _Example.AddedOneResponse(number=request.number + 1)


@pytest.mark.asyncio
async def test_send() -> None:
    request = _Example.DoAddOneRequest(number=1)
    mediator = Mediator()
    mediator.register_handler(_Example.AddOneHandler())

    response = await mediator.send(request)

    assert isinstance(response, _Example.AddedOneResponse)
    assert response.number == 2


@pytest.mark.asyncio
async def test_invalid_handler_type() -> None:
    mediator = Mediator()
    with pytest.raises(TypeError) as e_info:
        # noinspection PyTypeChecker
        mediator.register_handler(_Example.AddOneHandler)  # type: ignore

    assert isinstance(e_info.value, TypeError)
    assert e_info.value.args[0] == "Request and handler must inherit proper parents."


@pytest.mark.asyncio
async def test_multiple_handlers_error() -> None:
    mediator = Mediator()
    mediator.register_handler(_Example.AddOneHandler())

    with pytest.raises(RuntimeError) as e_info:
        mediator.register_handler(_Example.AddOneHandler())

    assert isinstance(e_info.value, RuntimeError)
    assert e_info.value.args[0] == "Request of that type already have a handler."
