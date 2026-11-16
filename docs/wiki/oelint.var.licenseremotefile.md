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

Also be aware that the template files in ``${COMMON_LIC_DIR}`` do lack copyright holder and year, rendering them
effectively useful for claiming the copyright on any sources/packages.

## Ways to fix it

Get in touch with the maintainer of the source code and ask them to ship a proper license file with
the release. Alternatively use a ``git://`` fetcher instead of downloading an archive.

```
LIC_FILES_CHKSUM = "file://LICENSE;md5=sjdjasdjhddh"
```

For file that reside in the same layer, please add a copy of your license (including your name) and the year,
via ``SRC_URI`` with another ``file://`` fetcher

Another way to "fix" it is to use the ``oelint-licenseremotefile-optout`` entry of the [Constants interface](https://github.com/priv-kweihmann/oelint-adv/tree/master/docs/constants.md).
For given case adding ``${COMMON_LIC_DIR}/MIT`` to the list of entries, would also suppress initially reported finding.
