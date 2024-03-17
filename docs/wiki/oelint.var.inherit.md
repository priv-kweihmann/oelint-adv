# oelint.var.inherit

severity: warning

## Example

```
inherit ${A}
```

or

```
inherit_defer A
```

## Why is this bad?

``inherit_defer`` should be used if the class is determined by a variable.
``inherit`` should be used if the content is static.

## Ways to fix it

```
inherit_defer ${A}
```

or

```
inherit A
```