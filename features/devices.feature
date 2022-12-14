#noinspection CucumberUndefinedStep
Feature: Create, read, update, and delete records of devices

  Background:
    Given the API

  Scenario: Create a device
    When I create a new device
    Then I know the unique identifier of said device

  Scenario: Read a device
    Given the unique identifier of an existing device
    When I look up the device with the given identifier
    Then I see the details of that device

  Scenario: Read a device not existing
    Given any identifier of a non-existing device
    When I look up the device with the given identifier
    Then the read will fail

  Scenario: List all devices
    Given multiple devices already in the storage
    When I list all devices
    Then I see the details of all existing devices in the storage

  Scenario: Update a device
    Given the unique identifier of an existing device
    When I update the details of that device
    Then I see the details of that device

  Scenario: Delete a device
    Given the unique identifier of an existing device
    When I delete that device
    And I look up the device with the given identifier
    Then the read will fail
