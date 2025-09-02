# oelint.vars.srcuriappend

severity: error

## Example

In any bitbake recipe

```
SRC_URI += "file://abc"
inherit def
```

## Why is this bad?

If the ``inherit`` class uses ``SRC_URI ?= "file://ghi"`` the setting would be ignored, a weak variable default only become
effective if there's no previous value.

Depending on what should be done the ``SRC_URI`` operation in the recipe should a
hard assignment ``SRC_URI = "file://abc"`` to override the default choices of the ``inherit`` class.

Or if it should be an ``append`` it needs to be ``SRC_URI:append = " file://abc"``

This check only will raise issues, if all of the requested `inherit` classes,
can be found in the same layer.

## Ways to fix it

To override any default value use

```
SRC_URI = "file://abc"
inherit def
```

or to append use

```
SRC_URI:append = " file://abc"
inherit def
```

if you can fix the original class that creates the weak define,
by using a small hack like

```
WEAK_DEF ?= "file://abc"
SRC_URI:prepend = "${WEAK_DEF} "
```
