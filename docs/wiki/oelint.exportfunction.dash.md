# oelint.exportfunction.dash

severity: error

## Example

In ``my_class.bbclass``

```
EXPORT_FUNCTIONS my_class_do-install
```

## Why is this bad?

Bitbake tries to create shell and/or python functions out of the base name of the class when
using ``EXPORT_FUNCTIONS``.
``-`` is unfortunately not a valid symbol in neither shell nor python.

## Ways to fix it

```
EXPORT_FUNCTIONS my_class_do_install
```
