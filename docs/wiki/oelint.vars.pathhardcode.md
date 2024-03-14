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

- ``${systemd_user_unitdir}`` => ``/usr/lib/systemd/user``
- ``${systemd_system_unitdir}`` => ``/lib/systemd/system``
- ``${docdir}`` => ``/usr/share/doc``
- ``${infodir}`` => ``/usr/share/info``
- ``${mandir}`` => ``/usr/share/man``
- ``${libexecdir}`` => ``/usr/libexec``
- ``${systemd_unitdir}`` => ``/lib/systemd``
- ``${libdir}`` => ``/usr/lib``
- ``${bindir}`` => ``/usr/bin``
- ``${datadir}`` => ``/usr/share``
- ``${includedir}`` => ``/usr/include``
- ``${localstatedir}`` => ``/var``
- ``${nonarch_base_libdir}`` => ``/lib``
- ``${sbindir}`` => ``/usr/sbin``
- ``${servicedir}`` => ``/srv``
- ``${sharedstatedir}`` => ``/com``
- ``${sysconfdir}`` => ``/etc``

```
FILES:${PN} += "${docdir}"
```
