import os
import shutil
import tempfile

from .base import TestBaseClass


# flake8: noqa S101 - n.a. for test files
class TestClassOelintLayerPath(TestBaseClass):
    """Cross-layer require resolution via the opt-in --layer-path flag.

    A require in one layer can point at an include shipped by a sister layer
    (as u-boot-fslc does in meta-freescale). bitbake resolves that against
    BBPATH; oelint only searches the containing layer, so it reports a false
    oelint.file.requirenotfound. --layer-path mirrors BBPATH to fix this.
    """

    def _make_layer_root(self, name):
        _root = os.path.join(tempfile.mkdtemp(), name)
        os.makedirs(os.path.join(_root, 'conf'), exist_ok=True)
        with open(os.path.join(_root, 'conf', 'layer.conf'), 'w') as o:
            o.write('# test layer\n')
        self._extra_roots = getattr(self, '_extra_roots', [])
        self._extra_roots.append(_root)
        return _root

    def _write(self, _root, relpath, content):
        _path = os.path.join(_root, relpath)
        os.makedirs(os.path.dirname(_path), exist_ok=True)
        with open(_path, 'w') as o:
            o.write(content)
        return _path

    def teardown_method(self):
        super().teardown_method()
        for _root in getattr(self, '_extra_roots', []):
            shutil.rmtree(os.path.dirname(_root), ignore_errors=True)

    def _consumer_recipe(self, require_line):
        _consumer = self._make_layer_root('meta-consumer')
        _recipe = self._write(
            _consumer, 'recipes-foo/foo/foo_2025.01.bb',
            'SUMMARY = "t"\nLICENSE = "MIT"\n{req}\n'.format(req=require_line))
        return _consumer, _recipe

    def _count_id(self, args, id_):
        from oelint_adv.__main__ import run
        _issues, _ = run(args)
        return len([x[1] for x in _issues if ':{id}:'.format(id=id_) in x[1]])

    def test_bad_without_layer_path(self):
        # include lives only in the sister layer -> not found without --layer-path
        _consumer, _recipe = self._consumer_recipe(
            'require recipes-foo/foo/foo-common.inc')
        _provider = self._make_layer_root('meta-provider')
        self._write(_provider, 'recipes-foo/foo/foo-common.inc', 'VAR = "a"\n')

        args = self._create_args_plain([_recipe])
        assert self._count_id(args, 'oelint.file.requirenotfound') == 1

    def test_good_with_layer_path(self):
        # --layer-path at the provider layer resolves the include
        _consumer, _recipe = self._consumer_recipe(
            'require recipes-foo/foo/foo-common.inc')
        _provider = self._make_layer_root('meta-provider')
        self._write(_provider, 'recipes-foo/foo/foo-common.inc', 'VAR = "a"\n')

        args = self._create_args_plain(
            [_recipe], extraopts=['--layer-path={r}'.format(r=_provider)])
        assert self._count_id(args, 'oelint.file.requirenotfound') == 0

    def test_good_with_layer_path_pv_from_filename(self):
        # ${PV} in the include name resolves to the filename version (2025.01),
        # not the assigned PV -- needs for_include semantics to find the file.
        _consumer, _recipe = self._consumer_recipe(
            'require recipes-foo/foo/foo-common_${PV}.inc\n'
            'PV = "2025.01+fslc+git${SRCPV}"')
        _provider = self._make_layer_root('meta-provider')
        self._write(_provider, 'recipes-foo/foo/foo-common_2025.01.inc',
                    'VAR = "a"\n')

        args = self._create_args_plain(
            [_recipe], extraopts=['--layer-path={r}'.format(r=_provider)])
        assert self._count_id(args, 'oelint.file.requirenotfound') == 0

    def test_lib_arguments_layer_path(self):
        # library entry point threads layer_path through like the CLI flag
        from oelint_adv.core import create_lib_arguments
        from oelint_adv.__main__ import run

        _consumer, _recipe = self._consumer_recipe(
            'require recipes-foo/foo/foo-common.inc')
        _provider = self._make_layer_root('meta-provider')
        self._write(_provider, 'recipes-foo/foo/foo-common.inc', 'VAR = "a"\n')

        args = create_lib_arguments([_recipe], quiet=True, jobs=1,
                                    layer_path=[_provider])
        _issues, _ = run(args)
        issues = [x[1] for x in _issues]
        assert not any(':oelint.file.requirenotfound:' in x for x in issues)
