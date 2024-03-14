# oelint.bbclass.underscores

severity: error

## Example

`my-class.bbclass`

## Why is this bad?

Bitbake tries to create shell and/or python functions out of the base name of the class when
using ``EXPORT_FUNCTIONS`` in this particular class.
``-`` is unfortunately not a valid symbol in neither shell nor python.

## Ways to fix it

Use ``_`` instead of ``-`` in the filename.
