from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash
from oelint_parser.constants import CONSTANTS

from oelint_adv.cls_rule import Rule


class VarSuggestedExists(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.var.suggestedvar',
                         severity='info',
                         message='<FOO>',
                         onappend=False,
                         appendix=CONSTANTS.VariablesSuggested)

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        _is_pkg_group = stash.IsPackageGroup(_file)
        all_items: List[Variable] = stash.GetItemsFor(filename=_file,
                                                      classifier=Variable.CLASSIFIER,
                                                      attribute=Variable.ATTR_VAR,
                                                      attributeValue=CONSTANTS.VariablesSuggested)
        for var_ in CONSTANTS.VariablesSuggested:
            if var_ == 'BBCLASSEXTEND':
                # this is better covered by oelint_adv/rule_base/rule_vars_bbclassextends.py
                continue
            if _is_pkg_group and var_ in ['LICENSE', 'CVE_PRODUCT']:
                continue
            items = [x for x in all_items if x.VarName == var_]
            if not any(items):
                res += self.finding(_file, 0, 'Variable \'{var}\' should be set'.format(var=var_), appendix=var_)
        return res
