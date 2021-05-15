import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

# -- known order --
# "do_fetch",
# "do_unpack",
# "do_patch",
# "do_configure",
# "do_compile",
# "do_install",
# "do_populate_sysroot",
# "do_build",
# "do_package"

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

    @pytest.mark.parametrize('id', ['oelint.task.order.do_fetch'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('pair', [
        ("do_unpack", "do_fetch"),
        ("do_patch", "do_fetch"),
        ("do_configure", "do_fetch"),
        ("do_compile", "do_fetch"),
        ("do_install", "do_fetch"),
        ("do_populate_sysroot", "do_fetch"),
        ("do_build", "do_fetch"),
        ("do_package", "do_fetch"),
    ])
    def test_bad_fetch(self, id, occurance, pair):
        input = {
            'oelint_adv_test.bb': self.__generate_sample_code(pair[0], pair[1])
        }
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.task.order.do_unpack'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('pair', [
        ("do_patch", "do_unpack"),
        ("do_configure", "do_unpack"),
        ("do_compile", "do_unpack"),
        ("do_install", "do_unpack"),
        ("do_populate_sysroot", "do_unpack"),
        ("do_build", "do_unpack"),
        ("do_package", "do_unpack"),
    ])
    def test_bad_unpack(self, id, occurance, pair):
        input = {
            'oelint_adv_test.bb': self.__generate_sample_code(pair[0], pair[1])
        }
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.task.order.do_patch'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('pair', [
        ("do_configure", "do_patch"),
        ("do_compile", "do_patch"),
        ("do_install", "do_patch"),
        ("do_populate_sysroot", "do_patch"),
        ("do_build", "do_patch"),
        ("do_package", "do_patch"),
    ])
    def test_bad_patch(self, id, occurance, pair):
        input = {
            'oelint_adv_test.bb': self.__generate_sample_code(pair[0], pair[1])
        }
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.task.order.do_configure'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('pair', [
        ("do_compile", "do_configure"),
        ("do_install", "do_configure"),
        ("do_populate_sysroot", "do_configure"),
        ("do_build", "do_configure"),
        ("do_package", "do_configure"),
    ])
    def test_bad_configure(self, id, occurance, pair):
        input = {
            'oelint_adv_test.bb': self.__generate_sample_code(pair[0], pair[1])
        }
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.task.order.do_compile'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('pair', [
        ("do_install", "do_compile"),
        ("do_populate_sysroot", "do_compile"),
        ("do_build", "do_compile"),
        ("do_install", "do_compile"),
        ("do_package", "do_compile"),
    ])
    def test_bad_compile(self, id, occurance, pair):
        input = {
            'oelint_adv_test.bb': self.__generate_sample_code(pair[0], pair[1])
        }
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.task.order.do_install'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('pair', [
        ("do_populate_sysroot", "do_install"),
        ("do_build", "do_install"),
        ("do_package", "do_install"),
    ])
    def test_bad_install(self, id, occurance, pair):
        input = {
            'oelint_adv_test.bb': self.__generate_sample_code(pair[0], pair[1])
        }
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.task.order.do_populate_sysroot'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('pair', [
        ("do_build", "do_populate_sysroot"),
        ("do_package", "do_populate_sysroot"),
    ])
    def test_bad_populate_sysroot(self, id, occurance, pair):
        input = {
            'oelint_adv_test.bb': self.__generate_sample_code(pair[0], pair[1])
        }
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.task.order.do_build'])
    @pytest.mark.parametrize('occurance', [1])
    @pytest.mark.parametrize('pair', [
        ("do_package", "do_build"),
    ])
    def test_bad_build(self, id, occurance, pair):
        input = {
            'oelint_adv_test.bb': self.__generate_sample_code(pair[0], pair[1])
        }
        self.check_for_id(self._create_args(input), id, occurance)

####

    @pytest.mark.parametrize('id', ['oelint.task.order.do_fetch'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('pair', [
        ("do_fetch", "do_unpack"),
        ("do_fetch", "do_patch"),
        ("do_fetch", "do_configure"),
        ("do_fetch", "do_compile"),
        ("do_fetch", "do_install"),
        ("do_fetch", "do_populate_sysroot"),
        ("do_fetch", "do_build"),
        ("do_fetch", "do_package"),
    ])
    def test_good_fetch(self, id, occurance, pair):
        input = {
            'oelint_adv_test.bb': self.__generate_sample_code(pair[0], pair[1])
        }
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.task.order.do_unpack'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('pair', [
        ("do_unpack", "do_patch"),
        ("do_unpack", "do_configure"),
        ("do_unpack", "do_compile"),
        ("do_unpack", "do_install"),
        ("do_unpack", "do_populate_sysroot"),
        ("do_unpack", "do_build"),
        ("do_unpack", "do_package"),
    ])
    def test_good_unpack(self, id, occurance, pair):
        input = {
            'oelint_adv_test.bb': self.__generate_sample_code(pair[0], pair[1])
        }
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.task.order.do_patch'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('pair', [
        ("do_patch", "do_configure"),
        ("do_patch", "do_compile"),
        ("do_patch", "do_install"),
        ("do_patch", "do_populate_sysroot"),
        ("do_patch", "do_build"),
        ("do_patch", "do_package"),
    ])
    def test_good_patch(self, id, occurance, pair):
        input = {
            'oelint_adv_test.bb': self.__generate_sample_code(pair[0], pair[1])
        }
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.task.order.do_configure'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('pair', [
        ("do_configure", "do_compile"),
        ("do_configure", "do_install"),
        ("do_configure", "do_populate_sysroot"),
        ("do_configure", "do_build"),
        ("do_configure", "do_package"),
    ])
    def test_good_configure(self, id, occurance, pair):
        input = {
            'oelint_adv_test.bb': self.__generate_sample_code(pair[0], pair[1])
        }
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.task.order.do_compile'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('pair', [
        ("do_compile", "do_install"),
        ("do_compile", "do_populate_sysroot"),
        ("do_compile", "do_build"),
        ("do_compile", "do_install"),
        ("do_compile", "do_package"),
    ])
    def test_good_compile(self, id, occurance, pair):
        input = {
            'oelint_adv_test.bb': self.__generate_sample_code(pair[0], pair[1])
        }
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.task.order.do_install'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('pair', [
        ("do_install", "do_populate_sysroot"),
        ("do_install", "do_build"),
        ("do_install", "do_package"),
    ])
    def test_good_install(self, id, occurance, pair):
        input = {
            'oelint_adv_test.bb': self.__generate_sample_code(pair[0], pair[1])
        }
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.task.order.do_populate_sysroot'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('pair', [
        ("do_populate_sysroot", "do_build"),
        ("do_populate_sysroot", "do_package"),
    ])
    def test_good_populate_sysroot(self, id, occurance, pair):
        input = {
            'oelint_adv_test.bb': self.__generate_sample_code(pair[0], pair[1])
        }
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.task.order.do_build'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('pair', [
        ("do_build", "do_package"),
    ])
    def test_good_build(self, id, occurance, pair):
        input = {
            'oelint_adv_test.bb': self.__generate_sample_code(pair[0], pair[1])
        }
        self.check_for_id(self._create_args(input), id, occurance)

    @pytest.mark.parametrize('id', ['oelint.task.order.do_build'])
    @pytest.mark.parametrize('occurance', [0])
    @pytest.mark.parametrize('input', 
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
            '''
            },
        ],
    )
    def test_good_pattern(self, input, id, occurance):
        self.check_for_id(self._create_args(input), id, occurance)