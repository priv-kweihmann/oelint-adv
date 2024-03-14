# oelint.spaces.linecont

severity: error

## Example

```
A = "\<space>
 1 \
 2 \
"
```

## Why is this bad?

Space(s) after the line continuation character ``\`` should be avoided.
They do not add value and have been an illegal syntax in some versions of bitbake.

## Ways to fix it

Remove all spaces after the line continuation character ``\``

```
A = "\
 1 \
 2 \
"
```
