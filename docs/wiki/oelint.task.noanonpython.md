# oelint.task.noanonpython

severity: warning

## Example

```
python __anonymous() {
    print("foo")
}
```

or

```
python () {
    print("bar")
}
```

## Why is this bad?

Anonymous python functions are run every time the recipe is parsed.
This is expensive in terms of computing.
In addition, as the functions are run last in the parsing process, they can be full of side-effects and are
hard to debug.

## Ways to fix it

Turn into a separate function

```
python do_mytask() {
    print("foo")
}

addtask do_mytask before configure
```
