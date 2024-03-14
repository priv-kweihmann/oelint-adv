# oelint.var.suggestedvar

severity: info

## Example

In ``my-recipe_1.0.bb``

```
A = "2"
```

## Why is this bad?

A few variables are suggested to be added, as it adds more information what the recipe is about.
In terms of ``CVE_PRODUCT`` it also helps to avoid false positives of the CVE check functionality.

## Ways to fix it

The following variables are suggested to be added to each recipe

- AUTHOR
- BUGTRACKER
- BBCLASSEXTEND
- CVE_PRODUCT
- SECTION

```
AUTHOR = "me <me@mine.org>"
BUGTRACKER = "https://my-homepage/issues"
CVE_PRODUCT = "me/lib"
SECTION = "graphics"

BBCLASSEXTEND = "native"
```
