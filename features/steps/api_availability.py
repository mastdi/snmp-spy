from behave import given, then
from behave.runner import Context
from fastapi.testclient import TestClient

from snmp_spy import pyproject
from snmp_spy.api.main import app


@given("the API")
def given_the_api(context: Context) -> None:
    context.api_client = TestClient(app)


@then("the OpenAPI specification is available")
def then_openapi_spec_available(context: Context) -> None:
    client: TestClient = context.api_client

    response = client.get("/openapi.json")
    data = response.json()
    info = data["info"]

    assert response.status_code == 200
    assert info["title"] == pyproject.tool.poetry.name.upper()
    assert info["version"] == pyproject.tool.poetry.version
    assert info["description"] == pyproject.tool.poetry.description
    assert info["license"]["name"] == pyproject.tool.poetry.license
    assert info["license"]["url"].startswith(pyproject.tool.poetry.repository)
    assert info["license"]["url"].endswith("LICENSE")
    assert info["contact"]["name"] == pyproject.tool.poetry.authors[0].display_name
    assert info["contact"]["email"] == pyproject.tool.poetry.authors[0].mail
