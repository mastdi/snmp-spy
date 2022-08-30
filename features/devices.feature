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