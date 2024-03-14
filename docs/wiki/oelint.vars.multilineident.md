# oelint.vars.multilineident

severity: info

## Example

On every multiline variable assignment

```
A = "\
    a \
b \
"
```

## Why is this bad?

For better readability the [Yocto project style guide](https://docs.yoctoproject.org/contributor-guide/recipe-style-guide.html#variable-formatting)
suggests to use a common indent (minimum 4 spaces) matching the first ``"`` on the starting line

## Ways to fix it

```
A = "\
    a \
    b \
"
```
