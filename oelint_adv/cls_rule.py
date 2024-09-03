import importlib
import inspect
import os
import pkgutil
import sys
from typing import FrozenSet, Iterable, List, Tuple

from colorama import Style
from oelint_parser.cls_stash import Stash

from oelint_adv.state import State
from oelint_adv.version import __version__


class Rule:
    def __init__(self,
                 id: str = '',  # noqa: A002, VNE003
                 severity: str = '',
                 message: str = '',
                 onappend: bool = True,
                 onlyappend: bool = False,
                 appendix: List[str] = (),
                 valid_till_release: str = '',
                 valid_from_release: str = '',
                 ) -> None:  # noqa: A002, VNE003
        """constructor

        Keyword Arguments:
            id {str} -- ID of the rule (default: {''})
            severity {str} -- severity of the rule (default: {''})
            message {str} -- Rule message (default: {''})
            onappend {bool} -- true if rule should be run on bbappends (default: {True})
            onlyappend {bool} -- true if rule applies to bbappends only (default: {False})
            appendix {List[str]} -- possible appendix to id
            valid_till_release {str} -- rule only valid till (excluding) this release (default: '' = all)
            valid_from_release {str} -- rule only valid from (including) this release (default: '' = all)
        """
        self.ID = id
        self.Severity = severity
        self.Msg = message
        self.OnAppend = onappend
        self.OnlyAppend = onlyappend
        self.Appendix = appendix
        self._valid_till_release = valid_till_release
        self._valid_from_release = valid_from_release
        self._state: State = None
        self.__matrix: FrozenSet[str] = []

    def set_product_matrix(self, in_: FrozenSet[str]) -> None:
        """Set the product matrix

        Args:
            in_ (frozenset[str]): Product matrix of ids
        """
        self.__matrix = in_

    def set_state(self, state_: State) -> None:
        """Set the state object

        Args:
            state_ (State): Current state object
        """
        self._state = state_

    def check_release_range(self, release_range: List[str]) -> bool:
        """Check if rule is applicable with currently configured release(s)

        Args:
            release_range (List[str]): Range of supported releases (as passed by tweaks)

        Returns:
            bool: Rule is applicable with release range
        """
        if self._valid_from_release and self._valid_from_release not in release_range:
            return False
        if self._valid_till_release and self._valid_till_release in release_range:
            return False
        return True

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        """Stub for running check - is overridden by each rule

        Arguments:
            _file {str} -- File to be parsed
            stash {oelint_adv.cls_stash.Stash} -- Parsed stash

        Returns:
            list -- List of findings
        """
        return []  # pragma: no cover

    def fix(self, _file: str, stash: Stash) -> List[str]:
        """Stub for fix function - can be overridden by each rule

        Arguments:
            _file {str} -- File to be parsed
            stash {oelint_adv.cls_stash.Stash} -- Parsed stash

        Returns:
            list -- list of changed files
        """
        return []

    def finding(self,
                _file: str,
                _line: int,
                override_msg: str = None,
                appendix: str = None,
                blockoffset: int = 0,
                severity_override: str = '') -> Tuple[Tuple[str, int], List[str], str]:
        """Called by rule to indicate a finding

        Arguments:
            _file {str} -- Full path to file or origin
            _line {int} -- Line number in file

        Keyword Arguments:
            override_msg {str} -- Optional string which overrides the set standard message (default: {None})
            appendix {str} -- Optional appendix to rule ID (default: {None})
            blockoffset {int} -- line number to look for inline suppressions instead of _line (default: 0 == use _line)
            severity_override {str} -- override the base severity (empty == use base)

        Returns:
            Tuple[Tuple[str, int], List[str], str] -- Path, line, matrix, Human readable finding (possibly with color codes)
        """
        if not self.OnAppend and _file.endswith('.bbappend'):
            return []  # pragma: no cover
        if self.OnlyAppend and not _file.endswith('.bbappend'):
            return []  # pragma: no cover
        if override_msg is None:
            override_msg = self.Msg
        _suppression_offset = blockoffset or _line
        _id = [self.ID]
        _display_id = self.ID
        if appendix:
            _id.append(self.ID + '.' + appendix)
            _display_id += '.' + appendix
        # filter out suppressions
        if any(x in self._state.get_suppressions() for x in _id):
            return []
        _severity = severity_override or self.get_severity(appendix)

        if self._state.get_hide(_severity):
            return []

        if _line <= 0:
            # Fix those issues, that don't come with a line
            _line = 1

        # filter out inline suppressions
        if any(x for x in _id if x in self._state.get_inlinesuppressions().get(_file, {}).get(max(1, _suppression_offset - 1), [])):
            self._state.set_inline_suppression_seen(_file, _suppression_offset - 1, _id)
            return []

        _path = os.path.abspath(_file)
        if self._state.get_relpaths():
            _path = os.path.relpath(_path, os.getcwd())

        _style = ''
        _color = ''
        if self._state.get_colorize():
            _color = self._state.get_color_by_severity(_severity)
            _style = Style.RESET_ALL

        wikiurl = f'https://github.com/priv-kweihmann/oelint-adv/blob/{__version__}/docs/wiki/{self.ID}.md'

        _msg = self._state.get_messageformat().format(path=_path, line=_line, severity=_severity,
                                                      id=_display_id, msg=override_msg,
                                                      wikiurl=wikiurl)
        return [((_path, _line), self.__matrix, f'{_color}{_msg}{_style}')]

    def __repr__(self) -> str:
        return '{id}'.format(id=self.ID)  # pragma: no cover

    def get_severity(self, appendix: str = None) -> str:
        """Get the configured severity for this rule, if it is enabled.

        Keyword Arguments:
            appendix {str} -- Potential subrule name (default: {None})

        Returns:
            str -- Severity for this rule if it is enabled, {None} if disabled.
        """
        _rule_file = self._state.get_rulefile()
        if not _rule_file:
            return self.Severity
        _subid = None if appendix is None else f'{self.ID}.{appendix}'
        if _subid and _subid in _rule_file:
            _severity = _rule_file[_subid]
        elif self.ID in _rule_file:
            _severity = _rule_file[self.ID]
        else:
            # rule not in rulefile
            return None
        return _severity if _severity != '' else self.Severity

    def get_ids(self) -> List[str]:
        """Returns all possible IDs of the rule

        Returns:
            list -- possible IDS of the rule
        """
        return [self.ID] + ['{id}.{app}'.format(id=self.ID, app=x) for x in self.Appendix]

    def get_rulefile_entries(self) -> dict:
        """Returns a dictionary of entries which would represent the currently
        enabled ruleset (for this rule) in a rulefile.

        Returns:
            dict -- list of rulefile entries
        """
        return {
            **({} if (self.get_severity() is None or self.ID in self._state.get_suppressions()) else {self.ID: self.get_severity()}),
            **{f'{self.ID}.{x}': self.get_severity(x) for x in self.Appendix if (self.get_severity(x) is not None and self.ID not in self._state.get_suppressions())},
        }

    def format_message(self, *args, **kwargs) -> str:
        """Format message

        Returns:
            str -- formatted message
        """
        return self.Msg.format(*args, **kwargs)

    @staticmethod
    def is_lone_append(stash: Stash, file: str) -> bool:
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
        return file in stash.GetLoneAppends()


