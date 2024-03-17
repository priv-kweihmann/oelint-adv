# oelint.var.inheritdevtool

severity: warning

## Example

```
inherit nativesdk
```

or

```
inherit native
```

## Why is this bad?

Bitbake complains if ``native`` or ``nativesdk`` are not inherited last.
When using ``devtool``, a few extra classes are inherited, hence it's better to use
``inherit_defer native`` or ``inherit_defer nativesdk``, even if there are not based on
variables.

## Ways to fix it

```
inherit_defer nativesdk
```

or

```
inherit_defer native
```
