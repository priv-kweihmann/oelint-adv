# oelint.vars.downloadfilename

severity: warning

## Example

In ``my-recipe_1.0.bb``

```
SRC_URI += "http://foo.bar/baz.jpg"
```

## Why is this bad?

As the download directory is shared across all builds all artifacts need to be properly versioned.
This makes sure that updates and rebuilds are detected.

One example is that with version ``1.0`` of the recipe we would download ``baz.jpg`` with a checksum A.
Now we do an upgrade to version ``1.1`` of the recipe leading to checksum B.

If we now would try to go back to version ``1.0`` the artifact in the download directory would have been
overwritten to version ``1.1``, causing a checksum error while building ``1.0`` again.

## Ways to fix it

Add a ``downloadfilename`` including ``PV`` or the hardcoded recipe version

```
SRC_URI += "http://foo.bar/baz.jpg;downloadfilename=something.dat.${PV}"
```
