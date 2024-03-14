# oelint.vars.srcurisrcrevtag

severity: error

## Example

In any bitbake recipe

```
SRC_URI += "git://foo.org/gaz.git;tag=${PV}"
SRCREV = "e5fa44f2b31c1fb553b6021e7360d07d5d91ff5e"
```

## Why is this bad?

``tag`` fetcher parameter and a ``SRCREV`` setting contradict each other.
``SRCREV`` is always preferred over the use of ``tag`` fetcher parameter.

## Ways to fix it

Use fixed revisions only and no ``tag`` parameter

```
SRC_URI += "git://foo.org/gaz.git"
SRCREV = "e5fa44f2b31c1fb553b6021e7360d07d5d91ff5e"
```
