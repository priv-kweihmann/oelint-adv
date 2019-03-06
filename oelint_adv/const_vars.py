
MANDATORY_VARS = [
    "SUMMARY",
    "DESCRIPTION",
    "AUTHOR",
    "HOMEPAGE",
    "SECTION",
    "LICENSE",
    "SRC_URI"
]

SUGGESTED_VARS = [
    "BUGTRACKER",
    "BBCLASSEXTEND"
]

VAR_ORDER = [
    "SUMMARY",
    "DESCRIPTION",
    "AUTHOR",
    "HOMEPAGE",
    "BUGTRACKER",
    "SECTION",
    "LICENSE",
    "LIC_FILES_CHKSUM",
    "DEPENDS",
    "PROVIDES",
    "PV",
    "SRC_URI",
    "SRCREV",
    "S",
    "inherit",
    "PACKAGECONFIG",
    "EXTRA_QMAKEVARS_POST",
    "EXTRA_OECONF",
    "PACKAGE_ARCH",
    "PACKAGES",
    "FILES_${PN}",
    "RDEPENDS_${PN}",
    "RRECOMMENDS_${PN}",
    "RSUGGESTS_${PN}",
    "RPROVIDES_${PN}",
    "RCONFLICTS_${PN}",
    "BBCLASSEXTEND"
]