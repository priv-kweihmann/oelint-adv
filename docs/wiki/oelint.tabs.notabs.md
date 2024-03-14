# oelint.tabs.notabs

severity: warning

## Example

```
A = "\
<tab>1 \
"
```

## Why is this bad?

The [Yocto project style guide](https://docs.yoctoproject.org/contributor-guide/recipe-style-guide.html#variable-formatting) discourages the
use of tabs.

## Ways to fix it

Use spaces instead

```
A = "\
<spaces>1 \
"
```
