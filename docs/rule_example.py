from oelint_adv.rule import Rule


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

    # To provide automatic fixing capability
    # add the following optinal function
    def fix(self, _file, stash):
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
