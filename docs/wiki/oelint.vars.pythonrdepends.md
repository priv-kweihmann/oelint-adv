# oelint.vars.pythonrdepends

severity: warning

## Example

```
RDEPENDS:${PN} = "python3"
```

## Why is this bad?

This will install the entire python ecosystem on your target, which adds >50Mb of footprint.
It is much better to just install the sub-package needed, like ``python3-core``.

## Ways to fix it

Find the needed packages using the information found at

- `meta/recipes-devtools/python/python3/python3-manifest.json`
- `meta/recipes-devtools/python/python/python-manifest.json`

in the `openembedded-core`/`poky` repository.

or recreate the recipe using `recipetool`
