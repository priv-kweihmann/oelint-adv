# oelint.file.requireinclude

severity: warning

## Example

In ``my-recipe_1.0.bb``

```
include some-include-file.inc
```

## Why is this bad?

``include`` statement fail silently is the file is not found.
``require`` will fail if the file hasn't been found.

## Ways to fix it

```
require some-include-file.inc
```

or if that is indented behavior

```
# nooelint: oelint.file.requireinclude
include some-include-file.inc
```
