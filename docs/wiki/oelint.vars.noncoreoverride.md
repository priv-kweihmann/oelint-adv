# oelint.vars.noncoreoverride

severity: error

## Example

In a custom bbappend

```
do_install:append() {
    some op
}
```

or

```
PACKAGE_BEFORE_PN += "${PN}-custom"
```

## Why is this bad?

If the layer should be compatible with the [Yocto Project Compatible Program](https://docs.yoctoproject.org/current/dev-manual/layers.html#making-sure-your-layer-is-compatible-with-yocto-project), any override of the standard core implementation needs to be
avoided, **OR** made specific to a MACHINE or DISTRO provided this this 3rd party layer or others (but core).

If not done properly it will not pass the checks of the ``yocto-check-layer`` script, which is also
very expensive to run, as relatively slow

## Ways to fix it

```
do_install:append:my-distro() {
    some op
}
```

or

```
PACKAGE_BEFORE_PN:append:my-machine = " ${PN}-custom"
```
