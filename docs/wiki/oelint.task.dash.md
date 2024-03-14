# oelint.task.dash

severity: error

## Example

```
do_my-task() {
    :
}
```

## Why is this bad?

As bitbake renders the task into python or shell functions we can't use ``-`` in the name, as this is
an illegal character for the shell and python interpreter

## Ways to fix it

Use ``_`` instead

```
do_my_task() {
    :
}
```
