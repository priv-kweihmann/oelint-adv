# oelint.vars.licensesdpx

severity: warning

## Example

In any recipe

```
LICENSE = "ISC &MIT"
```

## Why is this bad?

The syntax is always `` & `` or `` | `` for combined licenses.
Detection might fail if the surrounding spaces are omitted.

## Ways to fix it

```
LICENSE = "ISC & MIT"
```
