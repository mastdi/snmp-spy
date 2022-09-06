"""Step definitions of the feature: Exposing the common special files found in the root
directory of the repository.

Handles the given-part and all then-parts.
"""
import hashlib
from pathlib import Path

from behave import given, then
from behave.runner import Context


@given('the "snmp-spy" project')
def step_given_project(context: Context) -> None:
    """Set the root_dir to be the root directory of snmp-spy .
    :param context: behave context.
    """
    context.root_dir = Path(__file__).parent.parent.parent


@then('"LICENSE" is available')
def step_license(context: Context) -> None:
    """Asserts that the LICENSE is available and not changed from the initial commit.
    :param context: behave context.
    """
    license_file = context.root_dir.joinpath("LICENSE")

    with open(license_file, "rb") as license_fd:
        content = license_fd.read()
    license_hash = hashlib.sha224(content).hexdigest()

    # Compare to "sha224sum LICENSE" of initial commit
    # TODO: Figure out why Windows gives another hash
    assert len(content) > 0
    assert license_hash == "45fd0b382919a02f391b9ce13e70ed703b9569cce812332d03c514a2", content


@then('"{file_name}" is available')
def step_contributing(context: Context, file_name: str) -> None:
    """Asserts that the CONTRIBUTING.md file exists.
    :param context: behave context.
    :param file_name: The name of the file (.md is added if missing)
    """
    if not file_name.endswith(".md"):
        file_name = file_name + ".md"

    assert context.root_dir.joinpath(file_name).is_file()
