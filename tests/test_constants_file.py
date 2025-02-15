import os

import pytest  # noqa: I900

from .base import TestBaseClass

# flake8: noqa S101 - n.a. for test files


class TestConstantFile(TestBaseClass):

    THISDIR = os.path.dirname(__file__)
    RECIPE_DISTRO_IMPORTS = os.path.join(THISDIR, "testlayer/recipes/test_known_distro_imports.bb")
    RECIPE_DISTRO = os.path.join(THISDIR, "testlayer/recipes/test_known_distro.bb")
    RECIPE_MACHINE_IMPORTS = os.path.join(THISDIR, "testlayer/recipes/test_known_machine_imports.bb")
    RECIPE_MACHINE = os.path.join(THISDIR, "testlayer/recipes/test_known_machine.bb")
    RECIPE_VARIABLE_IMPORTS = os.path.join(THISDIR, "testlayer/recipes/test_known_vars_imports.bb")
    RECIPE_VARIABLE = os.path.join(THISDIR, "testlayer/recipes/test_known_vars.bb")

    def test_distro_imports_default_file(self):
        # Test the default
        _args = self._create_args_existing_file(TestConstantFile.RECIPE_DISTRO_IMPORTS, 
                                  ['--release=scarthgap'])

        self.check_for_id(_args, 'oelint.vars.specific', 0)

    def test_distro_default_file(self):
        # Test the default
        _args = self._create_args_existing_file(TestConstantFile.RECIPE_DISTRO, 
                                  ['--release=scarthgap'])

        self.check_for_id(_args, 'oelint.vars.specific', 0)
    
    def test_machine_imports_default_file(self):
        # Test the default
        _args = self._create_args_existing_file(TestConstantFile.RECIPE_MACHINE_IMPORTS, 
                                  ['--release=scarthgap'])

        self.check_for_id(_args, 'oelint.vars.specific', 0)

    def test_machine_default_file(self):
        # Test the default
        _args = self._create_args_existing_file(TestConstantFile.RECIPE_MACHINE, 
                                  ['--release=scarthgap'])

        self.check_for_id(_args, 'oelint.vars.specific', 0)

    def test_variable_imports_default_file(self):
        # Test the default
        _args = self._create_args_existing_file(TestConstantFile.RECIPE_VARIABLE_IMPORTS, 
                                  ['--release=scarthgap'])

        self.check_for_id(_args, 'oelint.vars.mispell.unknown', 0)

    def test_variable_default_file(self):
        # Test the default
        _args = self._create_args_existing_file(TestConstantFile.RECIPE_VARIABLE, 
                                  ['--release=scarthgap'])

        self.check_for_id(_args, 'oelint.vars.mispell.unknown', 0)

    def test_distro_imports_specific_file(self):
        # Test the default
        _args = self._create_args_existing_file(TestConstantFile.RECIPE_DISTRO_IMPORTS, 
                                  ['--release=styhead'])

        self.check_for_id(_args, 'oelint.vars.specific', 1)

    
    def test_machine_imports_specific_file(self):
        # Test the default
        _args = self._create_args_existing_file(TestConstantFile.RECIPE_MACHINE_IMPORTS, 
                                  ['--release=styhead'])

        self.check_for_id(_args, 'oelint.vars.specific', 1)

    def test_variable_imports_specific_file(self):
        # Test the default
        _args = self._create_args_existing_file(TestConstantFile.RECIPE_VARIABLE_IMPORTS, 
                                  ['--release=styhead'])

        self.check_for_id(_args, 'oelint.vars.mispell.unknown', 1)