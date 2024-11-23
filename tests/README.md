# Testing oelint-adv

## Installing test dependencies

```shell
pip3 install -r requirements-dev.txt
```

`oelint-adv` tests are built around `pytest`. Running `pytest` will execute all available tests.
Note, that test fail when coverage drops below 100 %.

## Adding a new test

Every test is organized in test classes derived from ``TestBaseClass``

```python

from .base import TestBaseClass

class TestClassMyNewTests(TestBaseClass):
    ...
```

now functions prefixed with ``test_`` can be added to this class

```python

from .base import TestBaseClass

class TestClassMyNewTests(TestBaseClass):
    
    def test_mynewtest(self):
        ...
```

### TestBaseClass

#### Creating CLI arguments

to create the CLI arguments for ``oelint-adv`` use

```python
self._create_args(input_)
```

``_input`` is a dictionary of filenames and content.

The ``_create_args`` function will then create temporary files with said content.

Optional arguments can be passed as a list of strings using

```python
self._create_args(input_, ['my', 'extra', 'arguments'])
```

#### Checking for a finding

To check if a finding was found ``check_for_id`` can be used

```python
self.check_for_id(arguments, id_to_check_for, number_of_occurrences)
```

e.g.

```python
self.check_for_id(self._create_args(input_), 'oelint.exportfunction.dash', 1)
```

checks the input an tests if the provided input file(s) produce exactly one report of
``oelint.exportfunction.dash``

#### Test automatic fixing

To test if automated fixing is working ``fix_and_check`` can be used

e.g.

```python
self.fix_and_check(self._create_args(input_), 'oelint.exportfunction.dash')
```

test if after automatic fixing exactly no reports of ``oelint.exportfunction.dash`` are found

### Using pytest.parametrize

to test different variation of inputs, ``pytest.parametrize`` is used widely

e.g.

```python
@pytest.mark.parametrize('id_', ['oelint.file.includenotfound'])
@pytest.mark.parametrize('occurrence', [1])
@pytest.mark.parametrize('input_',
                            [
                                {
                                    'oelint_adv_test.bb': 'include oelint_adv_test.inc',
                                },
                                {
                                    'oelint_adv_test.bb': 'include oelint_adv_test2.inc',
                                },
                            ],
                            )
def test_bad(self, input_, id_, occurrence):
    self.check_for_id(self._create_args(input_), id_, occurrence)
```

would run the check for all instances of inputs found in ``@pytest.mark.parametrize('input_'``.

This can be used to reduce the amount of test functions written.
Pytest will automatically generate instance for all permutations of configured inputs.
