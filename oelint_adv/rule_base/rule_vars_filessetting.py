from oelint_parser.cls_item import Variable
from oelint_adv.cls_rule import Rule


class VarUnneededFilesSetting(Rule):
    def __init__(self):
        super().__init__(id="oelint.vars.filessetting",
                         severity="warning",
                         message="Check for improvable FILES settings",
                         appendix=["hidden", "double"])

    def __find_match_from_stash(self, _file, stash, variable, needle, msg, appendix, onappendonly=False):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue=variable)
        for i in items:
            if needle in i.VarValue and "remove" not in i.SubItems: # pragma: no cover
                if (onappendonly and i.IsAppend()) or (not onappendonly):
                    res += self.finding(i.Origin, i.InFileLine, override_msg=msg, appendix=appendix)
        return res

    def check(self, _file, stash):
        res = []
        _expanded = stash.ExpandVar(filename=_file, attribute=Variable.ATTR_VAR)
        _seenpath = {}
        for p in _expanded["PACKAGES"]:
            _files = "FILES_{}".format(p)
            _convfiles = _files.replace(_expanded["PN"][0], "${PN}")
            if _files in _expanded:
                _pattern = _expanded[_files]
                for _p in _pattern:
                    # double setting in FILES
                    if len([x for x in _pattern if x == _p]) > 1:
                        # try to find with both unexpanded and expanded values
                        res += self.__find_match_from_stash(_file, stash, _convfiles, _p, 
                                                            "{} is already set by default or in this recipe".format(_p), "double", True)
                        res += self.__find_match_from_stash(_file, stash, _files, _p, 
                                                            "{} is already set by default or in this recipe".format(_p), "double", True)
                    # useless as hidden by previous package
                    if _p in _seenpath.keys() and _seenpath[_p] != _convfiles:
                        # try to find with both unexpanded and expanded values
                        res += self.__find_match_from_stash(_file, stash, _convfiles, _p, 
                                                            "{} is already covered by {}".format(_p, _seenpath[_p]),
                                                            "hidden")
                        res += self.__find_match_from_stash(_file, stash, _files, _p, 
                                                            "{} is already covered by {}".format(_p, _seenpath[_p]),
                                                            "hidden")
                    _seenpath[_p] = _convfiles
        return res
