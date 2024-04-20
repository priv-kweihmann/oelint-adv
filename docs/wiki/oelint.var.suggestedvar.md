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

### Fine tuning

To fine tuned the behavior on the rule, you can apply the following [constants](https://github.com/priv-kweihmann/oelint-adv#adding-additional-constants)

- `oelint-suggestedvar/pkggroup-excludes` to skip suggestedvar variables in a packagegroup
- `oelint-suggestedvar/image-excludes` to skip suggestedvar variables in images
- `oelint-suggestedvar/{varname}-exclude-classes` to skip `{varname}`, because of a class inherited that defines the variable already

e.g. if your custom class ``foo.bbclass`` contains

```
BUGTRACKER = "https://my-homepage/issues"
CVE_PRODUCT ?= "my/product"
```

but resides in a different layer than the current, you can run the linter with

```console
oelint-adv --constantmods=+.my-custom-src-uri-classes.json <other options> <file>...
```

with `.my-custom-src-uri-classes.json` being

```json
{
    "oelint-suggestedvar": {
        "BUGTRACKER-exclude-classes": [
            "foo"
        ],
        "CVE_PRODUCT-exclude-classes": [
            "foo"
        ]
    }
}
```

to let the linter know that this is fine in the given context.

See also the [Configuration file](https://github.com/priv-kweihmann/oelint-adv#configuration-file) option to automatically apply that to the layer.
