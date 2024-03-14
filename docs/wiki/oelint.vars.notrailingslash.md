# oelint.vars.notrailingslash

severity: error

## Example

In every bitbake recipe

```
S = "${WORDKIR}/foo/"
D = "${WORDKIR}/foo/"
T = "${WORDKIR}/foo/"
B = "${WORDKIR}/foo/"
```

## Why is this bad?

A trailing ``/`` on these selected variables will cause ``devtool`` to stop working properly.

## Ways to fix it

```
S = "${WORDKIR}/foo"
D = "${WORDKIR}/foo"
T = "${WORDKIR}/foo"
B = "${WORDKIR}/foo"
```
