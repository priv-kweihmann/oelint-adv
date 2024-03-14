# oelint.vars.bugtrackerisurl

severity: warning

## Example

In ``my-recipe_1.0.bb``

```
BUGTRACKER = "Black board in the kitchen"
```

## Why is this bad?

``BUGTRACKER`` should be a URL, otherwise setting the value doesn't add any value.

## Ways to fix it

```
BUGTRACKER = "https://black-board.kitchen.org"
```
