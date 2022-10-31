import pytest  # noqa: I900

from .base import TestBaseClass

# -- known order --
# 'do_fetch',
# 'do_unpack',
# 'do_patch',
# 'do_configure',
# 'do_compile',
# 'do_install',
# 'do_populate_sysroot',
# 'do_build',
# 'do_package'


class TestClassOelintTaskOrder(TestBaseClass):

    def __generate_sample_code(self, first, second):
        return '''
            {first}() {{
                :
            }}
            {second}() {{
                :
            }}
            '''.format(first=first, second=second)

    @pytest.mark.parametrize('id_', ['oelint.task.order.do_fetch'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('pair', [
        ('do_unpack', 'do_fetch'),
        ('do_patch', 'do_fetch'),
        ('do_configure', 'do_fetch'),
        ('do_compile', 'do_fetch'),
        ('do_install', 'do_fetch'),
        ('do_populate_sysroot', 'do_fetch'),
        ('do_build', 'do_fetch'),
        ('do_package', 'do_fetch'),
    ])
    def test_bad_fetch(self, id_, occurrence, pair):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(pair[0], pair[1]),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.task.order.do_unpack'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('pair', [
        ('do_patch', 'do_unpack'),
        ('do_configure', 'do_unpack'),
        ('do_compile', 'do_unpack'),
        ('do_install', 'do_unpack'),
        ('do_populate_sysroot', 'do_unpack'),
        ('do_build', 'do_unpack'),
        ('do_package', 'do_unpack'),
    ])
    def test_bad_unpack(self, id_, occurrence, pair):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(pair[0], pair[1]),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.task.order.do_patch'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('pair', [
        ('do_configure', 'do_patch'),
        ('do_compile', 'do_patch'),
        ('do_install', 'do_patch'),
        ('do_populate_sysroot', 'do_patch'),
        ('do_build', 'do_patch'),
        ('do_package', 'do_patch'),
    ])
    def test_bad_patch(self, id_, occurrence, pair):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(pair[0], pair[1]),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.task.order.do_configure'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('pair', [
        ('do_compile', 'do_configure'),
        ('do_install', 'do_configure'),
        ('do_populate_sysroot', 'do_configure'),
        ('do_build', 'do_configure'),
        ('do_package', 'do_configure'),
    ])
    def test_bad_configure(self, id_, occurrence, pair):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(pair[0], pair[1]),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.task.order.do_compile'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('pair', [
        ('do_install', 'do_compile'),
        ('do_populate_sysroot', 'do_compile'),
        ('do_build', 'do_compile'),
        ('do_install', 'do_compile'),
        ('do_package', 'do_compile'),
    ])
    def test_bad_compile(self, id_, occurrence, pair):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(pair[0], pair[1]),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.task.order.do_install'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('pair', [
        ('do_populate_sysroot', 'do_install'),
        ('do_build', 'do_install'),
        ('do_package', 'do_install'),
    ])
    def test_bad_install(self, id_, occurrence, pair):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(pair[0], pair[1]),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.task.order.do_populate_sysroot'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('pair', [
        ('do_build', 'do_populate_sysroot'),
        ('do_package', 'do_populate_sysroot'),
    ])
    def test_bad_populate_sysroot(self, id_, occurrence, pair):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(pair[0], pair[1]),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.task.order.do_build'])
    @pytest.mark.parametrize('occurrence', [1])
    @pytest.mark.parametrize('pair', [
        ('do_package', 'do_build'),
    ])
    def test_bad_build(self, id_, occurrence, pair):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(pair[0], pair[1]),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

####

    @pytest.mark.parametrize('id_', ['oelint.task.order.do_fetch'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('pair', [
        ('do_fetch', 'do_unpack'),
        ('do_fetch', 'do_patch'),
        ('do_fetch', 'do_configure'),
        ('do_fetch', 'do_compile'),
        ('do_fetch', 'do_install'),
        ('do_fetch', 'do_populate_sysroot'),
        ('do_fetch', 'do_build'),
        ('do_fetch', 'do_package'),
    ])
    def test_good_fetch(self, id_, occurrence, pair):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(pair[0], pair[1]),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.task.order.do_unpack'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('pair', [
        ('do_unpack', 'do_patch'),
        ('do_unpack', 'do_configure'),
        ('do_unpack', 'do_compile'),
        ('do_unpack', 'do_install'),
        ('do_unpack', 'do_populate_sysroot'),
        ('do_unpack', 'do_build'),
        ('do_unpack', 'do_package'),
    ])
    def test_good_unpack(self, id_, occurrence, pair):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(pair[0], pair[1]),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.task.order.do_patch'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('pair', [
        ('do_patch', 'do_configure'),
        ('do_patch', 'do_compile'),
        ('do_patch', 'do_install'),
        ('do_patch', 'do_populate_sysroot'),
        ('do_patch', 'do_build'),
        ('do_patch', 'do_package'),
    ])
    def test_good_patch(self, id_, occurrence, pair):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(pair[0], pair[1]),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.task.order.do_configure'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('pair', [
        ('do_configure', 'do_compile'),
        ('do_configure', 'do_install'),
        ('do_configure', 'do_populate_sysroot'),
        ('do_configure', 'do_build'),
        ('do_configure', 'do_package'),
    ])
    def test_good_configure(self, id_, occurrence, pair):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(pair[0], pair[1]),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.task.order.do_compile'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('pair', [
        ('do_compile', 'do_install'),
        ('do_compile', 'do_populate_sysroot'),
        ('do_compile', 'do_build'),
        ('do_compile', 'do_install'),
        ('do_compile', 'do_package'),
    ])
    def test_good_compile(self, id_, occurrence, pair):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(pair[0], pair[1]),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.task.order.do_install'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('pair', [
        ('do_install', 'do_populate_sysroot'),
        ('do_install', 'do_build'),
        ('do_install', 'do_package'),
    ])
    def test_good_install(self, id_, occurrence, pair):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(pair[0], pair[1]),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.task.order.do_populate_sysroot'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('pair', [
        ('do_populate_sysroot', 'do_build'),
        ('do_populate_sysroot', 'do_package'),
    ])
    def test_good_populate_sysroot(self, id_, occurrence, pair):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(pair[0], pair[1]),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.task.order.do_build'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('pair', [
        ('do_build', 'do_package'),
    ])
    def test_good_build(self, id_, occurrence, pair):
        input_ = {
            'oelint_adv_test.bb': self.__generate_sample_code(pair[0], pair[1]),
        }
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.task.order.do_build'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.bb':
                                     '''
                                     do_build() {
                                         :
                                     }
                                     do_package() {
                                         :
                                     }
                                     ''',
                                 },
                             ],
                             )
    def test_good_pattern(self, input_, id_, occurrence):
        self.check_for_id(self._create_args(input_), id_, occurrence)

    @pytest.mark.parametrize('id_', ['oelint.task.order.do_build'])
    @pytest.mark.parametrize('occurrence', [0])
    @pytest.mark.parametrize('input_',
                             [
                                 {
                                     'oelint_adv_test.inc':
                                     '''
                                     do_populate_sysroot() {
                                         :
                                     }
                                     do_package() {
                                         :
                                     }
                                     ''',
                                     'oelint_adv_test.bb':
                                     '''
                                     require oelint_adv_test.inc
                                     do_build() {
                                         :
                                     }
                                     ''',
                                 },
                             ],
                             )
    def test_single_file_scope(self, id_, occurrence, input_):
        self.check_for_id(self._create_args(input_), id_, occurrence)
