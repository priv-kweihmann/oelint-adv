# oelint.vars.pbpusage

severity: error

## Example

In ``my-recipe_1.0.bb``

```
SRC_URI = "file://${P}.patch"

BBCLASSEXTEND = "native"
```

## Why is this bad?

If compile for ``native`` (``my-recipe-native``) the value of ``${P}`` changes to ``my-recipe-native``, making the
build access a different file

## Ways to fix it

Always use ``${BP}`` instead

```
SRC_URI = "file://${BP}.patch"
```
