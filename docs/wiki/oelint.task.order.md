# oelint.task.order

severity: warning

## Example

```
do_compile() {
    :
}

do_unpack() {
    :
}
```

## Why is this bad?

For better readability the tasks should be written in a particular order.

## Ways to fix it

Write the tasks in the following order

- do_fetch
- do_unpack
- do_patch
- do_configure
- do_compile
- do_install
- do_populate_sysroot
- do_build
- do_package

```
do_unpack() {
    :
}

do_compile() {
    :
}
```