def load_rules(args, add_rules: Iterable[str] = (), add_dirs: Iterable[str] = ()) -> List['Rule']:
    """Load rules from set directories

    Keyword Arguments:
        add_rules {tuple} -- Additional builtin rulesets to be loaded (default: {[]})
        add_dirs {tuple} -- Additional directories to parse for rules (default: {[]})

    Returns:
        list -- Class instances of loaded rules
    """
    res = []
    _rule_file = args.state.get_rulefile()
    _path_list = {
        'base': {'path': 'rule_base', 'builtin': True},
    }
    for ar in add_rules:
        _path_list[ar] = {'path': 'rule_{a}'.format(a=ar), 'builtin': True}
    for ar in add_dirs:
        _path_list['additional_{a}'.format(a=os.path.basename(ar))] = {
            'path': ar, 'builtin': False}  # pragma: no cover
    for _, v in _path_list.items():
        if v['builtin']:
            _searchpath = os.path.join(os.path.dirname(
                os.path.abspath(__file__)), v['path'])
        else:
            _searchpath = os.path.join(v['path'])  # pragma: no cover
            sys.path.append(os.path.dirname(v['path']))  # pragma: no cover
        packages = pkgutil.walk_packages(path=[_searchpath])
        for _, name, _ in packages:
            if v['builtin']:
                name = __name__.split('.')[0] + '.' + v['path'] + '.' + name
            else:
                name = os.path.basename(v['path']) + '.' + name  # pragma: no cover
            try:
                mod = importlib.import_module(name)
                for m in inspect.getmembers(mod, inspect.isclass):
                    try:
                        if issubclass(m[1], Rule):
                            inst = m[1]()
                            if not inst.check_release_range(args._release_range):
                                continue
                            inst._state = args.state
                            _potential_ids = [
                                inst.ID] + ['{a}.{b}'.format(a=inst.ID, b=x) for x in inst.Appendix]
                            if any(_potential_ids):
                                if _rule_file and not any(x in _rule_file for x in _potential_ids):
                                    continue  # pragma: no cover
                                res.append(inst)
                    except Exception:  # pragma: no cover, # noqa: S110
                        pass  # pragma: no cover
            except Exception as e:  # pragma: no cover
                if not args.quiet:  # pragma: no cover
                    print(  # noqa: T201 this print is fine here
                        'Can\'t load rule {rule} -> {exp}'.format(rule=name, exp=e))  # pragma: no cover
    return res
