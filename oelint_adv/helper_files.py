import glob
import os
from urllib.parse import urlparse

from oelint_adv.cls_item import Variable


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


def get_scr_components(string):
    """
        Parses an URL string
        returns a dict with
            scheme = protcol used
            src = path to call
            options = dict with options added to URL
    """
    _url = urlparse(string)
    _scheme = _url.scheme
    _options = _url.netloc.split(";")[1:]
    _path = _url.netloc.split(";")[0]
    if _url.path:
        if not _path.endswith("/") and not _url.path.startswith("/"):
            _path += "/"
        _path += _url.path
    _parsed_opt = {x.split("=")[0]: x.split("=")[1] for x in _options}
    return {"scheme": _scheme, "src": _path, "options": _parsed_opt}
