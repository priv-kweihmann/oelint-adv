# oelint.vars.summarylinebreaks

severity: warning

## Example

In any bitbake recipe

```
SUMMARY = "a\nb\nc"
```

## Why is this bad?

The [OpenEmbedded Style guide](https://www.openembedded.org/index.php?title=Styleguide&oldid=10281) requires ``SUMMARY`` a single line

## Ways to fix it

```
SUMMARY = "a b c"
```
