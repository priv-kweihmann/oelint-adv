# oelint.vars.srcurioptions

severity: warning

## Example

```
SRC_URI += "svn://foo;proto=http"
```

## Why is this bad?

Each fetcher type has only a limited set of known parameters.
Using an unknown one will either cause fetching errors or making the parameter ignored entirely.

## Ways to fix it

Use only known fetcher parameters

```
SRC_URI += "svn://foo;protocol=http"
```
