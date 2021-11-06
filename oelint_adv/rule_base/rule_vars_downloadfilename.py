from oelint_adv.cls_rule import Rule
from oelint_parser.cls_item import Variable
from oelint_parser.helper_files import expand_term
from oelint_parser.helper_files import get_scr_components
from oelint_parser.helper_files import guess_recipe_version


class VarsDownloadfilename(Rule):
    def __init__(self):
        super().__init__(id='oelint.vars.downloadfilename',
                         severity='warning',
                         message='Fetcher does create a download artifact without \'PV\' in the filename')

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue='SRC_URI')

        _pv = expand_term(stash, _file, '${PV}') or guess_recipe_version(_file)

        for i in items:
            for item in [expand_term(stash, _file, x) for x in i.get_items()]:
                _scrcomp = get_scr_components(item)
                if _scrcomp.get('scheme', '') in ['https', 'http', 'ftp']:
                    _src = _scrcomp.get('src', '')
                    _dfn = _scrcomp.get('options', {}).get(
                        'downloadfilename', '')

                    if _pv not in _src:
                        if _dfn and _pv in _dfn:
                            continue
                        res += self.finding(i.Origin, i.InFileLine)
        return res
