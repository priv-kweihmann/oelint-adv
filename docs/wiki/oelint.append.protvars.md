# oelint.append.protvars

severity: error

## Example

In `my-random-%.bbappend`

```
LICENSE = "MIT"
LIC_FILES_CHKSUM = "foo;md5sum=f3e466264f6a083f8febd2b6921ce8c2"
PR = "4"
PV = "4"
SRCREV = "f161ebd29699d93411cec0915c5133c0f3229a28"
```

## Why is this bad?

This will obscure the license detection and change detection, leading to unpredictable effects, like
missing rebuilds or missed out license changes.

## Ways to fix it

- do **NOT** use any of ``LICENSE``, ``LIC_FILES_CHKSUM``, ``PR``, ``PV`` or ``SRCREV`` in ``*.bbappend``
- create a copy of the recipe instead and use `PREFERRED_PROVIDER` instead
