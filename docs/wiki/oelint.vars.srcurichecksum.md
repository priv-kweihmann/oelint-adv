# oelint.vars.srcurichecksum

severity: error

## Example

In any bitbake file

```
SRC_URI += "ftp://foo;name=f3"
```

or

```
SRC_URI += "ftp://foo"
```

## Why is this bad?

For any blob fetcher like ``http``, ``https``, ``ftp``, ``ftps``, ``sftp``, ``s3`` or ``az``.
a (named) checksum is required.

## Ways to fix it

```
SRC_URI += "ftp://foo;name=f3"
SRC_URI[f3.sha256sum] = "4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865"
```

or

```
SRC_URI += "ftp://foo"
SRC_URI[sha256sum] = "4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865"
```
