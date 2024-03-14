# oelint.task.nocopy

severity: error

## Example

```
do_install() {
    cp ${WORKDIR}/foo ${D}/foo
}
```

## Why is this bad?

``cp`` uses the current user's settings for default permissions, which can differ across multiple users.

## Ways to fix it

Use ``install`` instead

```
do_install() {
    install ${WORKDIR}/foo ${D}/foo
}
```
