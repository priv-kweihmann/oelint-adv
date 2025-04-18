from typing import List, Tuple

from oelint_parser.cls_item import Variable, Inherit, Function
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule, Classification


class VarsInappClassOverride(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.inappclassoverride',
                         severity='warning',
                         run_on=[Classification.RECIPE],
                         message='{var} is using {override}, but the recipe does not set {class_} in BBCLASSEXTEND or inherits the class {class_}')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        inherits = set()
        for item in stash.GetItemsFor(filename=_file, classifier=Inherit.CLASSIFIER):
            inherits.update(item.get_items())
        bbclassextend = stash.ExpandVar(_file, Variable.ATTR_VAR, attributeValue='BBCLASSEXTEND').get('BBCLASSEXTEND', [])

        for item in stash.GetItemsFor(filename=_file, classifier=[Variable.CLASSIFIER, Function.CLASSIFIER]):
            for needle in [('class-native', 'native'), ('class-nativesdk', 'nativesdk')]:
                override, class_ = needle
                if override not in item.SubItems:
                    continue
                if class_ in bbclassextend or class_ in inherits:
                    continue
                name = item.FuncName if isinstance(item, Function) else item.VarName
                res += self.finding(item.Origin, item.InFileLine,
                                    override_msg=self.Msg.format(var=name, override=override, class_=class_))
        return res
