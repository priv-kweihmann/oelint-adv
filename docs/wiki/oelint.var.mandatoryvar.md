# oelint.var.mandatoryvar

severity: error

## Example

In ``my-recipe_1.0.bb``

```
A = "1"
```

## Why is this bad?

Some variables should be always set to have more information about the purpose, license and origin of the sources
that this recipe is using.

## Ways to fix it

The following variables should always be set in the recipe

- SUMMARY
- DESCRIPTION
- HOMEPAGE
- LICENSE
- SRC_URI

```
SUMMARY = "My recipe"
DESCRIPTION = "My recipe that does all the magic"
HOMEPAGE = "https://my-homepage.com"
LICENSE = "MIT"
SRC_URI = "https://my-homepage.com/foo_${PV}.zip"
```
