import asyncio
import os

from behave.model import Scenario
from behave.runner import Context


def before_scenario(context: Context, scenario: Scenario) -> None:
    from uuid import uuid4

    from snmp_spy.infrastructure.db import init_db

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.get_event_loop()

    context.db_name = f"behave-tests-{uuid4()}.db"
    loop.run_until_complete(
        init_db(f"sqlite+aiosqlite:///{context.db_name}", False, True)
    )


def after_scenario(context: Context, scenario: Scenario) -> None:
    from snmp_spy.infrastructure.db import session

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.get_event_loop()
    loop.run_until_complete(session().close())

    os.remove(context.db_name)
