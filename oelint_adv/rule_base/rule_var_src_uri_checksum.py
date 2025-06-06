from typing import List, Tuple

from oelint_parser.cls_item import FlagAssignment, Item, Variable
from oelint_parser.cls_stash import Stash
from oelint_parser.parser import INLINE_BLOCK

from oelint_adv.cls_rule import Rule


class VarSRCUriChecksum(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.srcurichecksum',
                         severity='error',
                         message='<FOO>')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Item] = stash.GetItemsFor(filename=_file,
                                              classifier=[FlagAssignment.CLASSIFIER, Variable.CLASSIFIER],
                                              attribute=[FlagAssignment.ATTR_NAME, Variable.ATTR_VAR],
                                              attributeValue="SRC_URI")
        sha256sum = []
        res_candidate = []
        for i in items:
            if isinstance(i, FlagAssignment):
                if i.Flag.endswith("sha256sum"):
                    if i.Flag == "sha256sum":
                        sha256sum.append("")
                    else:
                        sha256sum.append(i.Flag.rsplit(".", 1)[0])
                if i.Flag.endswith("md5sum") and i.VarName in ['SRC_URI']:
                    res += self.finding(i.Origin, i.InFileLine, "md5sum is deprecated. It can be removed.",
                                        severity_override="warning")
            else:
                lines = [y.strip('"') for y in i.get_items() if y and y != INLINE_BLOCK]
                for index, value in enumerate(lines):
                    _url = stash.GetScrComponents(value)
                    if _url["scheme"] in ["http", "https", "ftp", "ftps", "sftp", "s3", "az"]:
                        name = ""
                        if "name" in _url["options"]:
                            name = _url["options"]["name"]
                        # If the checksum is already provided in the url, we can skip the
                        # flag check.
                        if "sha256sum" not in _url["options"]:
                            res_candidate.append((name, i.Origin, i.InFileLine + index, i.InFileLine))

        res_candidate.sort(key=lambda tup: tup[0])

        for (name, filename, filelines, blockoffset) in res_candidate:
            message = ""
            if name == "":
                if "" not in sha256sum:
                    message += "SRC_URI[sha256sum] is needed"
            elif name not in sha256sum:
                message += "SRC_URI[{n}.sha256sum] is needed".format(n=name)
            if len(message) > 0:
                res += self.finding(filename, filelines, message, blockoffset=blockoffset)

        return res
