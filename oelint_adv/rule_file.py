from oelint_parser.constants import CONSTANTS

_NOINFO = False
_NOWARN = False
_RELPATH = False
_MESSAGEFORMAT = ''
_RULE_FILE = {}
_SUPPRESSIONS = []


def get_noinfo():
    return _NOINFO


def get_nowarn():
    return _NOWARN


def get_relpaths():
    return _RELPATH


def get_messageformat():
    return _MESSAGEFORMAT


def set_noinfo(value):
    global _NOINFO
    _NOINFO = value


def set_relpaths(value):
    global _RELPATH
    _RELPATH = value


def set_messageformat(value):
    global _MESSAGEFORMAT
    _MESSAGEFORMAT = value


def set_nowarn(value):
    global _NOWARN
    _NOWARN = value


def set_suppressions(value):
    global _SUPPRESSIONS
    _SUPPRESSIONS = value


def get_suppressions():
    return _SUPPRESSIONS


def get_rulefile():
    return _RULE_FILE


def set_rulefile(value):
    global _RULE_FILE
    _RULE_FILE = value
    CONSTANTS.AddFromRuleFile(value)
