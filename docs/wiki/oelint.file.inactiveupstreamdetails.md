# oelint.file.inactiveupstreamdetails

severity: info

## Example

With `my.patch`

```
Upstream-Status: Inactive-Upstream
```

or 

```
Upstream-Status: Inactive-Upstream [1234]
```

## Why is this bad?

``Inactive-Upstream`` shall name a timestamp when the last activity was seen upstream,
see former [OpenEmbedded contribution guide](https://www.openembedded.org/index.php?title=Commit_Patch_Message_Guidelines&oldid=10935)

## Ways to fix it

```
Inactive-Upstream [lastcommit: 11.11.2011]
```

or

```
Inactive-Upstream [lastrelease: 11.11.2011]
```

or even

```
Inactive-Upstream [lastcommit: 11.11.2011, lastrelease: 11.11.2011]
```
