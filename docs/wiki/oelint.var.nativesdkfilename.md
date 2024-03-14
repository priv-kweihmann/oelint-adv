# oelint.var.nativesdkfilename

severity: warning

## Example

In ``my-recipe_1.0.bb``

```
inherit nativesdk
```

## Why is this bad?

``nativesdk`` only recipes should have ``nativesdk-`` in their filename.
This makes it much easier to identify them.

## Ways to fix it

Rename the file to ``nativesdk-my-recipe_1.0.bb``
