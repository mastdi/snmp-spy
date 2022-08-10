# SNMP Spy
> Spies are stubs that also record some information based on how they were called.
>
> &mdash; <cite>Martin Fowler</cite>

This is a Simple Network Management Protocol (SNMP) service that records when it last
sent a response and the ability to change the values for each object identifier (OID).

When monitoring network connected devices that expose the SNMP it can be troublesome
to test scenarios where the devices are misbehaving - which is one of the reasons why
we them!
