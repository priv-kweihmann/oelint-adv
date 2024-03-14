# oelint.jetm.vars.dependssingleline

severity: warning

## Example

```
DEPENDS = "foo bar"
```

## Why is this bad?

Writing each ``DEPENDS`` or ``RDEPENDS`` item on a single line enables using ``grep`` to search a local file tree.

## Ways to fix it

Write every item on a single line

```
DEPENDS = "foo"
DEPENDS += "bar"
```
