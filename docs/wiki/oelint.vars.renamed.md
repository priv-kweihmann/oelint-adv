# oelint.vars.renamed

severity: error

## Example

```
PNBLACKLIST = "1"
```

## Why is this bad?

Those variables were deprecated.
Some of them will be automatically renamed.

## Ways to fix it

Use the correct variable

```
SKIP_RECIPE = "1"
```

or in case of a removal by upstream remove the variable from the recipe code
