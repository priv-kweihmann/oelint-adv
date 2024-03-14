# oelint.vars.appendop

severity: error

## Example

In ``my-recipe_1.0.bb``

```
A ??= "1"
A += "2"
```

## Why is this bad?

When using weak defines in combination with ``+=`` the latter operation overwrite the entire value of ``A``

## Ways to fix it

Use ``append`` instead

```
A ??= "1"
A:append = " 2"
```
