from typing import List, Tuple

from oelint_parser.cls_stash import Stash

from oelint_adv.cls_rule import Rule


class CustomTestRule(Rule):
    def __init__(self) -> None:
        super().__init__(id='test.rule.magic',
                         severity='error',
                         message='This is a test rule')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        return [self.finding(_file, 1)]


class CustomTestRuleValidTill(Rule):
    def __init__(self) -> None:
        super().__init__(id='test.rule.magic.validtill_sumo',
                         severity='error',
                         message='This is a test rule',
                         valid_till_release='sumo')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        return [self.finding(_file, 1)]


class CustomTestRuleValidFrom(Rule):
    def __init__(self) -> None:
        super().__init__(id='test.rule.magic.validfrom_kirkstone',
                         severity='error',
                         message='This is a test rule',
                         valid_from_release='kirkstone')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        return [self.finding(_file, 1)]


class CustomTestRuleValidTillFrom(Rule):
    def __init__(self) -> None:
        super().__init__(id='test.rule.magic.validtill_kirkstone_from_thud',
                         severity='error',
                         message='This is a test rule',
                         valid_till_release='kirkstone',
                         valid_from_release='thud')

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        return [self.finding(_file, 1)]


class CustomTestRuleReleaseSpecAppendix(Rule):
    def __init__(self) -> None:
        super().__init__(id='test.rule.magic.specappendix',
                         severity='error',
                         message='This is a test rule',
                         appendix=['A', 'B'])

    def check(self, _file: str, stash: Stash) -> List[Tuple[str, int, str]]:
        return [self.finding(_file, 1)]

    def check_release_range(self, release_range: List[str]) -> bool:
        if 'kirkstone' in release_range:
            self.Appendix.append('kirkstone')
        return super().check_release_range(release_range)
