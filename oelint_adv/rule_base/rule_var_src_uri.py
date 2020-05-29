from oelint_adv.cls_item import Variable
from oelint_adv.cls_rule import Rule
from oelint_adv.helper_files import get_scr_components, expand_term
from oelint_adv.parser import INLINE_BLOCK


class VarSRCUriOptions(Rule):
    def __init__(self):
        super().__init__(id="oelint.vars.srcurioptions",
                         severity="warning",
                         message="<FOO>")
        self._general_options = [
            "apply",
            "destsuffix",
            "name",
            "patchdir",
            "striplevel",
            "subdir",
            "unpack"
        ]
        self._valid_options = {
            "bzr": [
                "protocol",
                "scmdata"
            ],
            "crcc": [
                "module",
                "proto",
                "vob"
            ],
            "cvs": [
                "date",
                "fullpath",
                "localdir",
                "method",
                "module",
                "norecurse",
                "port",
                "rsh",
                "scmdata",
                "tag"
            ],
            "file": [
                "downloadfilename"
            ],
            "ftp": [
                "downloadfilename"
            ],
            "git": [
                "branch",
                "destsuffix",
                "nobranch",
                "nocheckout",
                "protocol",
                "rebaseable",
                "rev",
                "subpath",
                "tag",
                "usehead"
            ],
            "gitsm": [
                "branch",
                "destsuffix",
                "nobranch",
                "nocheckout",
                "protocol",
                "rebaseable",
                "rev",
                "subpath",
                "tag",
                "usehead"
            ],
            "gitannex": [],
            "hg": [
                "module",
                "rev",
                "scmdata",
                "protocol"
            ],
            "http": [
                "downloadfilename"
            ],
            "https": [
                "downloadfilename"
            ],
            "osc": [
                "module",
                "protocol",
                "rev"
            ],
            "p4": [
                "revision"
            ],
            "repo": [
                "branch",
                "manifest",
                "protocol"
            ],
            "ssh": [],
            "s3": [
                "downloadfilename"
            ],
            "sftp": [
                "downloadfilename",
                "protocol"
            ],
            "npm": [
                "name",
                "noverify",
                "version"
            ],
            "npmsw": [
                "dev",
            ],
            "svn": [
                "module",
                "path_spec",
                "protocol",
                "rev",
                "scmdata",
                "ssh",
                "transportuser"
            ],
        }

    def __analyse(self, i, _input, _index):
        _url = get_scr_components(_input)
        res = []
        # For certain types of file:// url parsing fails
        # ignore those
        if _url["scheme"] not in self._valid_options.keys() and \
           not _input.strip().startswith("file://") and _url["scheme"]:
            res += self.finding(i.Origin, i.InFileLine + _index,
                                "Fetcher '{}' is not known".format(_url["scheme"]))
        else:
            for k, _ in _url["options"].items():
                if k not in self._valid_options[_url["scheme"]] + self._general_options:
                    res += self.finding(i.Origin, i.InFileLine + _index,
                                        "Option '{}' is not known with this fetcher type".format(k))
        return res

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue="SRC_URI")
        for i in items:
            if any([i.Flag.endswith(x) for x in ["md5sum", "sha256sum"]]):
                # These are just the hashes
                continue
            lines = [y.strip('"') for y in i.get_items() if y]
            for x in lines:
                if x == INLINE_BLOCK:
                    continue
                res += self.__analyse(i, x, lines.index(x))
        return res
