import pytest  # noqa: I900

from .base import TestBaseClass

OPTIONS_AVAILABLE = [
    'apply',
    'branch',
    'date',
    'destsuffix',
    'dev',
    'downloadfilename',
    'fullpath',
    'localdir',
    'manifest',
    'md5sum',
    'method',
    'module',
    'name',
    'nobranch',
    'nocheckout',
    'norecurse',
    'noverify',
    'patchdir',
    'path_spec',
    'port',
    'proto',
    'protocol',
    'rebaseable',
    'rev',
    'revision',
    'rsh',
    'scmdata',
    'ssh',
    'sha256sum',
    'striplevel',
    'subdir',
    'subpath',
    'tag',
    'transportuser',
    'unpack',
    'usehead',
    'version',
    'vob',
    'unknownoperation',
]
OPTION_MAPPING = {
    'az': [
        'apply',
        'destsuffix',
        'md5sum',
        'name',
        'patchdir',
        'sha256sum',
        'striplevel',
        'subdir',
        'unpack',
    ],
    'bzr': [
        'apply',
        'destsuffix',
        'name',
        'patchdir',
        'protocol',
        'scmdata',
        'striplevel',
        'subdir',
        'unpack',
    ],
    'crate': [
        'apply',
        'destsuffix',
        'downloadfilename',
        'name',
        'patchdir',
        'striplevel',
        'subdir',
        'unpack',
    ],
    'crcc': [
        'apply',
        'destsuffix',
        'module',
        'name',
        'patchdir',
        'protocol',
        'striplevel',
        'subdir',
        'unpack',
        'vob',
    ],
    'cvs': [
        'apply',
        'date',
        'destsuffix',
        'fullpath',
        'localdir',
        'method',
        'module',
        'name',
        'norecurse',
        'patchdir',
        'port',
        'rsh',
        'scmdata',
        'striplevel',
        'subdir',
        'tag',
        'unpack',
    ],
    'file': [
        'apply',
        'destsuffix',
        'downloadfilename',
        'name',
        'patchdir',
        'striplevel',
        'subdir',
        'unpack',
    ],
    'ftp': [
        'apply',
        'destsuffix',
        'downloadfilename',
        'md5sum',
        'name',
        'patchdir',
        'sha256sum',
        'striplevel',
        'subdir',
        'unpack',
    ],
    'gs': [
        'downloadfilename',
    ],
    'git': [
        'apply',
        'branch',
        'destsuffix',
        'name',
        'nobranch',
        'nocheckout',
        'patchdir',
        'protocol',
        'rebaseable',
        'rev',
        'striplevel',
        'subdir',
        'subpath',
        'tag',
        'unpack',
        'usehead',
        'user',
    ],
    'gitsm': [
        'apply',
        'branch',
        'destsuffix',
        'name',
        'nobranch',
        'nocheckout',
        'patchdir',
        'protocol',
        'rebaseable',
        'rev',
        'striplevel',
        'subdir',
        'subpath',
        'tag',
        'unpack',
        'usehead',
    ],
    'gitannex': [
        'apply',
        'destsuffix',
        'name',
        'patchdir',
        'striplevel',
        'subdir',
        'unpack',
    ],
    'gn': [
        'destdir',
        'name',
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
        'apply',
        'destsuffix',
        'module',
        'name',
        'patchdir',
        'protocol',
        'rev',
        'scmdata',
        'striplevel',
        'subdir',
        'unpack',
    ],
    'http': [
        'apply',
        'destsuffix',
        'downloadfilename',
        'md5sum',
        'name',
        'patchdir',
        'sha256sum',
        'striplevel',
        'subdir',
        'unpack',
    ],
    'https': [
        'apply',
        'destsuffix',
        'downloadfilename',
        'md5sum',
        'name',
        'patchdir',
        'sha256sum',
        'striplevel',
        'subdir',
        'unpack',
    ],
    'osc': [
        'apply',
        'destsuffix',
        'module',
        'name',
        'patchdir',
        'protocol',
        'rev',
        'striplevel',
        'subdir',
        'unpack',
    ],
    'p4': [
        'apply',
        'destsuffix',
        'name',
        'patchdir',
        'revision',
        'striplevel',
        'subdir',
        'unpack',
    ],
    'repo': [
        'apply',
        'branch',
        'destsuffix',
        'manifest',
        'name',
        'patchdir',
        'protocol',
        'striplevel',
        'subdir',
        'unpack',
    ],
    'ssh': [
        'apply',
        'destsuffix',
        'name',
        'patchdir',
        'striplevel',
        'subdir',
        'unpack',
    ],
    's3': [
        'apply',
        'destsuffix',
        'downloadfilename',
        'md5sum',
        'name',
        'patchdir',
        'sha256sum',
        'striplevel',
        'subdir',
        'unpack',
    ],
    'sftp': [
        'apply',
        'destsuffix',
        'downloadfilename',
        'md5sum',
        'name',
        'patchdir',
        'protocol',
        'sha256sum',
        'striplevel',
        'subdir',
        'unpack',
    ],
    'npm': [
        'apply',
        'destsuffix',
        'downloadfilename',
        'name',
        'noverify',
        'package',
        'patchdir',
        'striplevel',
        'subdir',
        'unpack',
        'version',
    ],
    'npmsw': [
        'apply',
        'destsuffix',
        'dev',
        'downloadfilename',
        'name',
        'patchdir',
        'protocol',
        'rev',
        'striplevel',
        'subdir',
        'unpack',
    ],
    'svn': [
        'apply',
        'destsuffix',
        'module',
        'name',
        'patchdir',
        'path_spec',
        'protocol',
        'rev',
        'scmdata',
        'ssh',
        'striplevel',
        'subdir',
        'transportuser',
        'unpack',
    ],
}


