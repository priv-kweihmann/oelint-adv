# oelint.vars.specific

severity: error

## Example

```
A:append:fooarch = " foo"
```

## Why is this bad?

The override item should be known from either ``MACHINE``, ``MACHINEOVERRIDES``, ``PACKAGES`` or ``DISTRO``, otherwise
there is a high chance that the variable value will never be used.

## Ways to fix it

Use a known override - See the corresponding [README section](https://github.com/priv-kweihmann/oelint-adv#configure-your-custom-machine-or-distro-settings) or
if it's a ``PACKAGE`` set

```
PACKAGE_BEFORE_PN += "${PN}-mypackage"

FILES:${PN}-mypackage += "some/file"
```
