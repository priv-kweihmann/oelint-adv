from typing import List, Tuple

from oelint_parser.cls_item import Inherit, Variable
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
        CONSTANTS.AddConstants(
            {
                'oelint-mandatoryvar':
                {
                    'image-excludes': [
                        'CVE_PRODUCT',
                        'HOMEPAGE',
                        'SRC_URI',
                    ],
                },
            },
        )

        CONSTANTS.AddConstants(
            {
                'oelint-mandatoryvar':
                {
                    'pkggroup-excludes': [
                        'CVE_PRODUCT',
                        'HOMEPAGE',
                        'LICENSE',
                        'SRC_URI',
                    ],
                },
            },
        )

        CONSTANTS.AddConstants(
            {
                'oelint-mandatoryvar':
                {
                    'SRC_URI-exclude-classes': [
                        'pypi',
                        'gnomebase',
                    ],
                },
            },
        )

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        _is_pkg_group = stash.IsPackageGroup(_file)
        _is_image = stash.IsImage(_file)
        if _file in stash.GetConfFiles():
            return []
        items: List[Variable] = stash.GetItemsFor(filename=_file,
                                                  classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR,
                                                  attributeValue=CONSTANTS.VariablesMandatory)
        inherits: List[Inherit] = stash.GetItemsFor(filename=_file,
                                                    classifier=Inherit.CLASSIFIER)

        def get_class_specific(varname: str, inherits: List[Inherit]) -> bool:
            return any(True for x in inherits if any(y in x.get_items()
                                                     for y in (CONSTANTS.GetByPath(f'oelint-mandatoryvar/{varname}-exclude-classes') or [])))

        # some classes set SRC_URI on their own, do not warn here
        for var_ in CONSTANTS.VariablesMandatory:
            if _is_pkg_group and var_ in CONSTANTS.GetByPath('oelint-mandatoryvar/pkggroup-excludes'):
                continue
            if _is_image and var_ in CONSTANTS.GetByPath('oelint-mandatoryvar/image-excludes'):
                continue
            if get_class_specific(var_, inherits):
                continue
            filtered = stash.Reduce(items, attribute=Variable.ATTR_VAR, attributeValue=var_)
            if not any(filtered):
                res += self.finding(_file, 0,
                                    'Variable \'{a}\' should be set'.format(a=var_), appendix=var_)
        return res
