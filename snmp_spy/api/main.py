"""The bootstrapper of the API.

Exposes app which is the instance of the FastAPI that can be run using an appropriate
runner, e.g. uvicorn.
"""
from urllib.parse import urljoin

from fastapi import FastAPI

from snmp_spy.features import devices

from .. import __doc__, __version__, pyproject

__all__ = ["app"]


app = FastAPI(
    title=pyproject.tool.poetry.name.upper(),
    version=__version__,
    description=__doc__,
    contact={
        "name": pyproject.tool.poetry.authors[0].display_name,
        "email": pyproject.tool.poetry.authors[0].mail,
    },
    license_info={
        "name": pyproject.tool.poetry.license,
        "url": urljoin(
            pyproject.tool.poetry.repository, "blob/main/LICENSE", allow_fragments=True
        ),
    },
)

devices.register_routes(app)
