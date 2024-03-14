# oelint.vars.insaneskip

severity: error

## Example

```
INSANE_SKIP:${PN} = "ldflags"
```

## Why is this bad?

Use of ``INSANE_SKIP`` effectively disables core quality checks, rendering the outcome
potentially unusable

## Ways to fix it

Avoid the usage of ``INSANE_SKIP``.
For situations where it is still necessary use

```
# nooelint: oelint.vars.insaneskip - the reason goes here as a comment
INSANE_SKIP:${PN} = "ldflags"
```