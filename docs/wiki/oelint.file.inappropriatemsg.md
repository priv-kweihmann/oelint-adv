# oelint.file.inappropriatemsg

severity: info

## Example

With `my.patch`

```
Upstream-Status: Inappropriate [me don't care]
```

or

```
Upstream-Status: Inappropriate
```

or

```
Upstream-Status: Inappropriate (configuration)
```

## Why is this bad?

``Inappropriate`` will create technical debt, as the will never be merged upstream,
so labelling why this patch is needed is essential for tracking.
See [OpenEmbedded contribution guide](https://www.openembedded.org/index.php?title=Commit_Patch_Message_Guidelines&oldid=10935)

## Ways to fix it

```
Inappropriate [licensing]
```

or any other reason in the square brackets from the following list

- oe-specific
- OE specific
- oe-core specific
- not author
- native
- configuration
- enable feature
- disable feature
- bugfix .*
- embedded specific
- no upstream
- other
