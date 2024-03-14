# oelint.vars.autorev

severity: warning

## Example

In ``my-recipe_1.0.bb``

```
SRCREV = "${AUTOREV}"
```

## Why is this bad?

``AUTOREV`` will pull always the latest commit, breaking reproducible builds in general.
The usage is discouraged in general other than for local experiments.

## Ways to fix it

Use a fixed revision

```
SRCREV = "e5fa44f2b31c1fb553b6021e7360d07d5d91ff5e"
```
