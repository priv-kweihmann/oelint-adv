# oelint.vars.virtual

severity: error

## Example

```
RDEPENDS:${PN} = "virtual/kernel"
```

## Why is this bad?

The use of ``virtual/`` items is limited to ``DEPENDS`` and ``PROVIDES``, all runtime
related items such as ``RDEPENDS``, ``RPROVIDES`` a.s.o. will ignore ``virtual/`` items.

## Ways to fix it

Avoid ``virtual/`` items and use the really package name

```
RDEPENDS:${PN} = "linux-yocto"
```
