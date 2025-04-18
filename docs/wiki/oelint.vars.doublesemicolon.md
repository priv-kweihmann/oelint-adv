# oelint.vars.doublesemicolon

severity: info

## Example

```
LIC_FILES_CHKSUM = "file://foo;md5sum=abcdef12355;;wsw=1;;;;;a=1"
```

or

```
SRC_URI = "file://foo;branch=main;;wsw=1;;;;;a=1"
```

## Why is this bad?

The `;;` settings are pointless and can be removed

The variables checked for containing `;;` can be configured through the constant `oelint-semicolon-vars` (list of string)

## Ways to fix it

Replace `;;` by `;`
