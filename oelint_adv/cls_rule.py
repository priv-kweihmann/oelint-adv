import importlib
import inspect
import os
import pkgutil
import sys

from colorama import Fore, Style

from oelint_adv.color import get_color
from oelint_adv.rule_file import get_rulefile, get_noinfo, get_nowarn


class Rule():
    def __init__(self, id="", severity="", message="", onappend=True, onlyappend=False, appendix=[]):
        """constructor

        Keyword Arguments:
            id {str} -- ID of the rule (default: {""})
            severity {str} -- severity of the rule (default: {""})
            message {str} -- Rule message (default: {""})
            onappend {bool} -- true if rule shoult be run on bbappends (default: {True})
            onlyappend {bool} -- true if rule applies to bbappends only (default: {False})
            appendix {list} -- possible appendix to id
        """
        self.ID = id
        self.Severity = severity
        self.Msg = message
        self.OnAppend = onappend
        self.OnlyAppend = onlyappend
        self.Appendix = appendix

    def check(self, _file, stash):
        """Stub for running check - is overridden by each rule

        Arguments:
            _file {str} -- File to be parsed
            stash {oelint_adv.cls_stash.Stash} -- Parsed stash

        Returns:
            list -- List of findings
        """
        return []

    def fix(self, _file, stash):
        """Stub for fix function - can be overridden by each rule

        Arguments:
            _file {str} -- File to be parsed
            stash {oelint_adv.cls_stash.Stash} -- Parsed stash

        Returns:
            list -- list of changed files
        """
        return []

    def finding(self, _file, _line, override_msg=None, appendix=None):
        """Called by rule to indicate a finding

        Arguments:
            _file {str} -- Full path to file or origin
            _line {int} -- Line number in file

        Keyword Arguments:
            override_msg {str} -- Optional string which overrides the set standard message (default: {None})
            appendix {str} -- Optional appendix to rule ID (default: {None})

        Returns:
            str -- Human readable finding (possibly with color codes)
        """
        if not self.OnAppend and _file.endswith(".bbappend"):
            return []
        if self.OnlyAppend and not _file.endswith(".bbappend"):
            return []
        if override_msg is None:
            override_msg = self.Msg
        _severity = self.Severity
        _rule_file = get_rulefile()
        _id = self.ID
        if appendix:
            _id += "." + appendix
        if _rule_file and self.ID in _rule_file:
            _severity = _rule_file[self.ID] or self.Severity
        if _severity == "info" and get_noinfo():
            return []
        if _severity == "warning" and get_nowarn():
            return []
        if _line <= 0:
            # Fix those issues, that don't come with a line
            _line = 1
        if get_color():
            if _severity == "error":
                return [(_line, "{}:{}{}:{}:{}:{}{}".format(os.path.abspath(_file), Fore.RED, _line, _severity, _id, override_msg, Style.RESET_ALL))]
            elif _severity == "warning":
                return [(_line, "{}:{}{}:{}:{}:{}{}".format(os.path.abspath(_file), Fore.YELLOW, _line, _severity, _id, override_msg, Style.RESET_ALL))]
            else:
                return [(_line, "{}:{}{}:{}:{}:{}{}".format(os.path.abspath(_file), Fore.GREEN, _line, _severity, _id, override_msg, Style.RESET_ALL))]
        return [(_line, "{}:{}:{}:{}:{}".format(os.path.abspath(_file), _line, _severity, _id, override_msg))]

    def __repr__(self):
        return "{}".format(self.ID)

    def GetIDs(self):
        """Returns all possible IDs of the rule

        Returns:
            list -- possible IDS of the rule
        """
        return [self.ID] + ["{}.{}".format(self.ID, x) for x in self.Appendix]

    def FormatMsg(self, *args):
        """Format message

        Returns:
            str -- formatted message
        """
        return self.Msg.format(*args)


def load_rules(args, add_rules=[], add_dirs=[]):
    """Load rules from set directories

    Keyword Arguments:
        add_rules {list} -- Additional builtin rulesets to be loaded (default: {[]})
        add_dirs {list} -- Additional directories to parse for rules (default: {[]})

    Returns:
        list -- Class instances of loaded rules
    """
    res = []
    _rule_file = get_rulefile()
    _path_list = {
        "base": {"path": "rule_base", "builtin": True}
    }
    for ar in add_rules:
        _path_list[ar] = {"path": "rule_{}".format(ar), "builtin": True}
    for ar in add_dirs:
        _path_list["additional_{}".format(os.path.basename(ar))] = {"path": ar, "builtin": False}
    for _, v in _path_list.items():
        if v["builtin"]:
            _searchpath = os.path.join(os.path.dirname(
                os.path.abspath(__file__)), v["path"])
        else:
            _searchpath = os.path.join(v["path"])
            sys.path.append(os.path.dirname(v["path"]))
        packages = pkgutil.walk_packages(path=[_searchpath])
        for _, name, _ in packages:
            if v["builtin"]:
                name = __name__.split(".")[0] + "." + v["path"] + "." + name
            else:
                name = os.path.basename(v["path"]) + "." + name
            try:
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
            except:
                if not args.quiet:
                    print("Can't load rule {}".format(name))
    return res
