from typing import List, Tuple

from oelint_parser.cls_item import Inherit
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarInheritDevtool(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.var.inheritdevtool',
                         severity='warning',
                         message='It is better to use inherit_defer for {statement}, to enable proper devtool integration',
                         appendix=['native', 'nativesdk', 'cross'],
                         valid_from_release='scarthgap')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Inherit] = stash.GetItemsFor(filename=_file, classifier=Inherit.CLASSIFIER)
        for i in items:
            if 'native' in i.get_items() and i.Statement != 'inherit_defer':
                res += self.finding(i.Origin, i.InFileLine,
                                    override_msg=self.Msg.format(statement='native'),
                                    appendix='native',
                                    )
            if 'nativesdk' in i.get_items() and i.Statement != 'inherit_defer':
                res += self.finding(i.Origin, i.InFileLine,
                                    override_msg=self.Msg.format(statement='nativesdk'),
                                    appendix='nativesdk',
                                    )
            if 'cross' in i.get_items() and i.Statement != 'inherit_defer':
                res += self.finding(i.Origin, i.InFileLine,
                                    override_msg=self.Msg.format(statement='cross'),
                                    appendix='cross',
                                    )
        return res
