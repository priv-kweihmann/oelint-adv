from typing import List, Tuple

from anytree import LoopError, Node
from oelint_parser.cls_item import TaskAdd
from oelint_parser.cls_stash import Stash
from oelint_parser.rpl_regex import RegexRpl

from oelint_adv.cls_rule import Rule


class TaskCustomOrder(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.task.customorder',
                         severity='error',
                         message='<FOO>')

    def __getNodeFromException(self, msg: str) -> List[str]:
        m = RegexRpl.match(r'^.*Node\(\'(?P<path>.*)\'\)\.$', msg)
        if m:
            return [x for x in m.group('path').split('/') if x]
        return []  # pragma: no cover

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items = stash.GetItemsFor(
            filename=_file, classifier=TaskAdd.CLASSIFIER)
        _nodes = []
        for item in items:
            for t in item.After:
                _n = None
                _m = None
                try:
                    _t = [y for y in _nodes if y.name == t]
                    if not any(_t):
                        _n = Node(t)
                        _nodes.append(_n)
                    else:
                        _n = _t[0]
                    _t = [y for y in _nodes if y.name == item.FuncName]
                    if not any(_t):
                        _m = Node(item.FuncName)
                        _nodes.append(_m)
                    else:
                        _m = _t[0]
                    if _m not in _n.children:  # pragma: no cover
                        _n.children += (_m,)
                except LoopError as e:
                    _path = self.__getNodeFromException(str(e)) + [t]
                    res += self.finding(item.Origin, item.InFileLine,
                                        'Assignment creates a cyclic dependency - Path={a}'.format(a='->'.join(_path)))
            for t in item.Before:
                try:
                    _n = None
                    _t = [y for y in _nodes if y.name == item.FuncName]
                    if not any(_t):
                        _n = Node(item.FuncName)  # pragma: no cover
                        _nodes.append(_n)  # pragma: no cover
                    else:
                        _n = _t[0]
                    _t = [y for y in _nodes if y.name == t]
                    _m = None
                    if not any(_t):
                        _m = Node(t)  # pragma: no cover
                        _nodes.append(_m)  # pragma: no cover
                    else:
                        _m = _t[0]
                    if _m not in _n.children:  # pragma: no cover
                        _n.children += (_m,)
                except LoopError as e:
                    _path = self.__getNodeFromException(str(e)) + [t]
                    res += self.finding(item.Origin, item.InFileLine,
                                        'Assignment creates a cyclic dependency - Path={a}'.format(a='->'.join(_path)))
        return res
