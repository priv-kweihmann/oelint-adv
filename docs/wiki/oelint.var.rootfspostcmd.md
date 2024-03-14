# oelint.var.rootfspostcmd

severity: warning

## Example

In ``my-image.bb``

```
ROOTFS_POSTPROCESS_COMMAND += "abc; adef ;;"
```

## Why is this bad?

Do not leave extra spaces between the function name and ``;``, these can cause that appends to the image, can remove the
function anymore

## Ways to fix it

```
ROOTFS_POSTPROCESS_COMMAND += "abc; adef;;"
```
