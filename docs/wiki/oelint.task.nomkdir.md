# oelint.task.nomkdir

severity: error

## Example

```
do_install() {
    mkdir -p ${D}/foo
}
```

## Why is this bad?

``mkdir`` uses the current user's settings for default permissions, which can differ across multiple users.

## Ways to fix it

Use ``install -d`` instead

```
do_install() {
    install -d ${D}/foo
}
```

