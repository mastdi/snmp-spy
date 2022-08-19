# SNMP Spy
> Spies are stubs that also record some information based on how they were called.
>
> &mdash; <cite>Martin Fowler</cite>

This is a Simple Network Management Protocol (SNMP) service that records when it last
sent a response and the ability to change the values for each object identifier (OID).

When monitoring network connected devices that expose the SNMP it can be troublesome
to test scenarios where the devices are misbehaving - which is one of the reasons why
we them!

## Usage
There are several ways to use this package.

### From pytest (or other places directly in Python code)

Coming up.

### Command-line interface

Coming up.

### API

To start the API using uvicorn, run the command:
```shell
poetry run uvicorn snmp_spy.api.main:app
```

### User interface

Coming up.
