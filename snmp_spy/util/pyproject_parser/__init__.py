"""Exposes a method to parse the content of pyproject.toml along with the models
associated with the parsed version.
"""
from typing import List

import pydantic
import toml


class MailBox(pydantic.BaseModel):
    """Authors and maintainers must be in the form name <email>."""

    display_name: str
    mail: str


class Poetry(pydantic.BaseModel):
    """The tool.poetry section of the pyproject.toml"""

    name: str
    version: str
    description: str
    readme: str
    license: str
    repository: pydantic.HttpUrl
    authors: List[MailBox]

    @pydantic.validator("authors", pre=True)
    def _mailboxes_to_authors(cls, value: List[str]) -> List[MailBox]:
        mailboxes = []
        for mailbox in value:
            parts = mailbox.split("<")
            assert len(parts) == 2
            assert parts[1].endswith(">")
            mailboxes.append(MailBox(display_name=parts[0], mail=parts[1][:-1]))
        return mailboxes


class Tool(pydantic.BaseModel):
    """Tools defined in the pyproject."""

    poetry: Poetry


class PyProject(pydantic.BaseModel):
    """Root of the parsed pyproject.toml file."""

    tool: Tool


def loads(content: str) -> PyProject:
    """Parses a TOML-formatted string to a PyProject object.

    :param content: TOML-formatted string of pyproject.toml
    :return: A parsed typed PyProject
    """
    return PyProject(**toml.loads(content))
