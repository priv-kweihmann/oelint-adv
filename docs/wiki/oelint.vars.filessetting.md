# oelint.vars.filessetting

severity: warning

## Example

In ``my-recipe_1.0.bb``

```
FILES:${PN} += "${bindir}"

PACKAGE_BEFORE_PN = "${PN}-mydev"

FILES:${PN}-mydev += "/some/path"
FILES:${PN}-mydev += "/some/path"
```

## Why is this bad?

Yocto/OE come with a predefined set of values from ``FILES``, so there is no need to add certain values twice.
Same applies for custom packages

## Ways to fix it

Remove the mentioned occurrences

```
PACKAGE_BEFORE_PN = "${PN}-mydev"

FILES:${PN}-mydev += "/some/path"
```
