# oelint.var.nativefilename

severity: warning

## Example

In ``my-recipe_1.0.bb``

```
inherit native
```

## Why is this bad?

``native`` only recipes should have ``-native`` in their filename.
This makes it much easier to identify them.

## Ways to fix it

Rename the file to ``my-recipe-native_1.0.bb``
