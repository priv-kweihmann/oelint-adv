# oelint.vars.valuequoted

severity: error

## Example

```
A = "a
D = a"
```

## Why is this bad?

Variables should be properly quoted, otherwise they will not be parsed properly

## Ways to fix it

```
A = "a"
D = "a"
```
