# oelint.var.bbclassextend

severity: info

## Example

In ``my-recipe_1.0.bb``

```
A = "2"
```

## Why is this bad?

To allow the use in the SDK or as a ``native`` variant ``BBCLASSEXTEND`` should be set.

## Ways to fix it

```
A = "2"

BBCLASSEXTEND = "native nativesdk"
```
