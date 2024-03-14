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
See [OpenEmbedded contribution guide](https://www.openembedded.org/index.php?title=Commit_Patch_Message_Guidelines&oldid=10935)

## Ways to fix it

Add to the patch file

```
Upstream-Status: reason
```
