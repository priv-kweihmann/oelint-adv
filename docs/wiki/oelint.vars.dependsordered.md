# oelint.vars.dependsordered

severity: warning

## Example

In ``my-recipe_1.0.bb``

```
DEPENDS = "\
    z \
    a \
    f \
"
```

## Why is this bad?

For better readability (and to avoid added the same value multiple times) ``DEPENDS`` should be ordered alphabetically

## Ways to fix it

```
DEPENDS = "\
    a \
    f \
    z \
"
```
