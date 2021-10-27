from oelint_adv.cls_rule import Rule
from oelint_parser.cls_item import Variable
from oelint_parser.helper_files import get_scr_components


class VarPnBpnUsage(Rule):
    def __init__(self):
        super().__init__(id='oelint.vars.pnbpnusage',
                         severity='error',
                         message='${BPN} should be used instead of ${PN}')

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR)
        needles = ['SRC_URI']
        for i in [x for x in items if x.VarName in needles]:
            for x in i.get_items():
                _comp = get_scr_components(x)
                if '${PN}' in _comp['src']:
                    res += self.finding(i.Origin, i.InFileLine)
        return res
