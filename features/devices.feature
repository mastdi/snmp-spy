Feature: Create, read, update, and delete records of devices

  Background:
    Given the API

  Scenario: Create a device
    When I create a new device
    Then I know the unique identifier of said device
