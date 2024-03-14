# oelint.task.multifragments

severity: info

## Example

```
do_install:append() {
    a
}
do_install:append() {
    b
}
```

## Why is this bad?

Multiple appends, removes, prepends, a.s.o. should be merged into a single append, remove, prepend for better readability.

## Ways to fix it

```
do_install:append() {
    a
    b
}
```
