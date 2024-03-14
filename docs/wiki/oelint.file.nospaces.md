# oelint.file.nospaces

severity: error

## Example

File ``/some/file/with/a /space/ in /its/path.bb``

## Why is this bad?

Bitbake doesn't support spaces at any place in the absolute file path.

## Ways to fix it

Rename to ``/some/file/with/a_/space/_in_/its/path.bb``
