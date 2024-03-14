# oelint.var.multiinherit

severity: warning

## Example

In ``my-recipe_1.0.bb``

```
inherit abc
inherit abc
```

## Why is this bad?

Inheriting the same file more than once, doesn't add value and likely will modify variables and functions multiple times,
leading all kinds of undesired effects.

## Ways to fix it

Only inherit the same file once

```
inherit abc
```
