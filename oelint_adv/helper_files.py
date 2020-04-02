import glob
import os
import re
from urllib.parse import urlparse

from oelint_adv.cls_item import Variable
from oelint_adv.const_vars import get_known_mirrors


def get_files(stash, _file, pattern):
    res = []
    src_uris = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                 attribute=Variable.ATTR_VAR, attributeValue="SRC_URI")
    files_paths = list(
        set(["{}/*/{}".format(os.path.dirname(x.Origin), pattern) for x in src_uris]))
    for item in src_uris:
        files_paths += list(set(["{}/*/{}".format(os.path.dirname(x.Origin), pattern)
                                 for x in stash.GetItemsFor(filename=item.Origin)]))
    for item in files_paths:
        res += glob.glob(item)
    return list(set(res))


def find_local_or_in_layer(name, localdir):
    if os.path.exists(os.path.join(localdir, name)):
        return os.path.join(localdir, name)
    _curdir = localdir
    while os.path.isdir(_curdir):
        if _curdir == "/":
            break
        _curdir = os.path.dirname(_curdir)
        if os.path.exists(os.path.join(_curdir, "conf/layer.conf")):
            if os.path.exists(os.path.join(_curdir, name)):
                return os.path.join(_curdir, name)
            else:
                break
    return None


def _replace_with_known_mirrors(_in):
    """
    Replace the known mirror configuration items
    """
    for k, v in get_known_mirrors().items():
        _in = _in.replace(k, v)
    return _in


def get_scr_components(string):
    """
        Parses an URL string
        returns a dict with
            scheme = protcol used
            src = path to call
            options = dict with options added to URL
    """
    _url = urlparse(_replace_with_known_mirrors(string))
    _scheme = _url.scheme
    _tmp = _url.netloc
    if _url.path:
        _tmp += "/" + _url.path.lstrip("/")
    _path = _tmp.split(";")[0]
    _options = _tmp.split(";")[1:]
    _parsed_opt = {x.split("=")[0]: x.split("=")[1] for x in _options if "=" in x}
    return {"scheme": _scheme, "src": _path, "options": _parsed_opt}


def safe_linesplit(string):
    return re.split(r"\s|\t|\x1b", string)

def guess_recipe_name(_file):
    _name, _ext = os.path.splitext(os.path.basename(_file))
    return _name.split("_")[0]

def guess_recipe_version(_file):
    _name, _ext = os.path.splitext(os.path.basename(_file))
    return _name.split("_")[-1]

def expand_term(stash, _file, value):
    pattern = r"\$\{(.+?)\}"
    res = str(value)
    for m in re.finditer(pattern, value):
        _comp = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue=m.group(1))
        if any(_comp):
            res = res.replace(m.group(0), expand_term(stash, _file, _comp[0].VarValueStripped))
        elif m.group(1) in ["PN", "BPN"]:
            res = res.replace(m.group(0), guess_recipe_name(_file))
        elif m.group(1) in ["PV"]:
            res = res.replace(m.group(0), guess_recipe_version(_file))
    return res

def get_valid_package_names(stash, _file):
    res = set()
    _comp = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                              attribute=Variable.ATTR_VAR, attributeValue="PACKAGES")
    _recipe_name = guess_recipe_name(_file)
    for item in _comp:
        for pkg in [x for x in safe_linesplit(item.VarValueStripped) if x]:
            _pkg = pkg.replace("${PN}", _recipe_name)
            res.add(_pkg)
    return res

def get_valid_named_resources(stash, _file):
    res = set()
    _comp = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                              attribute=Variable.ATTR_VAR, attributeValue="SRC_URI")
    _recipe_name = guess_recipe_name(_file)
    for item in _comp:
        for name in [x for x in safe_linesplit(item.VarValueStripped) if x]:
            _url = get_scr_components(name)
            if "name" in _url["options"]:
                res.add(_url["options"]["name"].replace("${PN}", _recipe_name))
    return res
