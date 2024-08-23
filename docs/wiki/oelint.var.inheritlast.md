# oelint.var.inheritlast

severity: warning

## Example

```
inherit native foo bar
```

## Why is this bad?

``native``, ``nativesdk`` and ``cross`` set some important variables to enable the proper build configuration.
To avoid having them overridden by later class code, those ``bbclass`` files should always be inherited last.

## Ways to fix it

```
inherit foo bar native
```
