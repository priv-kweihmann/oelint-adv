# oelint.vars.inconspaces

severity: error

## Example

In a recipe

```
VAR += " ffjjj"
VAR:append = "fhhh"
```

## Why is this bad?

``+=`` will add a `` `` automatically, while for ``append`` operation this has to be done explicitly

## Ways to fix it

```
VAR += "ffjjj"
VAR:append = " fhhh"
```
