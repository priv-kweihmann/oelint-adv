# oelint.vars.notneededspace

severity: info

## Example

In every bitbake file

```
VAR += " a"
```

## Why is this bad?

The leading space is unnecessary and will just bloat the resulting command line(s)

## Ways to fix it

```
VAR += "a"
```
