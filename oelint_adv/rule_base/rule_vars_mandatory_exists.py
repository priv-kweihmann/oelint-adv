from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash
from oelint_parser.constants import CONSTANTS

from oelint_adv.cls_rule import Rule


class VarMandatoryExists(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.var.mandatoryvar',
                         severity='error',
                         message='<FOO>',
                         onappend=False,
                         appendix=CONSTANTS.VariablesMandatory)

    IMAGE_EXCLUDES = [
        'CVE_PRODUCT',
        'HOMEPAGE',
        'SRC_URI',
    ]

    PACKAGEGRP_EXCLUDES = [
        'CVE_PRODUCT',
        'HOMEPAGE',
        'LICENSE',
        'SRC_URI',
    ]

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        _is_pkg_group = stash.IsPackageGroup(_file)
        _is_image = stash.IsImage(_file)
        items: List[Variable] = stash.GetItemsFor(filename=_file,
                                                  classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR,
                                                  attributeValue=CONSTANTS.VariablesMandatory)
        for var_ in CONSTANTS.VariablesMandatory:
            if _is_pkg_group and var_ in VarMandatoryExists.PACKAGEGRP_EXCLUDES:
                continue
            if _is_image and var_ in VarMandatoryExists.IMAGE_EXCLUDES:
                continue
            filtered = stash.Reduce(items, attribute=Variable.ATTR_VAR, attributeValue=var_)
            if not any(filtered):
                res += self.finding(_file, 0,
                                    'Variable \'{a}\' should be set'.format(a=var_), appendix=var_)
        return res
