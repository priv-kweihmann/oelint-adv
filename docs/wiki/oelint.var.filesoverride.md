# oelint.var.filesoverride

severity: warning

## Example

In ``my-recipe_1.0.bb``

```
FILES:${PN} = " foo"
```

## Why is this bad?

Override of ``FILES`` can lead to files accidentally installed into a different than the desired package.
Do not override the default of Yocto/OE.

## Ways to fix it

Append instead

```
FILES:${PN} += " foo"
```
