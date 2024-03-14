# oelint.vars.srcurigittag

severity: warning

## Example

In any bitbake recipe

```
SRC_URI += "git://foo.org/gaz.git;tag=${PV}"
```

## Why is this bad?

Use of the ``tag`` parameter is risky, as a tag can be forcefully and silently moved to a different
revision by the upstream repository, breaking reproducible builds.

## Ways to fix it

Use fixed revisions only

```
SRC_URI += "git://foo.org/gaz.git"
SRCREV = "e5fa44f2b31c1fb553b6021e7360d07d5d91ff5e"
```
