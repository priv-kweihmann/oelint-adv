# oelint.vars.inappclassoverride

severity: warning

## Example

```
A:class-nativesdk = "1"
```

or

```
A:class-native = "1"
```

## Why is this bad?

For the class specific settings to be applicable either
`BBCLASSEXTEND` needs to be set accordingly or the
specific class needs to be inherited

## Ways to fix it

```
A:class-nativesdk = "1"
```

can be fixed as

```
A:class-nativesdk = "1"
BBCLASSEXTEND = "nativesdk"
```

or

```
A:class-nativesdk = "1"
inherit nativesdk
```
