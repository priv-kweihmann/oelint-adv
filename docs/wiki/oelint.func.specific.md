# oelint.func.specific

severity: error

## Example

```
do_install:append:fooarch() {
    abc
}
```

or

```
do_install:qemuall () {
    cp -r ${B}/testsuite ${D}${PTEST_PATH}/
    cp ${B}/.config      ${D}${PTEST_PATH}/
    ln -s /bin/busybox   ${D}${PTEST_PATH}/busybox
}
```

## Why is this bad?

The override item should be known from either ``MACHINE``, ``MACHINEOVERRIDES``, ``PACKAGES`` or ``DISTRO``, otherwise
there is a high chance that the function will never get run.

## Ways to fix it

Use a known override - See the corresponding [README section](https://github.com/priv-kweihmann/oelint-adv#configure-your-custom-machine-or-distro-settings) or
if it's a ``PACKAGE`` set

```
PACKAGE_BEFORE_PN += "${PN}-mypackage"

FILES:${PN}-mypackage += "some/file"
```
