import asyncio
import os
import tempfile

from behave.model import Scenario
from behave.runner import Context

from snmp_spy.infrastructure.db import init_db


def before_scenario(context: Context, scenario: Scenario) -> None:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.get_event_loop()

    temp_file = tempfile.NamedTemporaryFile(
        suffix=".db",
        prefix="behave-tests",
        delete=False,
    )
    context.db_name = temp_file.name
    temp_file.close()
    loop.run_until_complete(
        init_db(f"sqlite+aiosqlite:///{context.db_name}", False, True)
    )


def after_scenario(context: Context, scenario: Scenario) -> None:
    from snmp_spy.infrastructure.db import session

    loop = asyncio.get_event_loop()
    loop.run_until_complete(session().close())

    os.remove(context.db_name)
