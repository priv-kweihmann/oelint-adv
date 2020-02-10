import importlib
import inspect
import os
import pkgutil

from colorama import Fore, Style

from oelint_adv.color import get_color
from oelint_adv.rule_file import get_rulefile


class Rule():
    def __init__(self, id="", severity="", message=""):
        self.ID = id
        self.Severity = severity
        self.Msg = message

    def check(self, _file, stash):
        return []

    def fix(self, _file, stash):
        return []

    def finding(self, _file, _line, override_msg=None):
        if override_msg is None:
            override_msg=self.Msg
        _severity = self.Severity
        _rule_file = get_rulefile()
        if _rule_file and self.ID in _rule_file:
            _severity = _rule_file[self.ID] or self.Severity
        if get_color():
            if _severity == "error":
                return ["{}:{}{}:{}:{}:{}{}".format(os.path.abspath(_file), Fore.RED, _line, _severity, self.ID, override_msg, Style.RESET_ALL)]
            elif _severity == "warning":
                return ["{}:{}{}:{}:{}:{}{}".format(os.path.abspath(_file), Fore.YELLOW, _line, _severity, self.ID, override_msg, Style.RESET_ALL)]
            else:
                return ["{}:{}{}:{}:{}:{}{}".format(os.path.abspath(_file), Fore.GREEN, _line, _severity, self.ID, override_msg, Style.RESET_ALL)]
        return ["{}:{}:{}:{}:{}".format(os.path.abspath(_file), _line, _severity, self.ID, override_msg)]

    def __repr__(self):
        return "{}".format(self.ID)

    def FormatMsg(self, *args):
        return self.Msg.format(*args)


def load_rules(add_rules=[]):
    res = []
    _rule_file = get_rulefile()
    _path_list = {
        "base": {"path": "rule_base"}
    }
    for ar in add_rules:
        _path_list[ar] = {"path": "rule_{}".format(ar)}
    for _, v in _path_list.items():
        _searchpath = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), v["path"])
        packages = pkgutil.walk_packages(path=[_searchpath])
        for _, name, _ in packages:
            name = __name__.split(".")[0] + "." + v["path"] + "." + name
            mod = importlib.import_module(name)
            for m in inspect.getmembers(mod, inspect.isclass):
                try:
                    if issubclass(m[1], Rule):
                        inst = m[1]()
                        if inst.ID:
                            if _rule_file and inst.ID not in _rule_file:
                                continue
                            res.append(inst)
                except Exception:
                    pass
    return res
