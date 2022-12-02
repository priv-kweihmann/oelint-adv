from oelint_adv.cls_rule import Rule
from oelint_parser.cls_item import Variable


class VarListAppend(Rule):
    def __init__(self):
        super().__init__(id='oelint.vars.listappend',
                         severity='error',
                         message='<FOO>')

    def __getMatches(self, _file, stash):
        res_app = []
        res_pre = []
        items = stash.GetItemsFor(
            filename=_file, classifier=Variable.CLASSIFIER)
        needles = ['PACKAGES', 'SRC_URI', 'FILES', 'RDEPENDS', 'DEPENDS']

        for i in items:
            if not any(i.VarName.startswith(x) for x in needles):
                continue
            if i.VarName.startswith(('FILESEXTRAPATHS', 'FILESPATH')):
                # Caught by the `FILES` above but this list is colon separated.
                continue
            ops = i.AppendOperation()
            if not i.VarValue.startswith('" ') and any(x in ops for x in ['append', ' .= ']):
                res_app.append(i)
            if not i.VarValue.endswith(' "') and any(x in ops for x in ['prepend', ' =. ']):
                res_pre.append(i)
        return (res_app, res_pre)

    def check(self, _file, stash):
        res = []
        res_app, res_pre = self.__getMatches(_file, stash)
        for i in res_app:
            res += self.finding(i.Origin, i.InFileLine,
                                override_msg='Append to list should start with a blank')
        for i in res_pre:
            res += self.finding(i.Origin, i.InFileLine,
                                override_msg='Prepend to list should end with a blank')
        return res

    def fix(self, _file, stash):
        res = []
        res_app, res_pre = self.__getMatches(_file, stash)
        for i in res_app:
            vv_rpl = i.VarValue.replace('"', '" ', 1).replace('\'', '\' ', 1)
            i.RealRaw = i.RealRaw.replace(i.VarValue, vv_rpl)
            i.Raw = i.Raw.replace(i.VarValue, vv_rpl)
            i.VarValue = vv_rpl
            res.append(_file)
        for i in res_pre:
            vv_rpl = i.VarValue[::-1].replace('"', '" ', 1).replace('\'', '\' ', 1)[::-1]
            i.RealRaw = i.RealRaw.replace(i.VarValue, vv_rpl)
            i.Raw = i.Raw.replace(i.VarValue, vv_rpl)
            i.VarValue = vv_rpl
            res.append(_file)
        return res
