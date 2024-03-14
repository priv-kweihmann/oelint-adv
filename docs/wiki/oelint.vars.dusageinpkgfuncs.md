# oelint.vars.dusageinpkgfuncs

severity: error

## Example

In ``my-recipe_1.0.bb``

```
pkg_preinst:${PN} () {
    if [ -n "${D}" ]; then
        echo "Foo"
    fi
}
```

## Why is this bad?

``${D}`` is only known to bitbake, while the ``pkg_*`` function can run on the actual target as well (through package management feature).

## Ways to fix it

Use ``$D`` instead

```
pkg_preinst:${PN} () {
    if [ -n "$D" ]; then
        echo "Foo"
    fi
}
```
