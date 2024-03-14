# oelint.task.customorder

severity: error

## Example

```
do_bar() {
    :
}

addtask do_bar after compile before configure
```

## Why is this bad?

The task creates a cyclic or illogical dependency between tasks.

## Ways to fix it

The common order of functions is

- do_fetch
- do_unpack
- do_patch
- do_configure
- do_compile
- do_install
- do_package

make sure setup the custom task to fit into this sequential order

```
do_bar() {
    :
}

addtask do_bar after compile before do_package
```
