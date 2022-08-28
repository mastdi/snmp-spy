import os

from behave.model import Scenario
from behave.runner import Context


def before_scenario(context: Context, scenario: Scenario) -> None:
    from uuid import uuid4

    from snmp_spy.infrastructure.database import create_all, database, init

    context.db_name = f"behave-tests-{uuid4()}.db"
    create_all(f"sqlite:///{context.db_name}")
    init(f"sqlite+aiosqlite:///{context.db_name}")
    database.connect()


def after_scenario(context: Context, scenario: Scenario) -> None:
    from snmp_spy.infrastructure.database import database

    database.disconnect()

    os.remove(context.db_name)
