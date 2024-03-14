# oelint.vars.duplicate

severity: warning

## Example

In ``my-recipe_1.0.bb``

```
DEPENDS = "foo"
DEPENDS += "foo"
```

## Why is this bad?

There is no need to depend or (r)depend on the same recipe more than once.

## Ways to fix it

Remove the duplicates

```
DEPENDS = "foo"
```
