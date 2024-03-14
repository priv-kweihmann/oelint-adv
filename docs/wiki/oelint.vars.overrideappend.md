# oelint.vars.overrideappend

severity: warning

## Example

In every bitbake file

```
A = "a"
A:class-target:append = " b"
```

## Why is this bad?

This would create an empty set of ``A`` for ``class-target`` and then ``append`` ``b``,
but most likely what should have been done is take the original value of ``A``
and add ``b`` in case the recipe is compiled for the target.

## Ways to fix it

``append`` (or ``prepend`` or ``remove``) always comes first, then the other overrides

```
A = "a"
A:append:class-target = " b"
```
