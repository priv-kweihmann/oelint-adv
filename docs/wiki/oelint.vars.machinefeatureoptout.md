# oelint.vars.machinefeatureoptout

severity: warning

## Example

```
MACHINE_FEATURES:remove = "a"
```

## Why is this bad?

`:remove` is an operation that cannot be undone, hence it is discouraged to use.
Starting from `wrynose` release `MACHINE_FEATURES_OPTED_OUT` provides a way to remove `MACHINE_FEATURES`

## Ways to fix it

```
MACHINE_FEATURES_OPTED_OUT += "a"
```
