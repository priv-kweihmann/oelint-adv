# oelint.vars.listappend

severity: error

## Example

```
RDEPENDS:${PN} .= "bar"
RDEPENDS:${PN}:append = "bar"
```

or

```
RDEPENDS:${PN} =. "bar"
RDEPENDS:${PN}:prepend = "bar"
```

## Why is this bad?

``append`` operations need to start with a leading space.
``prepend`` operations need to end with trailing space.

Otherwise it will be just added to a potentially existing value.

Like

```
RDEPENDS:${PN} = "foo"
RDEPENDS:${PN}:prepend = "bar"
```

will result in ``RDEPENDS:${PN} = "barfoo"``, while ``RDEPENDS:${PN} = "bar foo"`` is most likely the desired outcome

## Ways to fix it

```
RDEPENDS:${PN} .= " bar"
RDEPENDS:${PN}:append = " bar"
```

or

```
RDEPENDS:${PN} =. "bar "
RDEPENDS:${PN}:prepend = "bar "
```
