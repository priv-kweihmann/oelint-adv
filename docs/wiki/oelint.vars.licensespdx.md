# oelint.vars.licensespdx

severity: warning

## Example

In any recipe

```
LICENSE = "ISC &MIT"
```

## Why is this bad?

The syntax is always 

- `` & `` or `` | `` prior to `wrynose` release
- `` AND `` or `` OR `` from `wrynose` release

for combined licenses.
Detection might fail if the surrounding spaces are omitted.

## Ways to fix it

```
LICENSE = "ISC & MIT"
```

respectively

```
LICENSE = "ISC AND MIT"
```
