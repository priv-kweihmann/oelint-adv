from oelint_parser.cls_item import Variable
from oelint_adv.cls_rule import Rule
from oelint_parser.helper_files import get_scr_components
from oelint_parser.parser import INLINE_BLOCK


class VarSRCUriChecksum(Rule):
    def __init__(self):
        super().__init__(id='oelint.vars.srcurichecksum',
                         severity='error',
                         message='<FOO>')

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue="SRC_URI")
        md5sum = []
        sha256sum = []
        res_candidate = []
        for i in items:
            if i.Flag.endswith("md5sum"):
                if i.Flag == "md5sum":
                    md5sum.append("")
                else:
                    md5sum.append(i.Flag.rsplit(".", 1)[0])
            elif i.Flag.endswith("sha256sum"):
                if i.Flag == "sha256sum":
                    sha256sum.append("")
                else:
                    sha256sum.append(i.Flag.rsplit(".", 1)[0])
            else:
                lines = [y.strip('"') for y in i.get_items() if y]
                for x in lines:
                    if x == INLINE_BLOCK:
                        continue
                    _url = get_scr_components(x)
                    if _url["scheme"] in ["http", "https", "ftp", "ftps", "sftp", "s3", "az"]:
                        name = ""
                        if "name" in _url["options"]:
                            name = _url["options"]["name"]
                        res_candidate.append((name, i.Origin, i.InFileLine + lines.index(x)))

        res_candidate.sort(key=lambda tup: tup[0])

        no_name_src_uri = False
        for (name, filename, filelines) in res_candidate:
            message = ""
            if name == "":
                if no_name_src_uri:
                    message = "if SRC_URI have multiple URLs, each URL has checksum"
                else:
                    if "" not in md5sum:
                        message = "SRC_URI[md5sum]"
                    if "" not in sha256sum:
                        if len(message) > 0:
                            message += ", "
                        message += "SRC_URI[sha256sum]"
                    if len(message) > 0:
                        message += " is(are) needed"
                no_name_src_uri = True
            else:
                if name not in md5sum:
                    message = "SRC_URI[{n}.md5sum]".format(n=name)
                if name not in sha256sum:
                    if len(message) > 0:
                        message += ", "
                    message += "SRC_URI[{n}.sha256sum]".format(n=name)
                if len(message) > 0:
                    message += " is(are) needed"
            if len(message) > 0:
                res += self.finding(filename, filelines, message)

        return res
