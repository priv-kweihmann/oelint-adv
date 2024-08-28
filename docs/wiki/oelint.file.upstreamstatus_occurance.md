# oelint.file.upstreamstatus_occurance

severity: inactive

**Note**: this rule is not used by default and needs to be activated through a rule file first

## Example

```
Upstream-Status: Pending
```

in a patch file

## Why is this bad?

This is bad as e.g. ``Pending`` patches, are piling up technical debt.

## Ways to fix it

- submit the code if applicable and change the ``Upstream-Status``
- set to ``Inappropriate`` if the patch can't be upstreamed
