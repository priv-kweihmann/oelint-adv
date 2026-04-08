# oelint.file.upstreamstatus

severity: info

## Example

With `my.patch`

```
Upstream-Status: reason
```

is missing or not classified properly

## Why is this bad?

Every patch should have a ``Upstream-Status`` line.
See [Yocto Upstream-Status guide](https://docs.yoctoproject.org/contributor-guide/recipe-style-guide.html#patch-upstream-status)

## Ways to fix it

Add to the patch file

```
Upstream-Status: reason
```
