# oelint.vars.descriptionsame

severity: warning

## Example

In ``my-recipe_1.0.bb``

```
SUMMARY = "ABC"
DESCRIPTION = "ABC"
```

## Why is this bad?

``DESCRIPTION`` defaults to ``SUMARRY`` in the standard Yocto project configuration.
No need to set both to the same value.

## Ways to fix it

Set ``DESCRIPTION`` to a different value than ``SUMMARY`` or remove ``DESCRIPTION`` entirely.
