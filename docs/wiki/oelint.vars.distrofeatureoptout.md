# oelint.vars.distrofeatureoptout

severity: warning

## Example

```
DISTRO_FEATURES:remove = "a"
```

## Why is this bad?

`:remove` is an operation that cannot be undone, hence it is discouraged to use.
Starting from `wrynose` release `DISTRO_FEATURES_OPTED_OUT` provides a way to remove `DISTRO_FEATURES`

## Ways to fix it

```
DISTRO_FEATURES_OPTED_OUT += "a"
```
