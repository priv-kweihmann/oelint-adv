# oelint.vars.modifyoverride

severity: warning

## Example

In every bitbake file

```
A = "a"
A:class-target += " b"
```

## Why is this bad?

This would append to ``A:class-target`` variable, which would later override ``A``,
but most likely what should have been done is ``:append`` to ``A``.

## Ways to fix it

``append`` (or ``prepend``) instead of using ``+=`` (or ``.=``, ``=+``, ``=.``)

```
A = "a"
A:append:class-target = " b"
```
