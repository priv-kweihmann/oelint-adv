from oelint_parser.const_vars import set_constantfile as parser_set_constantfile
from oelint_parser.const_vars import set_rulefile as parser_set_rulefile

_RULE_FILE = {}
_CONST_FILE = {}
_NOINFO = False
_NOWARN = False

def get_noinfo():
    return _NOINFO

def get_nowarn():
    return _NOWARN

def set_noinfo(value):
    global _NOINFO
    _NOINFO = value

def set_nowarn(value):
    global _NOWARN
    _NOWARN = value

def get_rulefile():
    return _RULE_FILE


def get_constantfile():
    return _CONST_FILE


def set_rulefile(value):
    global _RULE_FILE
    _RULE_FILE = value
    parser_set_rulefile(_RULE_FILE)


def set_constantfile(value):
    global _CONST_FILE
    _CONST_FILE = value
    parser_set_constantfile(_CONST_FILE)
