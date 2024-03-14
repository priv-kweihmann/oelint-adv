# oelint.vars.pnusagediscouraged

severity: warning

## Example

In any bitbake recipe

```
HOMEPAGE = "http://${PN}.com"
DESCRIPTION = "http://${BPN}.com"
```

## Why is this bad?

For a selection of variables, that provide metadata the use of ``${PN}`` and ``${BPN}`` is discouraged, as those
variables provide links.
And in a unexpanded form they are not clickable immediately from the IDE or editor, leading to manual work.

Also there is little use in using a variable here, as the information likely will remain static anyway.

## Ways to fix it

For variables

- SUMMARY
- HOMEPAGE
- BUGTRACKER
- DESCRIPTION

remove the use of ``${PN}`` and ``${BPN}``

```
HOMEPAGE = "http://foo-bar.com"
DESCRIPTION = "http://foo-bar.com"
```
