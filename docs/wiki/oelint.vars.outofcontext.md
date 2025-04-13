# oelint.vars.outofcontext

severity: warning

## Example

On a normal recipe like `test_1.0.bb`

```
MACHINEOVERRIDES .= "foo:"
```

## Why is this bad?

The variables flagged by the linter rule should only be applied in a very specific context.

e.g. variables meant for recipes (`.bb`, `.bbappend`) used in a global scope will affect all
other recipes being parsed, hence the impact of the setting can have very far reaching consequences.

While for variables meant for a global scope (`.conf` files) normally set a baseline for all
recipes to operate in.
Changing those for just a single recipe will potentially create code and artifacts that do
not match the other recipes being build.

## Ways to fix it

- Remove the tagged variables from the file
- (opt) move the variable setting to the files the variables are deemed for
