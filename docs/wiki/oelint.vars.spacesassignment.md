# oelint.vars.spacesassignment

severity: warning

## Example

In any bitbake file

```
A ="1"
```

## Why is this bad?

For better readability it's advised to write variable operations always like ``A = "1"``, with
a single space surrounding the variable operation.

## Ways to fix it

```
A = "1"
```
