from oelint_adv.cls_rule import Rule
from oelint_parser.cls_item import Variable
from oelint_parser.rpl_regex import RegexRpl


class VarDependsClass(Rule):
    def __init__(self):
        super().__init__(id='oelint.vars.dependsclass',
                         severity='error',
                         message='{org} should be {patched} as it\'s a {class_} only recipe')

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue='DEPENDS')
        inherits = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                     attribute=Variable.ATTR_VAR, attributeValue='inherit')

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
