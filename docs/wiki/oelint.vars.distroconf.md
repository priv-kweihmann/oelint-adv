# oelint.vars.distroconf

severity: warn

## Example

```
IMAGE_INSTALL += "my-recipe"
MACHINE_FEATURES:append = " vfat"
```

## Why is this bad?

Image and or machine specific settings should not be set by a distro configuration.

## Ways to fix it

Avoid using any of the following variables in a distro configuration

- MACHINE
- MACHINE_ARCH
- MACHINE_ESSENTIAL_EXTRA_RDEPENDS
- MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS
- MACHINE_EXTRA_RRECOMMENDS
- MACHINE_FEATURES
- MACHINE_FEATURES_BACKFILL
- MACHINE_FEATURES_BACKFILL_CONSIDERED
- IMAGE_INSTALL
- MACHINEOVERRIDES
