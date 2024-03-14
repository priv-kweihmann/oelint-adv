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
See [OpenEmbedded contribution guide](https://www.openembedded.org/index.php?title=Commit_Patch_Message_Guidelines&oldid=10935)

## Ways to fix it

Add to the patch file

```
Signed-off-by: some body <some@body.com>
```
