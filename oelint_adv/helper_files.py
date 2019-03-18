import os
import glob
try:
    from .cls_stash import Stash
    from .cls_item import Comment, Function, Include, Item, PythonBlock, Variable
except (SystemError, ImportError):
    from cls_stash import Stash
    from cls_item import Comment, Function, Include, Item, PythonBlock, Variable

def get_files(stash, _file, pattern):
    res = []
    src_uris = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER, attribute=Variable.ATTR_VAR, attributeValue="SRC_URI")
    files_paths = list(set(["{}/*/{}".format(os.path.dirname(x.Origin), pattern) for x in src_uris]))
    for item in src_uris:
        files_paths += list(set(["{}/*/{}".format(os.path.dirname(x.Origin), pattern) for x in stash.GetItemsFor(filename=item.Origin)]))
    for item in files_paths:
        res += glob.glob(item)
    return list(set(res))
        
def get_scr_components(string):
    comp = string.replace("\t", "").strip(" \n\"").replace("://", ";", 1).split(";")
    if len(comp) < 2:
        return { "proto": "dummy", "name": "" }
    res = { "proto": comp[0], "name": comp[1] }
    for i in range(2, len(comp)):
        sp = comp[i].split("=")
        if len(sp) > 1:
            res[sp[0]] = sp[1]
    return res

