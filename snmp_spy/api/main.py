"""The bootstrapper of the API.

Exposes app which is the instance of the FastAPI that can be run using an appropriate
runner, e.g. uvicorn.
"""
from urllib.parse import urljoin

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from snmp_spy.features import devices

from .. import __doc__, __version__, pyproject

__all__ = ["app"]

from snmp_spy.infrastructure.db import init_db

from ..domain.exceptions import ExceptionBase

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


@app.exception_handler(RuntimeError)
async def unicorn_exception_handler(
    request: Request, exc: RuntimeError
) -> JSONResponse:
    if not isinstance(exc.args[0], ExceptionBase):
        raise exc
    return JSONResponse(
        status_code=exc.args[0].status_code,
        content=exc.args[0].dict(),
    )


@app.on_event("startup")
async def startup_database() -> None:
    await init_db("sqlite+aiosqlite:///database.db", True, True)


@app.on_event("shutdown")
async def close_all_databases() -> None:
    from snmp_spy.infrastructure.db import session

    await session().close()
