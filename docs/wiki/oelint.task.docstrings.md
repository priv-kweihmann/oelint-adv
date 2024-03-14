# oelint.task.docstrings

severity: info

## Example

```
do_my_task() {
    :
}
addtask do_my_task
```

## Why is this bad?

Every custom task should have a docstring set, so users get more information about the use of this task.
Also it is very helpful information for ``bitbake <recipe> -c listtasks``.

## Ways to fix it

```
do_my_task() {
    :
}
addtask do_my_task
do_my_task[doc] = "This is my custom task, doing something magical"
```
