# oelint.task.network

severity: warning

## Example

```
do_compile[network] = "1"
```

## Why is this bad?

It means that during compilation code could be fetched from a network.
That implies that the code cannot be reliably reproduced offline or even in the
future as remote network resources could vanish over time

## Ways to fix it

Inspect why the code is needing network access and engage with upstream to
discuss the options
