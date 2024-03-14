# oelint.vars.srcuridomains

severity: warning

## Example

```
SRC_URI += "git://abc.group.com/a.git"
SRC_URI += "git://def.group.com/b.git"
```

## Why is this bad?

A recipe fetched from different domains will cause issues for instance when using ``devtool``.
Try to avoid if possible

## Ways to fix it

Move the second fetching type to a separate recipe, or if not possible suppress the finding (accepting the consequences)

```
SRC_URI += "git://abc.group.com/a.git"
# nooelint: oelint.vars.srcuridomains
SRC_URI += "git://def.group.com/b.git"
```
