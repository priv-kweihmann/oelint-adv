from typing import List, Tuple

from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class FooMagicRule(Rule):
    def __init__(self) -> None:
        super().__init__(id='foocorp.foo.magic',
                         severity='error',
                         message='Too much foo happening here')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items = stash.GetItemsFor(filename=_file)
        for i in items:
            if 'Foo' in i.Raw:
                res += self.finding(i.Origin, i.InFileLine)
        return res

    # To provide automatic fixing capability
    # add the following optional function
    def fix(self, _file: str, stash: Stash) -> List[str]:
        res = []
        items = stash.GetItemsFor(filename=_file)
        for i in items:
            if 'Foo' in i.Raw:
                # you have to replace the content of `RealRaw` and `Raw`
                # with the fixed content
                # `Raw` is the raw block with expanded inlines blocks
                # `RealRaw` is the raw block without any modifications
                #           this is what will be actually written to the file
                i.RealRaw = i.RealRaw.replace('Foo', 'Bar')
                i.Raw = i.Raw.replace('Foo', 'Bar')
                # Return the file name to signalize that fixes have been
                # applied
                res.append(_file)
        return res
