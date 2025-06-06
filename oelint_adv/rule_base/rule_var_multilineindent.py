from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarMultiLineIndent(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.multilineident',
                         severity='info',
                         message='On a multiline assignment, line indent is desirable. {a} set, {b} desirable')

    def __line_stats(self, i: Variable) -> Tuple[int, int, List[Tuple[int, int, str]]]:
        _map = []

        _lines = i.VarValueStripped.replace('\x1b"', '"').split('\x1b')
        non_empty_line_indent = 4
        first_line_has_content = False
        last_line_indent = 0
        if _lines[0].strip():
            first_line_has_content = True
            non_empty_line_indent = i.Raw.index(_lines[0])
            last_line_indent = non_empty_line_indent

        for index, value in enumerate(_lines):
            if value.strip(' \x1b'):
                if first_line_has_content and index == 0:
                    _map.append((0, len(value) - len(value.lstrip()), value.lstrip()))
                else:
                    _map.append((non_empty_line_indent, len(value) - len(value.lstrip()),
                                " " * non_empty_line_indent + value.lstrip()))
            else:
                _map.append((0, 0, value.lstrip()))

        return (last_line_indent, non_empty_line_indent, _map)

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER)
        for i in items:
            if not i.IsMultiLine():
                continue
            _, _, _indent_map = self.__line_stats(i)
            for index, _line in enumerate(_indent_map):
                expected, actual, _ = _line
                if expected != actual:
                    res += self.finding(i.Origin, i.InFileLine + index,
                                        self.format_message(a=actual, b=expected), blockoffset=i.InFileLine)
        return res

    def fix(self, _file: str, stash: Stash) -> List[str]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER)
        for i in items:
            if not i.IsMultiLine():
                continue
            _lines = i.VarValueStripped.split('\x1b')
            _last_line_indent, _standard_indent, _indent_map = self.__line_stats(i)

            def _rreplace(in_: str, needle: str, repl: str) -> str:
                return in_[::-1].replace(needle[::-1], repl[::-1], 1)[::-1]

            fix_applied = False
            for index, value in enumerate(_lines):
                if value != _indent_map[index][2]:
                    if not value.strip():
                        continue
                    replacement = _indent_map[index][2]
                    fix_applied = True
                    # Note: we need to start replacing from the back of the string
                    # as otherwise a last line containing only whitespace
                    # will affect prior lines
                    i.VarValue = _rreplace(i.VarValue, value, replacement)
                    i.Raw = _rreplace(i.Raw, value, replacement)
                    i.RealRaw = _rreplace(i.RealRaw, value, replacement)

            _last_line = i.VarValue.split('\x1b')[-1]
            _last_line_stripped = _last_line.strip()
            if len(_last_line_stripped) > 1:
                _last_line_expected = f'{" " * _standard_indent + _last_line_stripped}'
            else:
                _last_line_expected = f'{" " * _last_line_indent + _last_line_stripped}'

            if _last_line != _last_line_expected:
                if _last_line.strip('"\''):
                    i.VarValue = _rreplace(i.VarValue, _last_line, _last_line_expected)
                    i.Raw = _rreplace(i.Raw, _last_line, _last_line_expected)
                    i.RealRaw = _rreplace(i.RealRaw, _last_line, _last_line_expected)
                    fix_applied = True

            if fix_applied:
                res.append(_file)

        return res
