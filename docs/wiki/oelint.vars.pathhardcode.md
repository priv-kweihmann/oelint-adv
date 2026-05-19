# oelint.vars.pathhardcode

severity: warning

## Example

```
FILES:${PN} += "/usr/share/doc"
```

## Why is this bad?

Bitbake uses variables for certain paths, to enable features like ``usrmerge`` or ``multilib``.
So the variables could change depending if those features (along others) are used or not.
Using hardcoded paths could result in packaging files wrongly or installing files into the
wrong paths.

## Ways to fix it

The following variables are known

- ``${bindir}`` => ``/usr/bin``
- ``${datadir}`` => ``/usr/share``
- ``${docdir}`` => ``/usr/share/doc``
- ``${firmwaredir}`` => ``/lib/firmware`` *1
- ``${includedir}`` => ``/usr/include``
- ``${infodir}`` => ``/usr/share/info``
- ``${libdir}`` => ``/usr/lib``
- ``${libexecdir}`` => ``/usr/libexec``
- ``${localstatedir}`` => ``/var``
- ``${mandir}`` => ``/usr/share/man``
- ``${nonarch_base_libdir}`` => ``/lib``
- ``${sbindir}`` => ``/usr/sbin``
- ``${servicedir}`` => ``/srv``
- ``${sharedstatedir}`` => ``/com``
- ``${sysconfdir}`` => ``/etc``
- ``${systemd_system_unitdir}`` => ``/lib/systemd/system``
- ``${systemd_unitdir}`` => ``/lib/systemd``
- ``${systemd_user_unitdir}`` => ``/usr/lib/systemd/user``

* 1 - starting from `wrynose` release

```
FILES:${PN} += "${docdir}"
```
