_RULE_FILE = {}
_CONST_FILE = {}


def get_rulefile():
    return _RULE_FILE


def get_constantfile():
    return _CONST_FILE


def set_rulefile(value):
    global _RULE_FILE
    _RULE_FILE = value


def set_constantfile(value):
    global _CONST_FILE
    _CONST_FILE = value