class TestClassOelintVarsSRCURIOptions(TestBaseClass):

    def __generate_sample_code(self, protocol, option):
        if not option:
            return '''
                SRC_URI += "{protocol}://foo"
                '''.format(protocol=protocol)
        return '''
            SRC_URI += "{protocol}://foo;{option}=1"
            '''.format(protocol=protocol, option=option)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('protocol', ['az'])
    @pytest.mark.parametrize('option', [x for x in OPTIONS_AVAILABLE if x not in OPTION_MAPPING['az']])
    def test_bad_az(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('protocol', ['az'])
    @pytest.mark.parametrize('option', OPTION_MAPPING['az'])
    def test_good_az(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('protocol', ['bzr'])
    @pytest.mark.parametrize('option', [x for x in OPTIONS_AVAILABLE if x not in OPTION_MAPPING['bzr']])
    def test_bad_bzr(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('protocol', ['bzr'])
    @pytest.mark.parametrize('option', OPTION_MAPPING['bzr'])
    def test_good_bzr(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('protocol', ['crate'])
    @pytest.mark.parametrize('option', [x for x in OPTIONS_AVAILABLE if x not in OPTION_MAPPING['crate']])
    def test_bad_crate(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('protocol', ['crate'])
    @pytest.mark.parametrize('option', OPTION_MAPPING['crate'])
    def test_good_crate(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('protocol', ['crcc'])
    @pytest.mark.parametrize('option', [x for x in OPTIONS_AVAILABLE if x not in OPTION_MAPPING['crcc']])
    def test_bad_crcc(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('protocol', ['crcc'])
    @pytest.mark.parametrize('option', OPTION_MAPPING['crcc'])
    def test_good_crcc(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('protocol', ['cvs'])
    @pytest.mark.parametrize('option', [x for x in OPTIONS_AVAILABLE if x not in OPTION_MAPPING['cvs']])
    def test_bad_cvs(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('protocol', ['cvs'])
    @pytest.mark.parametrize('option', OPTION_MAPPING['cvs'])
    def test_good_cvs(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('protocol', ['file'])
    @pytest.mark.parametrize('option', [x for x in OPTIONS_AVAILABLE if x not in OPTION_MAPPING['file']])
    def test_bad_file(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('protocol', ['file'])
    @pytest.mark.parametrize('option', OPTION_MAPPING['file'])
    def test_good_file(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('protocol', ['ftp'])
    @pytest.mark.parametrize('option', [x for x in OPTIONS_AVAILABLE if x not in OPTION_MAPPING['ftp']])
    def test_bad_ftp(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('protocol', ['ftp'])
    @pytest.mark.parametrize('option', OPTION_MAPPING['ftp'])
    def test_good_ftp(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('protocol', ['gs'])
    @pytest.mark.parametrize('option', ['foo', 'bar', 'baz'])
    def test_bad_gcp(self, id_, occurrence, protocol, option):
        input_ = {'oelint_adv_test.bb': self.__generate_sample_code(protocol, option)}
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('protocol', ['gs'])
    @pytest.mark.parametrize('option', OPTION_MAPPING['gs'])
    def test_good_gcp(self, id_, occurrence, protocol, option):
        input_ = {'oelint_adv_test.bb': self.__generate_sample_code(protocol, option)}
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('protocol', ['git'])
    @pytest.mark.parametrize('option', [x for x in OPTIONS_AVAILABLE if x not in OPTION_MAPPING['git']])
    def test_bad_git(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, 'protocol=ssh;nobranch=1;' + option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('protocol', ['git'])
    @pytest.mark.parametrize('option', OPTION_MAPPING['git'])
    def test_good_git(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, 'protocol=ssh;nobranch=1;' + option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('protocol', ['gitsm'])
    @pytest.mark.parametrize('option', [x for x in OPTIONS_AVAILABLE if x not in OPTION_MAPPING['gitsm']])
    def test_bad_gitsm(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, 'protocol=ssh;nobranch=1;' + option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('protocol', ['gitsm'])
    @pytest.mark.parametrize('option', OPTION_MAPPING['gitsm'])
    def test_good_gitsm(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, 'protocol=ssh;nobranch=1;' + option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('protocol', ['gitannex'])
    @pytest.mark.parametrize('option', [x for x in OPTIONS_AVAILABLE if x not in OPTION_MAPPING['gitannex']])
    def test_bad_gitannex(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('protocol', ['gitannex'])
    @pytest.mark.parametrize('option', OPTION_MAPPING['gitannex'])
    def test_good_gitannex(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('protocol', ['gomod'])
    @pytest.mark.parametrize('option', ['xyz', 'abc'])
    def test_bad_gomod(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, 'version=1;' + option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('protocol', ['gomod'])
    @pytest.mark.parametrize('option', OPTION_MAPPING['gomod'])
    def test_good_gomod(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, 'version=1;' + option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('protocol', ['gomodgit'])
    @pytest.mark.parametrize('option', ['xyz', 'abc'])
    def test_bad_gomodgit(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, 'version=1;' + option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('protocol', ['gomodgit'])
    @pytest.mark.parametrize('option', OPTION_MAPPING['gomodgit'])
    def test_good_gomodgit(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, 'version=1;' + option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('protocol', ['hg'])
    @pytest.mark.parametrize('option', [x for x in OPTIONS_AVAILABLE if x not in OPTION_MAPPING['hg']])
    def test_bad_hg(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('protocol', ['hg'])
    @pytest.mark.parametrize('option', OPTION_MAPPING['hg'])
    def test_good_hg(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('protocol', ['http'])
    @pytest.mark.parametrize('option', [x for x in OPTIONS_AVAILABLE if x not in OPTION_MAPPING['http']])
    def test_bad_http(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('protocol', ['http'])
    @pytest.mark.parametrize('option', OPTION_MAPPING['http'])
    def test_good_http(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('protocol', ['https'])
    @pytest.mark.parametrize('option', [x for x in OPTIONS_AVAILABLE if x not in OPTION_MAPPING['https']])
    def test_bad_https(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('protocol', ['https'])
    @pytest.mark.parametrize('option', OPTION_MAPPING['https'])
    def test_good_https(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('protocol', ['osc'])
    @pytest.mark.parametrize('option', [x for x in OPTIONS_AVAILABLE if x not in OPTION_MAPPING['osc']])
    def test_bad_osc(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('protocol', ['osc'])
    @pytest.mark.parametrize('option', OPTION_MAPPING['osc'])
    def test_good_osc(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('protocol', ['p4'])
    @pytest.mark.parametrize('option', [x for x in OPTIONS_AVAILABLE if x not in OPTION_MAPPING['p4']])
    def test_bad_p4(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('protocol', ['p4'])
    @pytest.mark.parametrize('option', OPTION_MAPPING['p4'])
    def test_good_p4(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('protocol', ['repo'])
    @pytest.mark.parametrize('option', [x for x in OPTIONS_AVAILABLE if x not in OPTION_MAPPING['repo']])
    def test_bad_repo(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('protocol', ['repo'])
    @pytest.mark.parametrize('option', OPTION_MAPPING['repo'])
    def test_good_repo(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('protocol', ['ssh'])
    @pytest.mark.parametrize('option', [x for x in OPTIONS_AVAILABLE if x not in OPTION_MAPPING['ssh']])
    def test_bad_ssh(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('protocol', ['ssh'])
    @pytest.mark.parametrize('option', OPTION_MAPPING['ssh'])
    def test_good_ssh(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('protocol', ['s3'])
    @pytest.mark.parametrize('option', [x for x in OPTIONS_AVAILABLE if x not in OPTION_MAPPING['s3']])
    def test_bad_s3(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('protocol', ['s3'])
    @pytest.mark.parametrize('option', OPTION_MAPPING['s3'])
    def test_good_s3(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('protocol', ['sftp'])
    @pytest.mark.parametrize('option', [x for x in OPTIONS_AVAILABLE if x not in OPTION_MAPPING['sftp']])
    def test_bad_sftp(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('protocol', ['sftp'])
    @pytest.mark.parametrize('option', OPTION_MAPPING['sftp'])
    def test_good_sftp(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('protocol', ['npm'])
    @pytest.mark.parametrize('option', [x for x in OPTIONS_AVAILABLE if x not in OPTION_MAPPING['npm']])
    def test_bad_npm(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('protocol', ['npm'])
    @pytest.mark.parametrize('option', OPTION_MAPPING['npm'])
    def test_good_npm(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('protocol', ['npmsw'])
    @pytest.mark.parametrize('option', [x for x in OPTIONS_AVAILABLE if x not in OPTION_MAPPING['npmsw']])
    def test_bad_npmsw(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('protocol', ['npmsw'])
    @pytest.mark.parametrize('option', OPTION_MAPPING['npmsw'])
    def test_good_npmsw(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('protocol', ['svn'])
    @pytest.mark.parametrize('option', [x for x in OPTIONS_AVAILABLE if x not in OPTION_MAPPING['svn']])
    def test_bad_svn(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('protocol', ['svn'])
    @pytest.mark.parametrize('option', OPTION_MAPPING['svn'])
    def test_good_svn(self, id_, occurrence, protocol, option):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(protocol, option),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI += "${@["", "file://init.cfg"][(d.getVar(\'VIRTUAL-RUNTIME_init_manager\') == \'busybox\')]}"',
                                 },
                             ],
                             )
    def test_good_conditionals(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI += "foo.bar.baz"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI[md5sum] = "file://abc"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI[sha256sum] = "file://abc"',
                                 },
                             ],
                             )
    def test_good_edgecases_good(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI += "abc://some.corp.com"',
                                 },
                             ],
                             )
    def test_good_edgecases_bad(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.srcurioptions'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI += "file://kmeta/common;type=kmeta"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     'SRC_URI += "git://git.yoctoproject.org/yocto-kernel-cache;type=kmeta;name=meta;branch=yocto-5.10;destsuffix=${KMETA};protocol=foo"',
                                 },
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     # nooelint: oelint.vars.srcurioptions
                                     SRC_URI += "\\
                                         file://kmeta/common;type=kmeta \\
                                         abc://some.corp.com \\
                                         foo://some.other.corp \\
                                     "
                                     ''',
                                 },
                             ],
                             )
    def test_type_kmeta_allowed(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)
