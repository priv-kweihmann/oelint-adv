# oelint.vars.srcurimutualex

severity: error

## Example

```
SRC_URI += "gitsm://github.com/CLIUtils/CLI11;branch=main;protocol=https"
SRCREV = "1233454566789"
SRC_URI[sha256sum] = "1233454566789"
```

## Why is this bad?

There is mutual exclusive information about the revision/artifact set.
Both could be used for validating the integrity of the artifact downloaded,
but only one is applicable for the fetcher used:

## Ways to fix it

Remove either the checksum or the ``SRCREV`` item, depending on the fetcher used
