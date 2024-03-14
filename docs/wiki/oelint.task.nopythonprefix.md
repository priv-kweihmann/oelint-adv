# oelint.task.nopythonprefix

severity: warning

## Example

```
python do_foo() {
    install -d ${D}/something
    ./configure
}
```

## Why is this bad?

Tasks that contain shell code should not be prefixed by ``python``, as bitbake would run
the code through the python interpreter.

## Ways to fix it

```
do_foo() {
    install -d ${D}/something
    ./configure
}
```
