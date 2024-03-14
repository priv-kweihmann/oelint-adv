# oelint.var.addpylib

severity: error

## Example

in ``my-recipe_1.0.bb``

```
addpylib ${LAYERDIR}/foo a
```

## Why is this bad?

The ``addpylib`` statement is only valid in ``.conf`` files, such as ``distro.conf`` and ``layer.conf``

## Ways to fix it

Remove the statement and if needed move it to ``layer.conf``
