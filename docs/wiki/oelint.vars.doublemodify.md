# oelint.vars.doublemodify

severity: error

## Example

In ``my-recipe_1.0.bb``

```
A:append += "1"
```

## Why is this bad?

Multiple (potentially conflicting) modify operations to the same variable, do not make sense and can lead to
unpredictable results

## Ways to fix it

Use just one modifier at a time

```
A:append = " 1"
```

or

```
A += "1"
```
