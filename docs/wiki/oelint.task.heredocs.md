# oelint.task.heredocs

severity: warning

## Example

```
do_foo() {
    cat    >  ${D}/some.files <<   EOF
    kfkdfkd
    EOF
}
```

## Why is this bad?

Use of [heredocs](https://en.wikipedia.org/wiki/Here_document) creates a file with the permissions and
filemode bits of the current user running bitbake.
These could differ between users of the same recipe, leading to unpredictable results.

In addition heredocs are hard to read.

## Ways to fix it

create a file with the desired content, or make sure that the correct user and the correct
permissions are set using ``chown`` and ``install``

```
do_foo() {
    echo "kfkdfkd" > ${T}/some.files
    chown root:root ${T}/some.files
    install -m 0644 ${T}/some.files ${D}/some.files
}
```
