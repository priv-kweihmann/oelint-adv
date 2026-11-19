# oelint.var.rootfspostcmdsemicolon

severity: warning

## Example

In ``my-image.bb``

```
ROOTFS_POSTPROCESS_COMMAND += "abc; adef ;"
```

## Why is this bad?

Starting from `blacksail` release the variable is a space separated list instead of a `;` separated list.

## Ways to fix it

```
ROOTFS_POSTPROCESS_COMMAND += "abc adef"
```
