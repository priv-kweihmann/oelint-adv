from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarMultiLineIndent(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.multilineident',
                         severity='info',
                         message='On a multiline assignment, line indent is desirable. {a} set, {b} desirable')

    def __line_stats(self, i: Variable) -> List[Tuple[int, str]]:
        _map = []

        _lines = i.VarValueStripped.replace('\x1b"', '"').split('\x1b')
        non_empty_line_indent = 4
        first_line_has_content = False
        if _lines[0].strip():
            first_line_has_content = True
            non_empty_line_indent = i.Raw.index(_lines[0])

        for index, value in enumerate(_lines):
            if value.strip(' \x1b'):
                if first_line_has_content and index == 0:
                    _map.append((0, len(value) - len(value.lstrip()), value.lstrip()))
                else:
                    _map.append((non_empty_line_indent, len(value) - len(value.lstrip()),
                                " " * non_empty_line_indent + value.lstrip()))
            else:
                _map.append((0, 0, value.lstrip()))

        return _map

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER)
        for i in items:
            if not i.IsMultiLine():
                continue
            _indent_map = self.__line_stats(i)
            for index, _line in enumerate(_indent_map):
                expected, actual, _ = _line
                if expected != actual:
                    res += self.finding(i.Origin, i.InFileLine + index,
                                        self.format_message(a=actual, b=expected))
        return res

    def fix(self, _file: str, stash: Stash) -> List[str]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER)
        for i in items:
            if not i.IsMultiLine():
                continue
            _lines = i.VarValueStripped.split('\x1b')
            _indent_map = self.__line_stats(i)

            def _rreplace(in_: str, needle: str, repl: str) -> str:
                return in_[::-1].replace(needle[::-1], repl[::-1], 1)[::-1]

            fix_applied = False
            for index, value in enumerate(_lines):
                if value != _indent_map[index][2]:
                    fix_applied = True
                    # Note: we need to start replacing from the back of the string
                    # as otherwise a last line containing only whitespace
                    # will affect prior lines
                    i.VarValue = _rreplace(i.VarValue, value, _indent_map[index][2])
                    i.Raw = _rreplace(i.Raw, value, _indent_map[index][2])
                    i.RealRaw = _rreplace(i.RealRaw, value, _indent_map[index][2])
            if fix_applied:
                res.append(_file)
        return res
