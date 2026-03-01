# oelint.vars.dependsordered

severity: warning

## Example

In ``my-recipe_1.0.bb``

```
DEPENDS = "\
    z \
    a \
    f \
"
```

## Why is this bad?

For better readability (and to avoid added the same value multiple times) ``DEPENDS`` should be ordered alphabetically.
And that applies to all files within a single layer, meaning additions in include files are also matched, equally as
bbappends to the same file within the same layer.

bbappends from files out of the original bb-file's scope are exempt

## Ways to fix it

```
DEPENDS = "\
    a \
    f \
    z \
"
```

**NOTE**: if you get reports from include files it is heavily advised to either make sure the ordering is kept intact
or, if that is not feasible, move all entries to the main bb recipe file.
