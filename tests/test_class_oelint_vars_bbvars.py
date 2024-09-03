import pytest  # noqa: I900

from .base import TestBaseClass


class TestClassOelintVarsBBVars(TestBaseClass):

    def __generate_sample_code(self, var, operation):
        return '''
            {var} {operation} "foo"
            '''.format(var=var, operation=operation)

    @pytest.mark.parametrize('id_', ['oelint.vars.bbvars'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('var', [
        'BB_CONSOLELOG',
        'BB_CURRENTTASK',
        'BB_DANGLINGAPPENDS_WARNONLY',
        'BB_DEFAULT_TASK',
        'BB_DISKMON_DIRS',
        'BB_DISKMON_WARNINTERVAL',
        'BB_ENV_EXTRAWHITE',
        'BB_ENV_WHITELIST',
        'BB_FETCH_PREMIRRORONLY',
        'BB_FILENAME',
        'BB_GENERATE_MIRROR_TARBALLS',
        'BB_HASHBASE_WHITELIST',
        'BB_HASHCHECK_FUNCTION',
        'BB_HASHCONFIG_WHITELIST',
        'BB_INVALIDCONF',
        'BB_LOGFMT',
        'BB_NICE_LEVEL',
        'BB_NO_NETWORK',
        'BB_NUMBER_PARSE_THREADS',
        'BB_NUMBER_THREADS',
        'BB_ORIGENV',
        'BB_PRESERVE_ENV',
        'BB_RUNFMT',
        'BB_RUNTASK',
        'BB_SCHEDULER',
        'BB_SCHEDULERS',
        'BB_SETSCENE_DEPVALID',
        'BB_SETSCENE_VERIFY_FUNCTION',
        'BB_SIGNATURE_EXCLUDE_FLAGS',
        'BB_SIGNATURE_HANDLER',
        'BB_SRCREV_POLICY',
        'BB_STAMP_POLICY',
        'BB_STAMP_WHITELIST',
        'BB_STRICT_CHECKSUM',
        'BB_TASK_NICE_LEVEL',
        'BB_TASKHASH',
        'BB_VERBOSE_LOGS',
        'BB_WORKERCONTEXT',
        'BBDEBUG',
        'BBFILE_COLLECTIONS',
        'BBFILE_PATTERN',
        'BBFILE_PRIORITY',
        'BBFILES',
        'BBINCLUDED',
        'BBINCLUDELOGS',
        'BBINCLUDELOGS_LINES',
        'BBLAYERS',
        'BBMASK',
        'BBPATH',
        'BBSERVER',
        'BBVERSIONS',
        'BITBAKE_UI',
        'BUILDNAME',
        'CACHE',
        'DL_DIR',
        'FILE',
        'FILESDIR',
        'FILESPATH',
        'LAYERDEPENDS',
        'LAYERDIR',
        'LAYERVERSION',
        'MIRRORS',
        'MULTI_PROVIDER_WHITELIST',
        'PERSISTENT_DIR',
        'PREFERRED_PROVIDER',
        'PREFERRED_PROVIDERS',
        'PREFERRED_VERSION',
        'PREMIRRORS',
        'PRSERV_HOST',
        'STAMP',
        'TOPDIR',
    ])
    @pytest.mark.parametrize('operation', ['=', ':=', '.=', '=.', '+=', '=+', ' =+'])
    def test_bad(self, id_, occurrence, var, operation):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(var, operation),
        }
        id_ += '.{var}'.format(var=var)
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.bbvars'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('filename', [
        'conf/layer.conf',
        'conf/machine/mymachine.conf',
        'conf/distro/mydistro.conf',
    ])
    def test_good_conf_files(self, id_, occurrence, filename):
        input_ = {
            filename: self.__generate_sample_code('TOPDIR', '='),
        }
        id_ += '.{var}'.format(var='TOPDIR')
        self.check_for_id(self._create_args(input_, ['--mode=all']), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.bbvars'])
    def test_good_global_inherit(self, id_):
        input_ = {
            'conf/layer.conf': 'INHERIT += "foo"',
            'conf/classes/foo.bbclass': self.__generate_sample_code('TOPDIR', '='),
        }
        id_ += '.{var}'.format(var='INHERIT')
        self.check_for_id(self._create_args(input_, ['--mode=all']), id_, 0)

    @pytest.mark.parametrize('id_', ['oelint.vars.bbvars'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('var', [
        'INHERIT',
    ])
    @pytest.mark.parametrize('operation', ['+='])
    def test_bad_inherit(self, id_, occurrence, var, operation):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(var, operation),
        }
        id_ += '.{var}'.format(var=var)
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.vars.bbvars'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('var', [
        'BB_CONSOLELOG',
        'BB_CURRENTTASK',
        'BB_DANGLINGAPPENDS_WARNONLY',
        'BB_DEFAULT_TASK',
        'BB_DISKMON_DIRS',
        'BB_DISKMON_WARNINTERVAL',
        'BB_ENV_EXTRAWHITE',
        'BB_ENV_WHITELIST',
        'BB_FETCH_PREMIRRORONLY',
        'BB_FILENAME',
        'BB_GENERATE_MIRROR_TARBALLS',
        'BB_HASHBASE_WHITELIST',
        'BB_HASHCHECK_FUNCTION',
        'BB_HASHCONFIG_WHITELIST',
        'BB_INVALIDCONF',
        'BB_LOGFMT',
        'BB_NICE_LEVEL',
        'BB_NO_NETWORK',
        'BB_NUMBER_PARSE_THREADS',
        'BB_NUMBER_THREADS',
        'BB_ORIGENV',
        'BB_PRESERVE_ENV',
        'BB_RUNFMT',
        'BB_RUNTASK',
        'BB_SCHEDULER',
        'BB_SCHEDULERS',
        'BB_SETSCENE_DEPVALID',
        'BB_SETSCENE_VERIFY_FUNCTION',
        'BB_SIGNATURE_EXCLUDE_FLAGS',
        'BB_SIGNATURE_HANDLER',
        'BB_SRCREV_POLICY',
        'BB_STAMP_POLICY',
        'BB_STAMP_WHITELIST',
        'BB_STRICT_CHECKSUM',
        'BB_TASK_NICE_LEVEL',
        'BB_TASKHASH',
        'BB_VERBOSE_LOGS',
        'BB_WORKERCONTEXT',
        'BBDEBUG',
        'BBFILE_COLLECTIONS',
        'BBFILE_PATTERN',
        'BBFILE_PRIORITY',
        'BBFILES',
        'BBINCLUDED',
        'BBINCLUDELOGS',
        'BBINCLUDELOGS_LINES',
        'BBLAYERS',
        'BBMASK',
        'BBPATH',
        'BBSERVER',
        'BBVERSIONS',
        'BITBAKE_UI',
        'BUILDNAME',
        'CACHE',
        'DEFAULT_PREFERENCE',
        'DL_DIR',
        'FILE',
        'FILESDIR',
        'FILESPATH',
        'LAYERDEPENDS',
        'LAYERDIR',
        'LAYERVERSION',
        'MIRRORS',
        'MULTI_PROVIDER_WHITELIST',
        'PERSISTENT_DIR',
        'PREFERRED_PROVIDER',
        'PREFERRED_PROVIDERS',
        'PREFERRED_VERSION',
        'PREMIRRORS',
        'PRSERV_HOST',
        'STAMP',
        'TOPDIR',
    ])
    @pytest.mark.parametrize('operation', ['?=', '??=', ' ??='])
    def test_good_weak(self, id_, occurrence, var, operation):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(var, operation),
        }
        id_ += '.{var}'.format(var=var)
        self.check_for_id(self._create_args(input_), id_, occurrence)
