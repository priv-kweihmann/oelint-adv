# oelint.vars.fileextrapathsop

severity: error

## Example

In ``my-recipe_%.bbappend``

```
FILESEXTRAPATHS:prepend .= "${THISDIR}/file"
```

## Why is this bad?

``FILESEXTRAPATHS`` needs immediate variable expansion.

## Ways to fix it

Always use ``:=``

```
FILESEXTRAPATHS:prepend := "${THISDIR}/file"
```
