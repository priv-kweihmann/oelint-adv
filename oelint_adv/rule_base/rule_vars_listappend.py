from oelint_adv.cls_rule import Rule
from oelint_parser.cls_item import Variable


class VarListAppend(Rule):
    def __init__(self):
        super().__init__(id='oelint.vars.listappend',
                         severity='error',
                         message='<FOO>')

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(
            filename=_file, classifier=Variable.CLASSIFIER)
        needles = ['PACKAGES', 'SRC_URI', 'FILES', 'RDEPENDS', 'DEPENDS']

        for i in items:
            if not any(i.VarName.startswith(x) for x in needles):
                continue
            if i.VarName.startswith('FILESEXTRAPATHS'):
                # Caught by the `FILES` above but this list is colon separated.
                continue
            ops = i.AppendOperation()
            if not i.VarValue.startswith('" ') and any(x in ops for x in ['append', ' .= ']):
                res += self.finding(i.Origin, i.InFileLine,
                                    override_msg='Append to list should start with a blank')
            if not i.VarValue.endswith(' "') and any(x in ops for x in ['prepend', ' =. ']):
                res += self.finding(i.Origin, i.InFileLine,
                                    override_msg='Prepend to list should end with a blank')
        return res
