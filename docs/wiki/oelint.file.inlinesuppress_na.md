# oelint.file.inlinesuppress_na

severity: info

## Example

```
# nooelint: some.warning
A = "1"
```

## Why is this bad?

A warning couldn't be reproduced from the line in question, meaning that there is no warning of the
specified ID.

## Ways to fix it

remove the ``nooelint`` line

```
A = "1"
```
