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
                    'srcuri-exclude-classes': [
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
        items: List[Variable] = stash.GetItemsFor(filename=_file,
                                                  classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR,
                                                  attributeValue=CONSTANTS.VariablesMandatory)
        inherits: List[Inherit] = stash.GetItemsFor(filename=_file,
                                                    classifier=Inherit.CLASSIFIER)
        # some classes set SRC_URI on their own, do not warn here
        src_setting_inherits = any(True for x in inherits if any(y in x.get_items()
                                   for y in CONSTANTS.GetByPath('oelint-mandatoryvar/srcuri-exclude-classes')))
        for var_ in CONSTANTS.VariablesMandatory:
            if _is_pkg_group and var_ in CONSTANTS.GetByPath('oelint-mandatoryvar/pkggroup-excludes'):
                continue
            if _is_image and var_ in CONSTANTS.GetByPath('oelint-mandatoryvar/image-excludes'):
                continue
            if src_setting_inherits and var_ in ['SRC_URI']:
                continue
            filtered = stash.Reduce(items, attribute=Variable.ATTR_VAR, attributeValue=var_)
            if not any(filtered):
                res += self.finding(_file, 0,
                                    'Variable \'{a}\' should be set'.format(a=var_), appendix=var_)
        return res
