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

### Fine tuning

To fine tuned the behavior on the rule, you can apply the following [constants](https://github.com/priv-kweihmann/oelint-adv#adding-additional-constants)

- `oelint-mandatoryvar/pkggroup-excludes` to skip mandatory variables in a packagegroup
- `oelint-mandatoryvar/image-excludes` to skip mandatory variables in images
- `oelint-mandatoryvar/srcuri-exclude-classes` to skip `SRC_URI`, because of a class inherited that defines `SRC_URI` already

e.g. if your custom class ``foo.bbclass`` contains

```
SRC_URI ?= "http://foo.com/{BPN}.zip"
```

but resides in a different layer than the current, you can run the linter with

```console
oelint-adv --constantmods=+.my-custom-src-uri-classes.json <other options> <file>...
```

with `.my-custom-src-uri-classes.json` being

```json
{
    "oelint-mandatoryvar": {
        "srcuri-exclude-classes": [
            "foo"
        ]
    }
}
```

to let the linter know that this is fine in the given context.

See also the [Configuration file](https://github.com/priv-kweihmann/oelint-adv#configuration-file) option to automatically apply that to the layer.
