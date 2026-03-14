from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule
from oelint_adv.rule_base.rule_var_override_append import VarOverrideAppend


class VarModifyOverride(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.modifyoverride',
                         severity='warning',
                         message='This modifies an override, not {op}s conditionally. Use `:{op}` or ` = `')
        self.pkgspecific = VarOverrideAppend().pkgspecific

    def __getMatches(self, _file: str, stash: Stash) -> Tuple[List[Variable], str]:
        res = []

        for i in stash.GetItemsFor(
            filename=_file,
            classifier=Variable.CLASSIFIER,
            attribute=Variable.ATTR_VAR,
        ):
            _items = [x for x in i.SubItems if x]
            if i.VarName in self.pkgspecific:
                _items = _items[1:]

            if i.VarOp.strip() in ("+=", ".="):
                op = "append"
            elif i.VarOp.strip() in ("=+", "=."):
                op = "prepend"
            else:
                continue

            if _items and _items[0] != op:
                res.append((i, op))

        return res

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        for i, op in self.__getMatches(_file, stash):
            res += self.finding(i.Origin, i.InFileLine,
                                override_msg=self.Msg.format(op=op))
        return res

    def fixone(self, item, op):
        varname = item.VarName
        if item.VarName in self.pkgspecific:
            varname += ":" + item.SubItems[0]

        def replacer(v):
            ret = v.replace(
                varname, varname + ":" + op,
            ).replace(
                item.VarOp, " = ",
            )
            extra_space = " " if "+" in item.VarOp else ""
            if op == "append":
                opening_quote = ret.find(item.VarValue[0])
                if extra_space and ret[opening_quote + 1] not in " \t\n":
                    ret = ret[:opening_quote + 1] + extra_space + ret[opening_quote + 1:]
            elif op == "prepend":
                closing_quote = ret.rfind(item.VarValue[-1])
                if extra_space and ret[closing_quote - 1] not in " \t\n":
                    ret = ret[:closing_quote] + extra_space + ret[closing_quote:]

            return ret

        item.Raw = replacer(item.Raw)
        item.RealRaw = replacer(item.RealRaw)

    def fix(self, _file: str, stash: Stash) -> List[str]:
        res = []

        for i, op in self.__getMatches(_file, stash):
            self.fixone(i, op)
            res.append(_file)
        return res
