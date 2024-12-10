from typing import List, Tuple

from oelint_parser.cls_item import Variable
from oelint_parser.cls_stash import Stash
from oelint_parser.parser import INLINE_BLOCK

from oelint_adv.cls_rule import Rule


class VarSRCUriOptions(Rule):
    def __init__(self) -> None:
        super().__init__(id='oelint.vars.srcurioptions',
                         severity='warning',
                         message='<FOO>')
        self._general_options = [
            'apply',
            'destsuffix',
            'extract',
            'name',
            'patchdir',
            'striplevel',
            'subdir',
            'unpack',
        ]
        self._valid_options = {
            'az': [
                'md5sum',
                'sha256sum',
            ],
            'bzr': [
                'protocol',
                'scmdata',
            ],
            'crate': [
                'downloadfilename',
            ],
            'crcc': [
                'module',
                'protocol',
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
                'md5sum',
                'sha256sum',
            ],
            'gs': [
                'downloadfilename',
            ],
            'git': [
                'branch',
                'destsuffix',
                'lfs',
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
                'lfs',
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
            'gn': [
                'destdir',
                'proto',
            ],
            'gomod': [
                'downloadfilename',
                'mod',
                'module',
                'version',
            ],
            'gomodgit': [
                'bareclone',
                'branch',
                'module',
                'nobranch',
                'protocol',
                'repo',
                'srcrev',
                'version',
            ],
            'hg': [
                'module',
                'rev',
                'scmdata',
                'protocol',
            ],
            'http': [
                'downloadfilename',
                'md5sum',
                'sha256sum',
            ],
            'https': [
                'downloadfilename',
                'md5sum',
                'sha256sum',
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
                'md5sum',
                'sha256sum',
            ],
            'sftp': [
                'downloadfilename',
                'md5sum',
                'protocol',
                'sha256sum',
            ],
            'npm': [
                'downloadfilename',
                'name',
                'noverify',
                'package',
                'version',
            ],
            'npmsw': [
                'dev',
                'downloadfilename',
                'protocol',
                'rev',
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

        self._required_might_options = {
            'git': ['protocol'],
            'gitsm': ['protocol'],
            'gomod': ['version'],
            'gomodgit': ['version'],
        }

        self._required_unless_options = {
            'git': {'branch': ['nobranch', 'usehead']},
            'gitsm': {'branch': ['nobranch', 'usehead']},
        }

        self._required_if_options = {
            'git': {'usehead': ['branch', 'nobranch']},
            'gitsm': {'usehead': ['branch', 'nobranch']},
        }

    def __analyse(self, stash: Stash, item: Variable, _input: str, _index: int) -> List[Tuple[str, int, str]]:
        _url = stash.GetScrComponents(_input)
        res = []
        if 'scheme' not in _url:
            return res  # pragma: no cover
        # For certain types of file:// url parsing fails
        # ignore those
        if _url['scheme'] not in self._valid_options.keys() and not _input.strip().startswith('file://') and _url['scheme']:
            res += self.finding(item.Origin, item.InFileLine + _index,
                                'Fetcher \'{a}\' is not known'.format(a=_url['scheme']),
                                blockoffset=item.InFileLine)
        else:
            for k, v in _url['options'].items():
                if _url['scheme'] not in self._valid_options:
                    continue  # pragma: no cover
                if k == 'type' and v == 'kmeta':
                    continue  # linux-yocto uses this option to indicate kernel metadata sources
                if k not in self._valid_options[_url['scheme']] + self._general_options:
                    res += self.finding(item.Origin, item.InFileLine + _index,
                                        'Option \'{a}\' is not known with this fetcher type'.format(a=k),
                                        blockoffset=item.InFileLine)
            for opt in self._required_might_options.get(_url['scheme'], []):
                if opt not in _url['options']:
                    res += self.finding(item.Origin, item.InFileLine + _index,
                                        'Fetcher \'{fetcher}\' might require option \'{option}\' to be set'.format(
                                            fetcher=_url['scheme'], option=opt),
                                        blockoffset=item.InFileLine)
            for key, val_ in self._required_unless_options.get(_url['scheme'], {}).items():
                if key not in _url['options'] and not any(x in _url['options'] for x in val_):
                    res += self.finding(item.Origin, item.InFileLine + _index,
                                        'Fetcher \'{fetcher}\' requires option \'{option}\' or any of \'{other}\' to be set'.format(
                                            fetcher=_url['scheme'], option=key, other=','.join(val_)),
                                        blockoffset=item.InFileLine)
            for key, val_ in self._required_if_options.get(_url['scheme'], {}).items():
                if key in _url['options'] and not any(x in _url['options'] for x in val_):
                    res += self.finding(item.Origin, item.InFileLine + _index,
                                        'Fetcher \'{fetcher}\' option \'{option}\' requires any of \'{other}\' to be set'.format(
                                            fetcher=_url['scheme'], option=key, other=','.join(val_)),
                                        blockoffset=item.InFileLine)
        return res

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        res = []
        items: List[Variable] = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER,
                                                  attribute=Variable.ATTR_VAR, attributeValue='SRC_URI')
        for item in items:
            lines = [y.strip('"') for y in item.get_items() if y and INLINE_BLOCK not in y]
            for x in lines:
                res += self.__analyse(stash, item, stash.ExpandTerm(_file, x), lines.index(x))  # noqa: B038
        return res

    def check_release_range(self, release_range: List[str]) -> bool:
        if 'nanbield' not in release_range:
            # GCP/gs fetcher is only supported from nanbield on
            del self._valid_options['gs']
        return super().check_release_range(release_range)
