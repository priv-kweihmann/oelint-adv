# oelint.var.override

severity: error

## Example

```
A = "2"

include foo.inc

A = "3"
```

## Why is this bad?

If in between hard variable assignments an immediate variable expansion is used (``:=`` operator) the value of ``A`` would be different
at different stages of the recipe, rendering the value unpredictable

## Ways to fix it

Avoid multiple hard assignments of the same variable.

```
A = "2"

include foo.inc
```

alternatively use weak assignments

```
A ?= "2"

include foo.inc

A = "3"
```
