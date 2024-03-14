# oelint.vars.dependsappend

severity: error

## Example

In ``my-recipe_1.0.bb``

```
inherit something
DEPENDS = "bar"
```

## Why is this bad?

The ``inherit`` (or ``include`` or ``require``) statement will pull in code that might set ``DEPENDS`` as well.
In the end those setting would be overwritten if ``DEPENDS`` is set after that.

## Ways to fix it

Move ``DEPENDS`` before any ``inherit`` or ``include`` or ``require`` statement

```
DEPENDS = "bar"
inherit something
```

or use

```
inherit something
DEPENDS += "bar"
```
