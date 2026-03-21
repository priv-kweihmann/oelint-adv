# oelint.vars.unpackdir

severity: error

## Example

```
S = "${WORKDIR}"
```

## Why is this bad?

Recently upstream changed the way sources are unpacked/refreshed
on changes of the SRC_URI inputs.
Unpacking in WORKDIR makes it impossible to determine what is
a new resource and what might be a left-over from a previous run.
Hence UNPACKDIR was introduced - users should refrain from
using WORKDIR for S.

## Ways to fix it

```
S = "${UNPACKDIR}"
```
