# oelint.vars.homepageprefix

severity: warning

## Example

In ``my-recipe_1.0.bb``

```
HOMEPAGE = "ftp://abc-def.com"
```

## Why is this bad?

``HOMEPAGE`` should point to a website, that is reachable by the user - ``http`` and ``https`` considered the only valid prefixes.

## Ways to fix it

```
HOMEPAGE = "https://abc-def.com"
```