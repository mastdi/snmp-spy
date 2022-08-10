"""Step definitions of the feature: Exposing the common special files found in the root
directory of the repository.

Handles the given-part and all then-parts.
"""
import hashlib
from pathlib import Path

from behave import (  # type: ignore # pylint: disable=no-name-in-module,import-error
    given,
    then,
)


@given('the "snmp-spy" project')
def step_given_project(context) -> None:
    """Set the root_dir to be the root directory of snmp-spy .
    :param context: behave context.
    """
    context.root_dir = Path(__file__).parent.parent.parent


@then('"LICENSE" is available')
def step_license(context) -> None:
    """Asserts that the LICENSE is available and not changed from the initial commit.
    :param context: behave context.
    """
    license_file = context.root_dir.joinpath("LICENSE")
    assert license_file.is_file()
    with open(license_file, "rb") as license_fd:
        content = license_fd.read()
    license_hash = hashlib.sha224(content).hexdigest()
    # Compare to "sha224sum LICENSE" of initial commit
    assert license_hash == "45fd0b382919a02f391b9ce13e70ed703b9569cce812332d03c514a2"


@then('"CONTRIBUTING" is available')
def step_contributing(context) -> None:
    """Asserts that the CONTRIBUTING.md file exists.
    :param context: behave context.
    """
    assert context.root_dir.joinpath("CONTRIBUTING.md").is_file()


@then('"CHANGELOG" is available')
def step_changelog(context):
    """Asserts that the CHANGELOG.md file exists.
    :param context: behave context.
    """
    assert context.root_dir.joinpath("CHANGELOG.md").is_file()


@then('"README" is available')
def step_readme(context):
    """Asserts that the README.md file exists.
    :param context: behave context.
    """
    assert context.root_dir.joinpath("README.md").is_file()
