# oelint.file.requirenotfound

severity: warning

## Example

```
require this/file/does/not/exist.inc
```

or

```
require a/file/from/another/layer.inc
```


## Why is this bad?

If a required file doesn't reside in the same layer, it creates an external dependency on something
that is likely beyond the control of the layer.
It will create breakage if the other layer changes the name and/or the path of the required file.

Or the required file simply doesn't exit at all.

## Ways to fix it

Fix the required file path or

```
# nooelint: oelint.file.requirenotfound
require a/file/from/another/layer.inc
```

in case the required file is from another layer.
