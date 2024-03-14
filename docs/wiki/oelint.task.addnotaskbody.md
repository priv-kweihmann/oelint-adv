# oelint.task.addnotaskbody

severity: warning

## Example

```
do_foo() {

}
addtask do_foo
```

## Why is this bad?

A task without code is considered illegal syntax.

## Ways to fix it

Fill the task with code instructions

```
do_foo() {
    call some code here
}
addtask do_foo
```

or add

```
do_foo() {
    :
}
addtask do_foo
```

to indicate any empty task
