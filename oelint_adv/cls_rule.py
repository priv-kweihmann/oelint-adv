import importlib
import inspect
import os
import pkgutil
import sys

from colorama import Fore, Style

from oelint_adv.color import get_color
from oelint_adv.rule_file import get_rulefile, get_noinfo, get_nowarn, get_suppressions


class Rule():
    def __init__(self, id="", severity="", message="", onappend=True, onlyappend=False, appendix=[]):
        """constructor

        Keyword Arguments:
            id {str} -- ID of the rule (default: {""})
            severity {str} -- severity of the rule (default: {""})
            message {str} -- Rule message (default: {""})
            onappend {bool} -- true if rule should be run on bbappends (default: {True})
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
        return [] # pragma: no cover

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
            return [] # pragma: no cover
        if self.OnlyAppend and not _file.endswith(".bbappend"):
            return [] # pragma: no cover
        if override_msg is None:
            override_msg = self.Msg
        _id = [self.ID]
        _displayId = self.ID
        if appendix:
            _id.append(self.ID + "." + appendix)
            _displayId += "." + appendix
        # filter out suppressions
        if any(x in get_suppressions() for x in _id):
            return []
        _severity = self.GetSeverity(appendix)
        if _severity is None:
            # the rule is disabled
            return []
        if _severity == "info" and get_noinfo():
            return []
        if _severity == "warning" and get_nowarn():
            return []
        if _line <= 0:
            # Fix those issues, that don't come with a line
            _line = 1
        if get_color():
            if _severity == "error":
                return [(_line, "{}:{}{}:{}:{}:{}{}".format(os.path.abspath(_file), Fore.RED, _line, _severity, _displayId, override_msg, Style.RESET_ALL))]
            elif _severity == "warning":
                return [(_line, "{}:{}{}:{}:{}:{}{}".format(os.path.abspath(_file), Fore.YELLOW, _line, _severity, _displayId, override_msg, Style.RESET_ALL))]
            else:
                return [(_line, "{}:{}{}:{}:{}:{}{}".format(os.path.abspath(_file), Fore.GREEN, _line, _severity, _displayId, override_msg, Style.RESET_ALL))]
        return [(_line, "{}:{}:{}:{}:{}".format(os.path.abspath(_file), _line, _severity, _displayId, override_msg))]

    def __repr__(self):
        return "{}".format(self.ID) # pragma: no cover

    def GetSeverity(self, appendix=None):
        """Get the configured severity for this rule, if it is enabled.

        Keyword Arguments:
            appendix {str} -- Potential subrule name (default: {None})

        Returns:
            str -- Severity for this rule if it is enabled, {None} if disabled.
        """
        _rule_file = get_rulefile()
        if not _rule_file:
            return self.Severity
        _subid = None if appendix is None else f"{self.ID}.{appendix}"
        if _subid and _subid in _rule_file:
            _severity = _rule_file[_subid]
        elif self.ID in _rule_file:
            _severity = _rule_file[self.ID]
        else:
            # rule not in rulefile
            return None
        return _severity if _severity != "" else self.Severity

    def GetIDs(self):
        """Returns all possible IDs of the rule

        Returns:
            list -- possible IDS of the rule
        """
        return [self.ID] + ["{}.{}".format(self.ID, x) for x in self.Appendix]

    def GetRulefileEntries(self):
        """Returns a dictionary of entries which would represent the currently
        enabled ruleset (for this rule) in a rulefile.

        Returns:
            dict -- list of rulefile entries
        """
        return {
            **({} if self.GetSeverity() is None else {self.ID: self.GetSeverity()}),
            **{f"{self.ID}.{x}": self.GetSeverity(x) for x in self.Appendix if self.GetSeverity(x) is not None},
        }

    def FormatMsg(self, *args):
        """Format message

        Returns:
            str -- formatted message
        """
        return self.Msg.format(*args)

    def IsLoneAppend(self, stash, file):
        """Check if the file is a bbappend file without any matching
           bb file

        Args:
            stash {oelint_parser.cls_stash.Stash} -- Parsed stash
            file {str} -- Path to file

        Returns:
            bool: True if bbappend has no matches in stash
        """
        if not file.endswith('.bbappend'):
            return False
        for item in stash.GetItemsFor(filename=file):
            if any(x.endswith('.bb') for x in item.Links):
                return False
        return True


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
        _path_list["additional_{}".format(os.path.basename(ar))] = {"path": ar, "builtin": False} # pragma: no cover
    for _, v in _path_list.items():
        if v["builtin"]:
            _searchpath = os.path.join(os.path.dirname(
                os.path.abspath(__file__)), v["path"])
        else:
            _searchpath = os.path.join(v["path"]) # pragma: no cover
            sys.path.append(os.path.dirname(v["path"])) # pragma: no cover
        packages = pkgutil.walk_packages(path=[_searchpath])
        for _, name, _ in packages:
            if v["builtin"]:
                name = __name__.split(".")[0] + "." + v["path"] + "." + name
            else:
                name = os.path.basename(v["path"]) + "." + name # pragma: no cover
            try:
                mod = importlib.import_module(name)
                for m in inspect.getmembers(mod, inspect.isclass):
                    try:
                        if issubclass(m[1], Rule):
                            inst = m[1]()
                            _potentialIds = [inst.ID] + ["{}.{}".format(inst.ID, x) for x in inst.Appendix]
                            if any(_potentialIds):
                                if _rule_file and not any(x in _rule_file for x in _potentialIds):
                                    continue # pragma: no cover
                                res.append(inst)
                    except Exception: # pragma: no cover
                        pass # pragma: no cover
            except Exception as e: # pragma: no cover
                if not args.quiet: # pragma: no cover
                    print("Can't load rule {} -> {}".format(name, e)) # pragma: no cover
    return res
