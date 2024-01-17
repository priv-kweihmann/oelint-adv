from typing import List, Tuple
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class VarHomepagePing(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.homepageping',
                         severity='warning',
                         message='\'HOMEPAGE\' isn\'t reachable')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR, attributeValue='HOMEPAGE')
        for i in items:
            try:
                req = Request(i.VarValueStripped)  # noqa: S310 - we can take the risk of calling unexpected schemes here
                try:
                    urlopen(req, timeout=4)  # noqa: S310 - we can take the risk of calling unexpected schemes here
                except HTTPError as e:
                    if e.code == 404:  # pragma: no cover
                        res += self.finding(i.Origin, i.InFileLine)  # pragma: no cover
                except URLError:
                    res += self.finding(i.Origin, i.InFileLine)
            except ValueError:
                res += self.finding(i.Origin, i.InFileLine)
            except Exception:  # noqa: S110, pragma: no cover
                pass  # pragma: no cover
        return res
