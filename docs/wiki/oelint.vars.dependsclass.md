# oelint.vars.dependsclass

severity: error

## Example

In ``my-recipe_1.0.bb``

```
inherit native
DEPENDS = "bar"
```

## Why is this bad?

This would depend on the ``target`` variant of ``bar``, while most likely it should depend on the ``native`` variant.

## Ways to fix it

```
inherit native
DEPENDS = "bar-native"
```
