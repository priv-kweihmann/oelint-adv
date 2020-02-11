# oelint-adv

![Build status](https://github.com/priv-kweihmann/oelint-adv/workflows/Python%20package/badge.svg)
[![PyPI version](https://badge.fury.io/py/oelint_adv.svg)](https://badge.fury.io/py/oelint_adv)
[![Python version](https://img.shields.io/pypi/pyversions/oelint_adv)](https://img.shields.io/pypi/pyversions/oelint_adv)
[![Downloads](https://img.shields.io/pypi/dm/oelint_adv)](https://img.shields.io/pypi/dm/oelint_adv)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/priv-kweihmann/oelint-adv.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/priv-kweihmann/oelint-adv/context:python)

Advanced oelint

## Purpose

Based on the [OpenEmbedded Styleguide](https://www.openembedded.org/wiki/Styleguide) and work done by [oe-stylize-tool](https://github.com/openembedded/meta-openembedded/blob/master/contrib/oe-stylize.py) this module offers a (nearly) complete linter for bitbake-recipes.

The tool does handle includes/requires automatically so you don't have to pass them via CLI.

**NOTE**: .bbappend-files have to be passed via CLI - these are NOT gathered automatically

## Install

With pip

```shell
pip3 install oelint_adv
```

From Arch Linux:

```shell
yay -S oelint-adv
```

## Usage

```shell
oelint-adv
usage: __main__.py [-h] [--suppress SUPPRESS] [--output OUTPUT] [--fix]
                   [--nobackup] [--addrules ADDRULES [ADDRULES ...]]
                   [--rulefile RULEFILE]
                   files [files ...]

Advanced OELint - Check bitbake recipes against OECore styleguide

positional arguments:
  files                 File to parse

optional arguments:
  -h, --help            show this help message and exit
  --suppress SUPPRESS   Rules to suppress
  --output OUTPUT       Where to flush the findings (default: stderr)
  --fix                 Automatically try to fix the issues
  --nobackup            Don't create backup file when auto fixing
  --addrules ADDRULES [ADDRULES ...]
                        Additional non-default rulessets to add
  --rulefile RULEFILE   Rulefile
  --color               Add color to the output based on the severity
```

## Output

Will be [file]:[line]:[severity]:[message].

Example:

```shell
/disk/meta-some/cppcheck-native/cppcheck.inc:26:error:oelint.task.nomkdir:'mkdir' shall not be used in do_install. Use 'install'
/disk/meta-some/cppcheck-native/cppcheck-native_1.87.bb:0:error:oelint.var.mandatoryvar:Variable 'SECTION' should be set
/disk/meta-some/cppcheck-native/cppcheck.inc:1:warning:oelint.vars.summary80chars:'SUMMARY' should not be longer than 80 characters
/disk/meta-some/cppcheck-native/cppcheck.inc:4:warning:oelint.vars.homepageprefix:'HOMEPAGE' should start with 'http://' or 'https://'
/disk/meta-some/cppcheck-native/cppcheck.inc:28:warning:oelint.spaces.lineend:Line shall not end with a space
/disk/meta-some/cppcheck-native/cppcheck-native_1.87.bb:0:error:oelint.var.mandatoryvar:Variable 'AUTHOR' should be set
/disk/meta-some/cppcheck-native/cppcheck.inc:26:error:oelint.task.nocopy:'cp' shall not be used in do_install. Use 'install'
/disk/meta-some/cppcheck-native/cppcheck.inc:12:warning:oelint.var.order:'DEPENDS' should be placed before 'inherit'
```

## Apply automatic fixing

Some of the rules are capable of fixing the issues found automatically.
This will be done if you pass **--fix** as a startup parameter.

As long as you don't pass **--nobackup** a backup copy (filename + .bak) will be created for all files fixed.

## Available rules

Rules marked with **[F]** are able to perform automatic fixing

* oelint.comments.notrailing - No trailing comments allowed, comments should be on a single line
* oelint.file.includenotfound - File to be included not found
* oelint.file.patchsignedoff - Patches should contain a Signed-Of-By entry
* oelint.file.requireinclude - Require should be used instead of include
* oelint.file.requirenotfound - File to be required not found
* oelint.file.upstreamstatus - Patches should contain a Upstream-Status entry
* oelint.spaces.emptyline - Empty line should not contain spaces or tabs **[F]**
* oelint.spaces.linebeginning - No space at a line beginning **[F]**
* oelint.spaces.linecont - Safe line continuation **[F]**
* oelint.spaces.lineend - No spaces at line end **[F]**
* oelint.tabs.notabs - No tabs allowed **[F]**
* oelint.task.addnotaskbody - Task added by addtask cannot be found
* oelint.task.customorder - order of custom tasks added via addtask
* oelint.task.docstrings - Custom tasks should have docstrings
* oelint.task.multiappends - Multiple appends to the same function in the same file won't work in bitbake
* oelint.task.nocopy - No cp usage in do_install
* oelint.task.nomkdir - No mkdir usage in do_install
* oelint.task.nopythonprefix - Tasks containing shell code should NOT be prefixed with 'python' in function header
* oelint.task.order - Order of tasks
* oelint.task.pythonprefix - Tasks containing python code should be prefixed with 'python' in function header
* oelint.var.bbclassextend - Use BBCLASSEXTEND when possible
* oelint.var.improperinherit - Warn about improperly named inherits
* oelint.var.licenseremotefile - License shall be a file in remote source not a local file
* oelint.var.mandatoryvar - Check for mandatory variables
* oelint.var.multiinclude - Warn on including the same file more than once
* oelint.var.multiinherit - Warn on inherit the same file more than once
* oelint.var.nativefilename - Native only recipes should be named -native
* oelint.var.order - Variable order
* oelint.var.override - Check if include/append is overriding a variable
* oelint.var.suggestedvar - Notice on suggested variables
* oelint.vars.autorev - The usage of 'AUTOREV' for SRCREV leads to not reproducible builds
* oelint.vars.bugtrackerisurl - BUGTRACKER should be an URL
* oelint.vars.dependsappend - DEPENDS should only be appended, not overwritten
* oelint.vars.dependsordered - RDEPENDS entries should be ordered alphabetically
* oelint.vars.duplicate - No duplicates in DEPENDS and RDEPENDS
* oelint.vars.fileextrapaths - 'FILESEXTRAPATHS' shouldn't be used in a bb file
* oelint.vars.homepageprefix - HOMEPAGE should begin with https:// or http://
* oelint.vars.inconspaces - Inconsistent use of spaces on append operation
* oelint.vars.insaneskip - INSANE_SKIP should be avoided at any cost
* oelint.vars.mispell - Possible typo detected
* oelint.vars.multilineident - On a multiline assignment, line indent is desirable
* oelint.vars.pathhardcode - Warn about the usage of hardcoded paths
* oelint.vars.pnbpnusage - ${BPN} should be used instead of ${PN}
* oelint.vars.pnusagediscouraged - Variable shouldn't contain ${PN} or ${BPN}
* oelint.vars.sectionlowercase - SECTION should be lowercase only **[F]**
* oelint.vars.spacesassignment - ' = ' should be correct variable assignment
* oelint.vars.srcurioptions - Fetcher should only valid options
* oelint.vars.summary80chars - SUMMARY should max. be 80 characters long
* oelint.vars.summarylinebreaks - No line breaks in SUMMARY
* oelint.vars.valuequoted - Variable values should be properly quoted

### Non-default rulesets

To enable rulesets that are not part of the standard ruleset pass
**--addrules \<ruleset-name\>** to CLI.

These rules are sometimes contrary to OE-style-guide, so use them with caution

#### jetm ruleset

To enable pass **--addrules jetm** to CLI

Rules marked with **[F]** are able to perform automatic fixing

* oelint.jetm.vars.dependssingleline - Each [R]DEPENDS entry should be put into a single line

## Defining a ruleset

If you pass the option `--rulefile` you could define the rules to be checked and their severity via a simple json file.

The rule file could look like this

```json
{
  "<rule>": "<severity>"
}
```

to override the severity, or

```json
{
  "<rule>": ""
}
```

to keep the original severity.

### Example

```json
{
  "oelint.file.includenotfound": "",
  "oelint.file.requirenotfound": "warning"
}
```

would enable the two rules `oelint.file.includenotfound` and `oelint.file.requirenotfound`.
The severity of `oelint.file.includenotfound` will be the default of the tool, while `oelint.file.requirenotfound` will report `warning` instead of the original suggested severity
