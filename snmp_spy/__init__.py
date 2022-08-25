"""Contains metadata about the project
"""
import pathlib

import snmp_spy.util.pyproject_parser
from snmp_spy.features import devices
from snmp_spy.util.mediator import mediator

with open(
    pathlib.Path(__file__).parent.parent.joinpath("pyproject.toml"),
    "r",
    encoding="utf-8",
) as _pyproject_toml:
    __pyproject_content = _pyproject_toml.read()

pyproject = snmp_spy.util.pyproject_parser.loads(__pyproject_content)


__version__ = pyproject.tool.poetry.version
__doc__ = pyproject.tool.poetry.description

devices.register_handlers(mediator)
