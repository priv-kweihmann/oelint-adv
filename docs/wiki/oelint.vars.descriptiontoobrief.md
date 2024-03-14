# oelint.vars.descriptiontoobrief

severity: warning

## Example

In ``my-recipe_1.0.bb``

```
SUMMARY = "ABC"
DESCRIPTION = "AB"
```

## Why is this bad?

``DESCRIPTION`` should give more text than ``SUMMARY``

## Ways to fix it

Set ``DESCRIPTION`` to a longer value than ``SUMMARY`` or remove ``DESCRIPTION`` entirely.
