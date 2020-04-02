from oelint_adv.cls_item import Variable
from oelint_adv.cls_rule import Rule

from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError


class VarHomepagePrefix(Rule):
    def __init__(self):
        super().__init__(id="oelint.vars.homepageping",
                         severity="warning",
                         message="'HOMEPAGE' isn't reachable")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue="HOMEPAGE")
        for i in items:
            try:
                req = Request(i.VarValueStripped)
                try:
                    urlopen(req, timeout=4)
                except HTTPError as e:
                    if e.code == 404:
                        res += self.finding(i.Origin, i.InFileLine)
                except URLError:
                    res += self.finding(i.Origin, i.InFileLine)
            except ValueError:
                res += self.finding(i.Origin, i.InFileLine)
            except Exception:
                pass
        return res
