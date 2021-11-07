from oelint_adv.cls_rule import Rule
from oelint_parser.cls_item import Variable
from oelint_parser.helper_files import get_scr_components
from oelint_parser.parser import INLINE_BLOCK


class VarSRCUriOptions(Rule):
    def __init__(self):
        super().__init__(id='oelint.vars.srcurioptions',
                         severity='warning',
                         message='<FOO>')
        self._general_options = [
            'apply',
            'destsuffix',
            'name',
            'patchdir',
            'striplevel',
            'subdir',
            'unpack',
        ]
        self._valid_options = {
            'az': [],
            'bzr': [
                'protocol',
                'scmdata',
            ],
            'crcc': [
                'module',
                'proto',
                'vob',
            ],
            'cvs': [
                'date',
                'fullpath',
                'localdir',
                'method',
                'module',
                'norecurse',
                'port',
                'rsh',
                'scmdata',
                'tag',
            ],
            'file': [
                'downloadfilename',
            ],
            'ftp': [
                'downloadfilename',
            ],
            'git': [
                'branch',
                'destsuffix',
                'nobranch',
                'nocheckout',
                'protocol',
                'rebaseable',
                'rev',
                'subdir',
                'subpath',
                'tag',
                'usehead',
                'user',
            ],
            'gitsm': [
                'branch',
                'destsuffix',
                'nobranch',
                'nocheckout',
                'protocol',
                'rebaseable',
                'rev',
                'subpath',
                'tag',
                'usehead',
            ],
            'gitannex': [],
            'hg': [
                'module',
                'rev',
                'scmdata',
                'protocol',
            ],
            'http': [
                'downloadfilename',
            ],
            'https': [
                'downloadfilename',
            ],
            'osc': [
                'module',
                'protocol',
                'rev',
            ],
            'p4': [
                'revision',
            ],
            'repo': [
                'branch',
                'manifest',
                'protocol',
            ],
            'ssh': [],
            's3': [
                'downloadfilename',
            ],
            'sftp': [
                'downloadfilename',
                'protocol',
            ],
            'npm': [
                'name',
                'noverify',
                'version',
            ],
            'npmsw': [
                'dev',
            ],
            'svn': [
                'module',
                'path_spec',
                'protocol',
                'rev',
                'scmdata',
                'ssh',
                'transportuser',
            ],
        }

    def __analyse(self, item, _input, _index):
        _url = get_scr_components(_input)
        res = []
        if 'scheme' not in _url:
            return res  # pragma: no cover
        # For certain types of file:// url parsing fails
        # ignore those
        if _url['scheme'] not in self._valid_options.keys() and not _input.strip().startswith('file://') and _url['scheme']:
            res += self.finding(item.Origin, item.InFileLine + _index,
                                'Fetcher \'{a}\' is not known'.format(a=_url['scheme']))
        else:
            for k, v in _url['options'].items():
                if _url['scheme'] not in self._valid_options:
                    continue  # pragma: no cover
                if k == 'type' and v == 'kmeta':
                    continue  # linux-yocto uses this option to indicate kernel metadata sources
                if k not in self._valid_options[_url['scheme']] + self._general_options:
                    res += self.finding(item.Origin, item.InFileLine + _index,
                                        'Option \'{a}\' is not known with this fetcher type'.format(a=k))
        return res

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                  attribute=Variable.ATTR_VAR, attributeValue='SRC_URI')
        for item in items:
            if any([item.Flag.endswith(x) for x in ['md5sum', 'sha256sum']]):
                # These are just the hashes
                continue
            lines = [y.strip('"') for y in item.get_items() if y]
            for x in lines:
                if x == INLINE_BLOCK:
                    continue
                res += self.__analyse(item, x, lines.index(x))
        return res
