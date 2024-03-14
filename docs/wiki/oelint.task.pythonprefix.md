# oelint.task.pythonprefix

severity: warning

## Example

```
do_foo() {
    import os
    print(os.getcwd())
}
```

## Why is this bad?

Tasks that contain python code should be prefixed by ``python``, as bitbake would run
the code through the shell interpreter instead.

## Ways to fix it

```
python do_foo() {
    import os
    print(os.getcwd())
}
```
