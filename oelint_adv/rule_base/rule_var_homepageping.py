from urllib.error import HTTPError
from urllib.error import URLError
from urllib.request import Request
from urllib.request import urlopen

from oelint_adv.cls_rule import Rule
from oelint_parser.cls_item import Variable


class VarHomepagePing(Rule):
    def __init__(self):
        super().__init__(id='oelint.vars.homepageping',
                         severity='warning',
                         message='\'HOMEPAGE\' isn\'t reachable')

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue='HOMEPAGE')
        for i in items:
            try:
                req = Request(i.VarValueStripped)  # noqa: S310 - we can take the risk of calling unexpected schemes here
                try:
                    urlopen(req, timeout=4)  # noqa: S310 - we can take the risk of calling unexpected schemes here
                except HTTPError as e:
                    if e.code == 404:  # pragma: no cover
                        res += self.finding(i.Origin,
                                            i.InFileLine)  # pragma: no cover
                except URLError:
                    res += self.finding(i.Origin, i.InFileLine)
            except ValueError:
                res += self.finding(i.Origin, i.InFileLine)
            except Exception:  # pragma: no cover
                pass  # pragma: no cover
        return res
