from typing import List, Tuple

from oelint_parser.cls_item import Inherit, Variable
from oelint_parser.cls_stash import Stash
from oelint_parser.rpl_regex import RegexRpl

from oelint_adv.cls_rule import Rule, Classification


class VarDependsClass(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.dependsclass',
                         severity='error',
                         run_on=[Classification.RECIPE, Classification.BBAPPEND],
                         message='{org} should be {patched} as it\'s a {class_} only recipe')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR, attributeValue='DEPENDS')
        inherits: List[Inherit] = stash.GetItemsFor(filename=_file, classifier=Inherit.CLASSIFIER)

        class_ = ''
        class_name = ''
        fixed_name = ''
        for i in inherits:
            if 'native' in i.get_items():
                class_ = '^.*-native$'
                class_name = 'native'
                fixed_name = '{org}-native'
            if 'nativesdk' in i.get_items():
                class_ = '^nativesdk-.*$'
                class_name = 'nativesdk'
                fixed_name = 'nativesdk-{org}'

        if not class_:
            return res

        for i in items:
            for dep in i.get_items():
                if not RegexRpl.match(class_, dep):
                    fixed = fixed_name.format(org=dep.replace(
                        'nativesdk-', '', 1).replace('-native', '', 1))
                    res += self.finding(i.Origin, i.InFileLine, override_msg=self.Msg.format(
                        org=dep, patched=fixed, class_=class_name))
        return res
