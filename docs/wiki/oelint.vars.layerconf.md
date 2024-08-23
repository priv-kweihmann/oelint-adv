# oelint.vars.layerconf

severity: warn

## Example

```
IMAGE_INSTALL += "my-recipe"
```

## Why is this bad?

A setting from a ``layer.conf`` becomes effective, just by including the layer into the build.
Adding settings beyond the pure layer configuration should be reserved for machine, distro or image configuration.

## Ways to fix it

Only the following variables should be set as part of a ``layer.conf``

- BBFILES
- BBFILES_DYNAMIC
- BBFILE_COLLECTIONS
- BBFILE_PATTERN_.*
- BBFILE_PRIORITY_.*
- BBPATH
- HOSTTOOLS_NONFATAL
- LAYERDEPENDS_.*
- LAYERRECOMMENDS_.*
- LAYERSERIES_COMPAT_.*
- LAYERVERSION_.*
- LICENSE_PATH
