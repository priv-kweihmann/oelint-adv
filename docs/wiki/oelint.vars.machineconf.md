# oelint.vars.machineconf

severity: warn

## Example

```
IMAGE_INSTALL += "my-recipe"
DISTRO_FEATURES:append = " foo"
```

## Why is this bad?

Image and or distro specific settings should not be set by a machine configuration.

## Ways to fix it

Avoid using any of the following variables in a machine configuration

- DISTROOVERRIDES
- DISTRO_EXTRA_RDEPENDS
- DISTRO_EXTRA_RRECOMMENDS
- DISTRO_FEATURES
- DISTRO_FEATURES_BACKFILL
- DISTRO_FEATURES_BACKFILL_CONSIDERED
- DISTRO_FEATURES_DEFAULT
- IMAGE_INSTALL
