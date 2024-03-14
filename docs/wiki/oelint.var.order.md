# oelint.var.order

severity: warning

## Example

In ``my-recipe_1.0.bb``

```
inherit cmake

SRCREV = "f161ebd29699d93411cec0915c5133c0f3229a28"
SRC_URI = "git://some.repo.com/repo.git"
```

## Why is this bad?

For readability and to avoid situations where immediate variable expansion is used (``:=`` operator), variables should be
set in the defined order.

## Ways to fix it

Variables should be set in the following order

- SUMMARY
- DESCRIPTION
- AUTHOR
- HOMEPAGE
- BUGTRACKER
- SECTION
- LICENSE
- LIC_FILES_CHKSUM
- DEPENDS
- PROVIDES
- PV
- SRC_URI
- SRCREV
- S
- inherit
- PACKAGECONFIG
- EXTRA_QMAKEVARS_POST
- EXTRA_OECONF
- PACKAGE_ARCH
- PACKAGES
- FILES
- RDEPENDS
- RRECOMMENDS
- RSUGGESTS
- RPROVIDES
- RCONFLICTS
- BBCLASSEXTEND

```
SRC_URI = "git://some.repo.com/repo.git"
SRCREV = "f161ebd29699d93411cec0915c5133c0f3229a28"

inherit cmake
```
