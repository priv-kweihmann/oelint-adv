# oelint.vars.pkgspecific

severity: error

## Example

In any bitbake file

```
RDEPENDS += "foo"
```

## Why is this bad?

A selection of variables/functions are known to be package specific.
Omitting a package override makes the build ignore the setting at all

## Ways to fix it

The following variables/functions are known to be package specific

- RDEPENDS
- RRECOMMENDS
- RSUGGESTS
- RCONFLICTS
- RPROVIDES
- RREPLACES
- FILES
- pkg_preinst
- pkg_postinst
- pkg_prerm
- pkg_postrm
- ALLOW_EMPTY

```
RDEPENDS:${PN} += "foo"
```
