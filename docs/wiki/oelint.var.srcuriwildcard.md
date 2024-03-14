# oelint.var.srcuriwildcard

severity: error

## Example

In ``my-recipe_1.0.bb``

```
SRC_URI = "file://*"
```

## Why is this bad?

File wildcards are discouraged, as bitbake might not see changes to the directory, thus missing out on rebuilds.

## Ways to fix it

Use a fixed list of files

```
SRC_URI = "file://file1 file://file2"
```
