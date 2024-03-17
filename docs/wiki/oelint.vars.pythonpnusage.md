# oelint.vars.pythonpnusage

severity: info

## Example

```
A = "${PYTHON_PN}"
```

## Why is this bad?

``${PYTHON_PN}`` was marked deprecated from ``scarthgap`` release.

## Ways to fix it

Use ``python3`` instead

```
A = "python3"
```
