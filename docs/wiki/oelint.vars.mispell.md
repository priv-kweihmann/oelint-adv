# oelint.vars.mispell

severity: warning

## Example

In any bitbake file

```
DPENDS += "foo"
```

## Why is this bad?

The variable name is not known but looks very similar to a known one.
Likely that is a typo.

## Ways to fix it

```
DEPENDS += "foo"
```
