# oelint.file.includerelpath

severity: warning

## Example

```
include ../../include-file.inc
```

## Why is this bad?

This makes assumptions about the layout, how layers are stored on the storage of the local
workspace.
If now someone places the files in a different layout, the include will be broken.

## Ways to fix it

Use a relative path from the layer root instead

```
include recipes-something/some-path/include-file.inc
```
