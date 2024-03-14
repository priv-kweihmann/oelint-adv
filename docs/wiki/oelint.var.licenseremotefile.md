# oelint.var.licenseremotefile

severity: warning

## Example

```
LIC_FILES_CHKSUM = "file://${COMMON_LIC_DIR}/MIT;md5=sjdjasdjhddh"
```

## Why is this bad?

This works around the license detection.
Changes in LICENSE won't be found in that case.
Also this is prone to setting the wrong LICENSE in the recipe.

## Ways to fix it

Get in touch with the maintainer of the source code and ask them to ship a proper license file with
the release. Alternatively use a ``git://`` fetcher instead of downloading an archive.

```
LIC_FILES_CHKSUM = "file://LICENSE;md5=sjdjasdjhddh"
```
