import uuid
from http import HTTPStatus
from typing import List, Optional

from behave import given, then, when
from behave.runner import Context
from starlette.testclient import TestClient

from snmp_spy.domain.device import Device, DeviceIn
from snmp_spy.domain.exceptions import NOT_FOUND_IDENTIFIER


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
    context.identifier = context.response.identifier


@given("multiple devices already in the storage")
def step_given_multiple_devices(context: Context) -> None:
    client: TestClient = context.api_client

    device0 = _create_device(client, name="Device 0")
    device1 = _create_device(client, name="Device 1")

    context.devices = [device0, device1]


@given("any identifier of a non-existing device")
def step_given_non_existing_id(context: Context) -> None:
    client: TestClient = context.api_client

    context.response = _create_device(client)
    context.identifier = uuid.uuid4()
    assert context.response.identifier != context.identifier


@when("I create a new device")
def step_when_new_device_created(context: Context) -> None:
    client: TestClient = context.api_client

    context.response = _create_device(client)


@when("I look up the device with the given identifier")
def step_when_lookup_device(context: Context) -> None:
    client: TestClient = context.api_client
    identifier: uuid.UUID = context.identifier

    response = client.get(f"/devices/{identifier}")

    context.lookup_response = response


@when("I list all devices")
def step_when_list_devices(context: Context) -> None:
    client: TestClient = context.api_client

    response = client.get("/devices")

    assert response.status_code == HTTPStatus.OK, f"Got {response.status_code}"
    context.list_result = [Device(**entity) for entity in response.json()["devices"]]


@when("I update the details of that device")
def step_when_update_device(context: Context) -> None:
    client: TestClient = context.api_client
    identifier: uuid.UUID = context.identifier
    device: Device = context.response

    device.description = (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod "
        "tempor incididunt ut labore et dolore magna aliqua."
    )

    context.lookup_response = client.patch(
        f"/devices/{identifier}", json={"description": device.description}
    )


@then("I see the details of that device")
def step_device_details(context: Context) -> None:
    assert context.lookup_response.status_code == HTTPStatus.OK

    lookup_result = Device(**context.lookup_response.json())

    assert lookup_result.dict() == context.response.dict()


@then("I see the details of all existing devices in the storage")
def step_then_list_devices(context: Context) -> None:
    # API does not guarantee anything about order, but we know that the names are
    # "Device 0" and "Device 1".
    search_result: List[Device] = sorted(context.list_result, key=lambda k: k.name)

    assert search_result[0].dict() == context.devices[0].dict()
    assert search_result[1].dict() == context.devices[1].dict()


@then("the read will fail")
def step_then_read_fail(context: Context) -> None:
    content = context.lookup_response.json()
    assert (
        context.lookup_response.status_code == HTTPStatus.NOT_FOUND
    ), f"Got: {context.lookup_response.status_code}"

    assert content["error_identifier"] == NOT_FOUND_IDENTIFIER
    assert content["status_code"] == HTTPStatus.NOT_FOUND
    assert content["message"] is not None and len(content["message"]) > 0
