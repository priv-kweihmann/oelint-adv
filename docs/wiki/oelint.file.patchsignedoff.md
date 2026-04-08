# oelint.file.inappropriatemsg

severity: info

## Example

With `my.patch`

```
Signed-off-by: some body <some@body.com>
```

is missing

## Why is this bad?

Every upstreamable patch should have a ``Signed-off-by`` line.
See [Yocto Upstream-Status guide](https://docs.yoctoproject.org/contributor-guide/recipe-style-guide.html#patch-upstream-status)

## Ways to fix it

Add to the patch file

```
Signed-off-by: some body <some@body.com>
```
