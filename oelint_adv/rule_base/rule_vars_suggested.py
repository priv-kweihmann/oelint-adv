from typing import List, Tuple

from oelint_parser.cls_item import Inherit, Variable
from oelint_parser.cls_stash import Stash
from oelint_parser.constants import CONSTANTS

from oelint_adv.cls_rule import Rule, Classification


class VarSuggestedExists(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.var.suggestedvar',
                         severity='info',
                         message='<FOO>',
                         run_on=[Classification.RECIPE],
                         appendix=CONSTANTS.GetByPath('variables/suggested'))

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        _is_pkg_group = stash.IsPackageGroup(_file)
        _is_image = stash.IsImage(_file)
        all_items: List[Variable] = stash.GetItemsFor(filename=_file,
                                                      classifier=Variable.CLASSIFIER,
                                                      attribute=Variable.ATTR_VAR,
                                                      attributeValue=CONSTANTS.GetByPath('variables/suggested'))
        inherits: List[Inherit] = stash.GetItemsFor(filename=_file,
                                                    classifier=Inherit.CLASSIFIER)

        def get_class_specific(varname: str, inherits: List[Inherit]) -> bool:
            return any(True for x in inherits if any(y in x.get_items()
                                                     for y in (CONSTANTS.GetByPath(f'oelint-suggestedvar/{varname}-exclude-classes') or [])))
        for var_ in CONSTANTS.GetByPath('variables/suggested'):
            if var_ == 'BBCLASSEXTEND':
                # this is better covered by oelint_adv/rule_base/rule_vars_bbclassextends.py
                continue
            if _is_pkg_group and var_ in CONSTANTS.GetByPath('oelint-suggestedvar/pkggroup-excludes'):
                continue
            if _is_image and var_ in CONSTANTS.GetByPath('oelint-suggestedvar/image-excludes'):
                continue
            if get_class_specific(var_, inherits):
                continue
            items = [x for x in all_items if x.VarName == var_]
            if not any(items):
                res += self.finding(_file, 0, 'Variable \'{var}\' should be set'.format(var=var_), appendix=var_)
        return res
