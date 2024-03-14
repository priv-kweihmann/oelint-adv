# oelint.var.multiinclude

severity: warning

## Example

In ``my-recipe_1.0.bb``

```
include abc.inc
include abc.inc
```

## Why is this bad?

Including the same file more than once, doesn't add value and likely will modify variables and functions multiple times,
leading all kinds of undesired effects.

## Ways to fix it

Only include the same file once

```
include abc.inc
```
