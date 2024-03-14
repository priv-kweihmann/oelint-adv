# oelint.vars.fileextrapaths

severity: warning

## Example

In ``my-recipe_1.0.bb``

```
FILESEXTRAPATHS:prepend := "${THISDIR}/file"
```

## Why is this bad?

``FILESEXTRAPATHS`` shouldn't be used in a ``bb`` file - please stick to the common folder structure provided by
Yocto/OE configuration instead.
In 99.99999999999% of the cases their is no need to create an additional search path in a recipe.

## Ways to fix it

Remove usage of ``FILESEXTRAPATHS`` in ``bb`` files.
