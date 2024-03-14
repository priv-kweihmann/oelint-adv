# oelint.vars.licfileprefix

severity: warning

## Example

In any recipe

```
LIC_FILES_CHKSUM = "file://${S}/LICENSE;md5=a4a2bbea1db029f21b3a328c7a059172"
```

## Why is this bad?

The ``${S}`` prefix is unnecessary, as the files are always searched relative to ``${S}``

## Ways to fix it

```
LIC_FILES_CHKSUM = "file://LICENSE;md5=a4a2bbea1db029f21b3a328c7a059172"
```
