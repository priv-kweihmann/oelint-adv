from .base import TestBaseClass

import os


# flake8: noqa S101 - n.a. for test files
class TestGrouping(TestBaseClass):

    def __flatten_file_names(self, list_):
        return [os.path.basename(x) for x in list_]

    def test_fast_bb_1(self):
        from oelint_adv.core import group_files

        input_ = {
            'test1.bb': '',
            'test2.bb': ''
        }

        args = self._create_args(input_)
        res = [self.__flatten_file_names(x[0]) for x in group_files(args.files, args.mode)]

        assert ['test1.bb'] in res
        assert ['test2.bb'] in res

    def test_fast_bb_bbappend(self):
        from oelint_adv.core import group_files

        input_ = {
            'test1.bb': '',
            'test1.bbappend': ''
        }

        args = self._create_args(input_)
        res = [self.__flatten_file_names(x[0]) for x in group_files(args.files, args.mode)]

        assert ['test1.bb', 'test1.bbappend'] in res

    def test_fast_bb_bbappend_version(self):
        from oelint_adv.core import group_files

        input_ = {
            'test1_1.0.bb': '',
            'test1_%.bbappend': ''
        }

        args = self._create_args(input_)
        res = [self.__flatten_file_names(x[0]) for x in group_files(args.files, args.mode)]

        assert ['test1_1.0.bb', 'test1_%.bbappend'] in res

    def test_fast_bb_bbappend_version_2(self):
        from oelint_adv.core import group_files

        input_ = {
            'test1_1.0.bb': '',
            'test1_1.%.bbappend': ''
        }

        args = self._create_args(input_)
        res = [self.__flatten_file_names(x[0]) for x in group_files(args.files, args.mode)]

        assert ['test1_1.0.bb', 'test1_1.%.bbappend'] in res

    def test_fast_bb_bbappend_lone(self):
        from oelint_adv.core import group_files

        input_ = {
            'test1_1.0.bb': '',
            'test1_2.%.bbappend': ''
        }

        args = self._create_args(input_)
        res = [self.__flatten_file_names(x[0]) for x in group_files(args.files, args.mode)]

        assert ['test1_1.0.bb'] in res
        assert ['test1_2.%.bbappend'] in res

    def test_fast_bb_bbappend_full_filename(self):
        from oelint_adv.core import group_files

        input_ = {
            'test1.bb': '',
            'test1-debug.bb': '',
            'test1.bbappend': '',
            'test1-debug.bbappend': '',
        }

        args = self._create_args(input_)
        res = [self.__flatten_file_names(x[0]) for x in group_files(args.files, args.mode)]

        assert ['test1.bb', 'test1.bbappend'] in res
        assert ['test1-debug.bb', 'test1-debug.bbappend'] in res

    def test_fast_layer_conf(self):
        from oelint_adv.core import group_files

        input_ = {
            'conf/layer.conf': '',
            'test1_1.0.bb': '',
            'test2_1.0.bb': ''
        }

        args = self._create_args(input_)
        res = [self.__flatten_file_names(x[0]) for x in group_files(args.files, args.mode)]

        assert ['layer.conf', 'test1_1.0.bb'] in res
        assert ['layer.conf', 'test2_1.0.bb'] in res
        assert ['layer.conf'] in res

    def test_all_layer_conf(self):
        from oelint_adv.core import group_files

        input_ = {
            'conf/layer.conf': '',
            'test1_1.0.bb': '',
            'test2_1.0.bb': ''
        }

        args = self._create_args(input_, ['--mode=all'])
        res = [self.__flatten_file_names(x[0]) for x in group_files(args.files, args.mode)]

        assert ['layer.conf', 'test1_1.0.bb'] in res
        assert ['layer.conf', 'test2_1.0.bb'] in res
        assert ['layer.conf'] in res

    def test_fast_distro_conf(self):
        from oelint_adv.core import group_files

        input_ = {
            'conf/distro/mydistro.conf': '',
            'test1_1.0.bb': '',
            'test2_1.0.bb': ''
        }

        args = self._create_args(input_)
        res = [self.__flatten_file_names(x[0]) for x in group_files(args.files, args.mode)]

        assert ['test1_1.0.bb'] in res
        assert ['test2_1.0.bb'] in res
        assert ['mydistro.conf'] not in res

    def test_all_distro_conf(self):
        from oelint_adv.core import group_files

        input_ = {
            'conf/distro/mydistro.conf': '',
            'test1_1.0.bb': '',
            'test2_1.0.bb': ''
        }

        args = self._create_args(input_, ['--mode=all'])
        res = [self.__flatten_file_names(x[0]) for x in group_files(args.files, args.mode)]

        assert ['mydistro.conf', 'test1_1.0.bb'] in res
        assert ['mydistro.conf', 'test2_1.0.bb'] in res
        assert ['mydistro.conf'] in res

    def test_fast_machine_conf(self):
        from oelint_adv.core import group_files

        input_ = {
            'conf/machine/mymachine.conf': '',
            'test1_1.0.bb': '',
            'test2_1.0.bb': ''
        }

        args = self._create_args(input_)
        res = [self.__flatten_file_names(x[0]) for x in group_files(args.files, args.mode)]

        assert ['test1_1.0.bb'] in res
        assert ['test2_1.0.bb'] in res
        assert ['mymachine.conf'] not in res

    def test_all_machine_conf(self):
        from oelint_adv.core import group_files

        input_ = {
            'conf/machine/mymachine.conf': '',
            'test1_1.0.bb': '',
            'test2_1.0.bb': ''
        }

        args = self._create_args(input_, ['--mode=all'])
        res = [self.__flatten_file_names(x[0]) for x in group_files(args.files, args.mode)]

        assert ['mymachine.conf', 'test1_1.0.bb'] in res
        assert ['mymachine.conf', 'test2_1.0.bb'] in res
        assert ['mymachine.conf'] in res

    def test_fast_full_setup(self):
        from oelint_adv.core import group_files

        input_ = {
            'conf/distro/mydistro.conf': '',
            'conf/machine/mymachine.conf': '',
            'test1_1.0.bb': '',
            'test2_1.0.bb': '',
            'conf/layer.conf': '',
        }

        args = self._create_args(input_)
        res = [self.__flatten_file_names(x[0]) for x in group_files(args.files, args.mode)]

        assert ['layer.conf', 'test1_1.0.bb'] in res
        assert ['layer.conf', 'test2_1.0.bb'] in res
        assert ['layer.conf'] in res
        assert ['mymachine.conf'] not in res
        assert ['mydistro.conf'] not in res

    def test_all_full_setup(self):
        from oelint_adv.core import group_files

        input_ = {
            'conf/distro/mydistro.conf': '',
            'conf/machine/mymachine.conf': '',
            'test1_1.0.bb': '',
            'test2_1.0.bb': '',
            'conf/layer.conf': '',
        }

        args = self._create_args(input_, ['--mode=all'])
        res = [self.__flatten_file_names(x[0]) for x in group_files(args.files, args.mode)]

        assert ['layer.conf', 'mymachine.conf', 'mydistro.conf', 'test1_1.0.bb'] in res
        assert ['layer.conf', 'mymachine.conf', 'mydistro.conf', 'test2_1.0.bb'] in res
        assert ['layer.conf'] in res
        assert ['mymachine.conf'] in res
        assert ['mydistro.conf'] in res

    def test_all_full_setup_multiple(self):
        from oelint_adv.core import group_files

        input_ = {
            'conf/distro/mydistro.conf': '',
            'conf/machine/mymachine.conf': '',
            'test1_1.0.bb': '',
            'conf/distro/mydistro2.conf': '',
            'conf/machine/mymachine2.conf': '',
            'test2_1.0.bb': '',
            'conf/layer.conf': '',
        }

        args = self._create_args(input_, ['--mode=all'])
        res = [self.__flatten_file_names(x[0]) for x in group_files(args.files, args.mode)]

        assert ['layer.conf', 'mymachine.conf', 'mydistro.conf', 'test1_1.0.bb'] in res
        assert ['layer.conf', 'mymachine2.conf', 'mydistro.conf', 'test1_1.0.bb'] in res
        assert ['layer.conf', 'mymachine.conf', 'mydistro2.conf', 'test1_1.0.bb'] in res
        assert ['layer.conf', 'mymachine2.conf', 'mydistro2.conf', 'test1_1.0.bb'] in res
        assert ['layer.conf', 'mymachine.conf', 'mydistro.conf', 'test2_1.0.bb'] in res
        assert ['layer.conf', 'mymachine2.conf', 'mydistro.conf', 'test2_1.0.bb'] in res
        assert ['layer.conf', 'mymachine.conf', 'mydistro2.conf', 'test2_1.0.bb'] in res
        assert ['layer.conf', 'mymachine2.conf', 'mydistro2.conf', 'test2_1.0.bb'] in res
        assert ['layer.conf'] in res
        assert ['mymachine.conf'] in res
        assert ['mymachine2.conf'] in res
        assert ['mydistro.conf'] in res
        assert ['mydistro2.conf'] in res
