# oelint.vars.pnbpnusage

severity: error

## Example

In ``my-recipe_1.0.bb``

```
SRC_URI = "file://${PN}.patch"

BBCLASSEXTEND = "native"
```

## Why is this bad?

If compile for ``native`` (``my-recipe-native``) the value of ``${PN}`` changes to ``my-recipe-native``, making the
build access a different file

## Ways to fix it

Always use ``${BPN}`` instead

```
SRC_URI = "file://${BPN}.patch"
```
