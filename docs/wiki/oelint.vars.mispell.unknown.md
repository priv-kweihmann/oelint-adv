# oelint.vars.mispell.unknown

severity: info

## Example

```
MY_CUSTOM_VARIABLE = "1"
```

## Why is this bad?

As the variable is not known, it is advised to create a layer specific oelint-adv ``--constantmod`` extension.

## Ways to fix it

Create a ``--constantmod`` extension and reference it while running the linter.
