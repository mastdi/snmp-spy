from http import HTTPStatus

from behave import given, then, when
from behave.runner import Context
from starlette.testclient import TestClient

from snmp_spy.domain.device import Device, DeviceIn


def _create_device(client: TestClient) -> Device:
    response = client.post(url="/devices", json=DeviceIn.Config.schema_extra["example"])

    assert response.status_code == HTTPStatus.CREATED
    return Device(**response.json())


@given("the unique identifier of an existing device")
def step_impl(context: Context) -> None:
    client: TestClient = context.api_client

    context.response = _create_device(client)


@when("I create a new device")
def step_create_new_device(context: Context) -> None:
    client: TestClient = context.api_client

    context.response = _create_device(client)


@when("I look up the device with the given identifier")
def step_lookup_device(context: Context) -> None:
    client: TestClient = context.api_client
    device: Device = context.response

    response = client.get(f"/devices/{device.identifier}")

    assert response.status_code == HTTPStatus.OK, f"Got {response.status_code}"
    context.lookup_result = Device(**response.json())


@then("I see the details of that device")
def step_device_details(context: Context) -> None:
    assert context.lookup_result.dict() == context.response.dict()
