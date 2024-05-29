# oelint.file.includenotfound

severity: warning

## Example

```
include this/file/does/not/exist.inc
```

or

```
include a/file/from/another/layer.inc
```


## Why is this bad?

If an include file doesn't reside in the same layer, it creates an external dependency on something
that is likely beyond the control of the layer.
It will create breakage if the other layer changes the name and/or the path of the include file.

Or the include simply doesn't exit at all.

## Ways to fix it

Fix the include path or

```
# nooelint: oelint.file.includenotfound
include a/file/from/another/layer.inc
```

in case the include file is from another layer.
