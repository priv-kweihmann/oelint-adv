import argparse
import json
import os
from argparse import ArgumentTypeError

import pytest  # noqa: I900

from .base import TestBaseClass


# flake8: noqa S101 - n.a. for test files
class TestClassCustomRules(TestBaseClass):

    CUSTOM_RULES_DIR = os.path.join(os.path.dirname(__file__), 'customrules')

    def test_custom_rules_loading(self, capsys):
        from oelint_adv.__main__ import print_rulefile

        _args = self._create_args(
            {}, extraopts=[f'--customrules={TestClassCustomRules.CUSTOM_RULES_DIR}', '--print-rulefile'])
        print_rulefile(_args)

        out = json.loads(capsys.readouterr().out)

        assert 'test.rule.magic' in out

    def test_custom_rules_till(self, capsys):
        from oelint_adv.__main__ import print_rulefile

        _args = self._create_args(
            {}, extraopts=[
                '--release=rocko',
                f'--customrules={TestClassCustomRules.CUSTOM_RULES_DIR}',
                '--print-rulefile']
        )
        print_rulefile(_args)

        out = json.loads(capsys.readouterr().out)

        assert 'test.rule.magic.validtill_sumo' in out

    def test_custom_rules_till_na(self, capsys):
        from oelint_adv.__main__ import print_rulefile

        _args = self._create_args(
            {}, extraopts=[
                '--release=kirkstone',
                f'--customrules={TestClassCustomRules.CUSTOM_RULES_DIR}',
                '--print-rulefile']
        )
        print_rulefile(_args)

        out = json.loads(capsys.readouterr().out)

        assert 'test.rule.magic.validtill_sumo' not in out

    def test_custom_rules_from(self, capsys):
        from oelint_adv.__main__ import print_rulefile

        _args = self._create_args(
            {}, extraopts=[
                '--release=sumo',
                f'--customrules={TestClassCustomRules.CUSTOM_RULES_DIR}',
                '--print-rulefile']
        )
        print_rulefile(_args)

        out = json.loads(capsys.readouterr().out)

        assert 'test.rule.magic.validfrom_kirkstone' not in out

    def test_custom_rules_from_na(self, capsys):
        from oelint_adv.__main__ import print_rulefile

        _args = self._create_args(
            {}, extraopts=[
                '--release=kirkstone',
                f'--customrules={TestClassCustomRules.CUSTOM_RULES_DIR}',
                '--print-rulefile']
        )
        print_rulefile(_args)

        out = json.loads(capsys.readouterr().out)

        assert 'test.rule.magic.validfrom_kirkstone' in out

    def test_custom_rules_range(self, capsys):
        from oelint_adv.__main__ import print_rulefile

        _args = self._create_args(
            {}, extraopts=[
                '--release=dunfell',
                f'--customrules={TestClassCustomRules.CUSTOM_RULES_DIR}',
                '--print-rulefile']
        )
        print_rulefile(_args)

        out = json.loads(capsys.readouterr().out)

        assert 'test.rule.magic.validtill_kirkstone_from_thud' in out

    def test_custom_rules_range_na_1(self, capsys):
        from oelint_adv.__main__ import print_rulefile

        _args = self._create_args(
            {}, extraopts=[
                '--release=mickledore',
                f'--customrules={TestClassCustomRules.CUSTOM_RULES_DIR}',
                '--print-rulefile']
        )
        print_rulefile(_args)

        out = json.loads(capsys.readouterr().out)

        assert 'test.rule.magic.validtill_kirkstone_from_thud' not in out

    def test_custom_rules_range_na_2(self, capsys):
        from oelint_adv.__main__ import print_rulefile

        _args = self._create_args(
            {}, extraopts=[
                '--release=sumo',
                f'--customrules={TestClassCustomRules.CUSTOM_RULES_DIR}',
                '--print-rulefile']
        )
        print_rulefile(_args)

        out = json.loads(capsys.readouterr().out)

        assert 'test.rule.magic.validtill_kirkstone_from_thud' not in out

    def test_custom_rules_appendix(self, capsys):
        from oelint_adv.__main__ import print_rulefile

        _args = self._create_args(
            {}, extraopts=[
                '--release=dunfell',
                f'--customrules={TestClassCustomRules.CUSTOM_RULES_DIR}',
                '--print-rulefile']
        )
        print_rulefile(_args)

        out = json.loads(capsys.readouterr().out)

        assert 'test.rule.magic.specappendix.A' in out
        assert 'test.rule.magic.specappendix.B' in out

    def test_custom_rules_appendix_kirkstone(self, capsys):
        from oelint_adv.__main__ import print_rulefile

        _args = self._create_args(
            {}, extraopts=[
                '--release=kirkstone',
                f'--customrules={TestClassCustomRules.CUSTOM_RULES_DIR}',
                '--print-rulefile']
        )
        print_rulefile(_args)

        out = json.loads(capsys.readouterr().out)

        assert 'test.rule.magic.specappendix.A' in out
        assert 'test.rule.magic.specappendix.B' in out
        assert 'test.rule.magic.specappendix.kirkstone' in out
