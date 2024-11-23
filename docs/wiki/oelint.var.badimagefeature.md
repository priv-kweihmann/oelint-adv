# oelint.var.badimagefeature

severity: warning

## Example

```
EXTRA_IMAGE_FEATURES:append = " empty-root-password"
```

## Why is this bad?

Various settings in ``EXTRA_IMAGE_FEATURES`` and ``IMAGE_FEATURES`` either
bloat the image or are a security risk.

The following items are considered bad

- allow-empty-password
- allow-root-login
- dbg-pkgs
- debug-tweaks
- dev-pkgs
- eclipse-debug
- empty-root-password
- post-install-logging
- ptest-pkgs
- serial-autologin-root
- staticdev-pkgs
- tools-debug

None of them should be used in production.

## Ways to fix it

- Remove the setting from ``EXTRA_IMAGE_FEATURES`` and ``IMAGE_FEATURES``
- use ``nooelint: oelint.var.badimagefeature.<id>`` when you are sure that
  none of the image(s) resulting out of this setting can be used in production
