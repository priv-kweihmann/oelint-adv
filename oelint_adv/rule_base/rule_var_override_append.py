from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash
from oelint_parser.constants import CONSTANTS

from oelint_adv.cls_rule import Rule


class VarOverrideAppend(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.overrideappend',
                         severity='warning',
                         message='This creates an empty scope which is then appended. It should be {op}:{_class} instead')
        self.pkgspecific = CONSTANTS.GetByPath(
            "oelint-variables-with-pkgn" or [])
        self.potpkgspecific = CONSTANTS.GetByPath(
            "oelint-variable-opt-with-pkgn" or [])

    def fix_override_append_order(self, item, op, scope):
        def replacer(v):
            return v.replace(
                item.VarNameComplete, item.VarName + ':' + op + ':' + scope,
            )

        item.Raw = replacer(item.Raw)
        item.RealRaw = replacer(item.RealRaw)

    def fix_pluseq_to_override(self, item, op_to_use, space):
        varname = item.VarName
        if item.VarName in (self.pkgspecific + self.potpkgspecific):
            varname += ':' + item.SubItems[0]

        def replacer(v):
            ret = v.replace(
                varname, varname + ':' + op_to_use,
            ).replace(
                item.VarOp, ' = ',
            )
            if op_to_use == 'append':
                opening_quote = ret.find(item.VarValue[0])
                if space and ret[opening_quote + 1] not in ' \t\n':
                    ret = ret[:opening_quote + 1] + \
                        space + ret[opening_quote + 1:]
            else:  # must be `else`, or coverage is unhappy about always true
                closing_quote = ret.rfind(item.VarValue[-1])
                if space and ret[closing_quote - 1] not in ' \t\n':
                    ret = ret[:closing_quote] + space + ret[closing_quote:]

            return ret

        item.Raw = replacer(item.Raw)
        item.RealRaw = replacer(item.RealRaw)

    def __getMatches(self, _file: str, stash: Stash):
        res = []
        pkgnames = stash.GetValidPackageNames(_file)

        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR)

        _store = set()

        for i in sorted(items, key=lambda key: key.Line):
            _items = [x for x in i.SubItems if x]
            if i.VarName in self.pkgspecific:
                _items = _items[1:]
            elif i.VarName in self.potpkgspecific:
                if _items and _items[0] in pkgnames:
                    _items = _items[1:]

            _scope = [x for x in _items if x not in ['append', 'prepend']]
            if not _scope:
                # Skip if there is no override
                continue

            _scope_key = i.VarName + ':' + '-'.join(_scope)
            if _scope_key in _store:
                # Skip if the override scope exists. This operation may be intentional
                continue

            extra_check = []
            extra_fixes = []
            _op = [x for x in _items if x in ['append', 'prepend']]
            if i.VarOp.strip() in ('+=', '.=', '=+', '=.') and not _op:
                # Case: A:foo += "b" -> A:append:foo = " b"
                op_to_use = 'prepend' if i.VarOp.strip()[
                    0] == '=' else 'append'
                space = ' ' if '+' in i.VarOp else ''

                extra_check = [op_to_use, ':'.join(_scope)]
                # to catch double errors
                extra_fixes.append(
                    [self.fix_override_append_order, op_to_use, ':'.join(_scope)])
                extra_fixes.append(
                    [self.fix_pluseq_to_override, op_to_use, space])
            elif _op and _items[0] not in _op:
                # Case: A:foo:append = " b" -> A:append:foo = " b"
                extra_check = [_op[0], ':'.join(_scope)]
                extra_fixes.append(
                    [self.fix_override_append_order, _op[0], ':'.join(_scope)])

            _store.add(_scope_key)
            if extra_check or extra_fixes:
                res.append((i, extra_check, extra_fixes))

        return res

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        for i, extra_check, _ in self.__getMatches(_file, stash):
            res += self.finding(
                i.Origin,
                i.InFileLine,
                override_msg=self.Msg.format(
                    op=extra_check[0],
                    _class=extra_check[1],
                ),
            )

        return res

    def fix(self, _file: str, stash: Stash) -> List[str]:
        res = []
        for i, _, extra_fixes in self.__getMatches(_file, stash):
            for fix in extra_fixes:
                fixer, *args = fix
                fixer(i, *args)
                res.append(_file)

        return res
