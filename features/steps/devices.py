from http import HTTPStatus

from behave import when
from behave.runner import Context
from starlette.testclient import TestClient

from snmp_spy.domain.device import Device, DeviceIn


def _create_device(client: TestClient) -> Device:
    response = client.post(url="/devices", json=DeviceIn.Config.schema_extra["example"])

    assert response.status_code == HTTPStatus.CREATED
    return Device(**response.json())


@when("I create a new device")
def step_create_new_device(context: Context) -> None:
    client: TestClient = context.api_client

    context.response = _create_device(client)
