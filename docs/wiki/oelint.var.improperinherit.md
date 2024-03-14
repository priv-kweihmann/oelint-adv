# oelint.var.improperinherit

severity: error

## Example

```
inherit abc/abc
```

or

```
inherit def~AAAA
```

## Why is this bad?

``inherit`` statements only support [A-Za-z0-9-_] characters

## Ways to fix it

Avoid unsupported characters

```
inherit abc
```
