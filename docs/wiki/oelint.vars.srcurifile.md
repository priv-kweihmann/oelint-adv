# oelint.vars.srcurifile

severity: warning

## Example

In any recipe

```
SRC_URI += "file://abc"
SRC_URI += "git://foo.org/gaz.git"
```

## Why is this bad?

When using ``devtool check-upgrade-status`` to check for updates of the recipe, ``devtool`` only uses the
first item of ``SRC_URI`` - in this case a ``file`` fetcher that will not change.

Leading potentially to missing out on upstream updates to the source code

## Ways to fix it

Put ``file`` fetcher at the end of the ``SRC_URI`` list

```
SRC_URI += "git://foo.org/gaz.git"
SRC_URI += "file://abc"
```
