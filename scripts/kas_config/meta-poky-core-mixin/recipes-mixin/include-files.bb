LICENSE = "CLOSED"

SRC_URI = "https://foo.bar/baz.tar.gz"
SRC_URI[sha256sum] = "1234567890"

include conf/distro/include/no-static-libs.inc
include conf/distro/include/yocto-uninative.inc
include conf/distro/include/security_flags.inc
include conf/distro/include/yocto-space-optimize.inc
