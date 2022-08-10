Feature: Exposing the common special files found in the root directory of the repository
  As a potential user of this project
  I want to be able to read common special files
  So that I know how to use it, under which conditions, what has changed and how I can contribute

Scenario: Common special files found in the root directory
  Given the "snmp-spy" project
  Then "LICENSE" is available
  And "CONTRIBUTING" is available
  And "CHANGELOG" is available
  And "README" is available
