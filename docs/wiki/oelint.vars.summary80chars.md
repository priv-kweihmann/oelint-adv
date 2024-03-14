# oelint.vars.summary80chars

severity: warning

## Example

In any bitbake recipe

```
SUMMARY = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
```

## Why is this bad?

The [OpenEmbedded Style guide](https://www.openembedded.org/index.php?title=Styleguide&oldid=10281) requires ``SUMMARY`` to be
a maximum of 80 characters long

## Ways to fix it

```
SUMMARY = "Something shorter than 80 characters"
```
