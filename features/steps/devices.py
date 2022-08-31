from http import HTTPStatus
from typing import List, Optional

from behave import given, then, when
from behave.runner import Context
from starlette.testclient import TestClient

from snmp_spy.domain.device import Device, DeviceIn


def _create_device(client: TestClient, name: Optional[str] = None) -> Device:
    payload = DeviceIn.Config.schema_extra["example"]
    if name is not None:
        payload["name"] = name
    response = client.post(url="/devices", json=payload)

    assert response.status_code == HTTPStatus.CREATED
    return Device(**response.json())


@given("the unique identifier of an existing device")
def step_given_one_device(context: Context) -> None:
    client: TestClient = context.api_client

    context.response = _create_device(client)


@given("multiple devices already in the storage")
def step_given_multiple_devices(context: Context) -> None:
    client: TestClient = context.api_client

    device0 = _create_device(client, name="Device 0")
    device1 = _create_device(client, name="Device 1")

    context.devices = [device0, device1]


@when("I create a new device")
def step_when_new_device_created(context: Context) -> None:
    client: TestClient = context.api_client

    context.response = _create_device(client)


@when("I look up the device with the given identifier")
def step_when_lookup_device(context: Context) -> None:
    client: TestClient = context.api_client
    device: Device = context.response

    response = client.get(f"/devices/{device.identifier}")

    assert response.status_code == HTTPStatus.OK, f"Got {response.status_code}"
    context.lookup_result = Device(**response.json())


@when("I list all devices")
def step_when_list_devices(context: Context) -> None:
    client: TestClient = context.api_client

    response = client.get("/devices")

    assert response.status_code == HTTPStatus.OK, f"Got {response.status_code}"
    context.list_result = [Device(**entity) for entity in response.json()["devices"]]


@then("I see the details of that device")
def step_device_details(context: Context) -> None:
    assert context.lookup_result.dict() == context.response.dict()


@then("I see the details of all existing devices in the storage")
def step_then_list_devices(context: Context) -> None:
    # API does not guarantee anything about order, but we know that the names are
    # "Device 0" and "Device 1".
    search_result: List[Device] = sorted(context.list_result, key=lambda k: k.name)

    assert search_result[0].dict() == context.devices[0].dict()
    assert search_result[1].dict() == context.devices[1].dict()
