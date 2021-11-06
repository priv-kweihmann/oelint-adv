from oelint_adv.cls_rule import Rule


class FooMagicRule(Rule):
    def __init__(self):
        super().__init__(id='foocorp.foo.magic',
                         severity='error',
                         message='Too much foo happening here')

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file)
        for i in items:
            if 'Foo' in i.Raw:
                res += self.finding(i.Origin, i.InFileLine)
        return res
