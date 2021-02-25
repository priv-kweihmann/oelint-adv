# oelint-adv

![Build status](https://github.com/priv-kweihmann/oelint-adv/workflows/Python%20package/badge.svg)
[![PyPI version](https://badge.fury.io/py/oelint-adv.svg)](https://badge.fury.io/py/oelint-adv)
[![Python version](https://img.shields.io/pypi/pyversions/oelint-adv)](https://img.shields.io/pypi/pyversions/oelint-adv)
[![Downloads](https://img.shields.io/pypi/dm/oelint-adv)](https://img.shields.io/pypi/dm/oelint-adv)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/priv-kweihmann/oelint-adv.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/priv-kweihmann/oelint-adv/context:python)

Advanced oelint

## Purpose

Based on the [OpenEmbedded Styleguide](https://www.openembedded.org/wiki/Styleguide) and work done by [oe-stylize-tool](https://github.com/openembedded/meta-openembedded/blob/master/contrib/oe-stylize.py) this module offers a (nearly) complete linter for bitbake-recipes.

The tool should help anyone working with YOCTO/OpenEmbedded to write more clean, less 'magical' recipes, without the need to know all the internals of your used poky/OpenEmbedded version.

It could also be used as part of a CI to avoid hard to debug issues slipping to your code base - be sure to checkout [rulefile](#defining-a-ruleset) for that use case.

As every linter this tool is sometimes extra picky, but for the good of it, not just to bug people.
Especially for novice users it might be a help to avoid the most common pitfalls of bitbake recipes.

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
                   [--customrules CUSTOMRULES [CUSTOMRULES ...]]
                   [--rulefile RULEFILE] [--constantfile CONSTANTFILE]
                   [--color]
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
  --customrules CUSTOMRULES [CUSTOMRULES ...]
                        Additional directories to parse for rulessets
  --rulefile RULEFILE   Rulefile
  --constantfile CONSTANTFILE
                        Constantfile
  --color               Add color to the output based on the severity
```

## Output

Will be [file]:[line]:[severity]:[message].

Example:

```shell
/disk/meta-some/cppcheck-native/cppcheck.inc:26:error:oelint.task.nomkdir:'mkdir' shall not be used in do_install. Use 'install'
/disk/meta-some/cppcheck-native/cppcheck-native_1.87.bb:0:error:oelint.var.mandatoryvar.SECTION:Variable 'SECTION' should be set
/disk/meta-some/cppcheck-native/cppcheck.inc:1:warning:oelint.vars.summary80chars:'SUMMARY' should not be longer than 80 characters
/disk/meta-some/cppcheck-native/cppcheck.inc:4:warning:oelint.vars.homepageprefix:'HOMEPAGE' should start with 'http://' or 'https://'
/disk/meta-some/cppcheck-native/cppcheck.inc:28:warning:oelint.spaces.lineend:Line shall not end with a space
/disk/meta-some/cppcheck-native/cppcheck-native_1.87.bb:0:error:oelint.var.mandatoryvar.AUTHOR:Variable 'AUTHOR' should be set
/disk/meta-some/cppcheck-native/cppcheck.inc:26:error:oelint.task.nocopy:'cp' shall not be used in do_install. Use 'install'
/disk/meta-some/cppcheck-native/cppcheck.inc:12:warning:oelint.var.order.DEPENDS:'DEPENDS' should be placed before 'inherit'
```

## Apply automatic fixing

Some of the rules are capable of fixing the issues found automatically.
This will be done if you pass **--fix** as a startup parameter.

As long as you don't pass **--nobackup** a backup copy (filename + .bak) will be created for all files fixed.

## Available rules

Rules marked with **[F]** are able to perform automatic fixing
Rules marked with **[S]** can have multiple sub-IDs

* oelint.append.protvars - Variables that shouldn't be set in a bbappend **[S]**
* oelint.file.includenotfound - File to be included not found
* oelint.file.nospaces - Path to file should not contain spaces
* oelint.file.patchsignedoff - Patches should contain a Signed-Of-By entry
* oelint.file.requireinclude - Require should be used instead of include
* oelint.file.requirenotfound - File to be required not found
* oelint.file.underscore - Checks the correct usage of underscores in filename
* oelint.file.upstreamstatus - Patches should contain a Upstream-Status entry
* oelint.func.specific - Function is specific to an unknown identifier
* oelint.newline.consecutive - Consecutive blank lines should be avoided **[F]**
* oelint.newline.eof - File shall end on a newline **[F]**
* oelint.spaces.emptyline - Empty line should not contain spaces or tabs **[F]**
* oelint.spaces.linebeginning - No space at a line beginning **[F]**
* oelint.spaces.linecont - Safe line continuation **[F]**
* oelint.spaces.lineend - No spaces at line end **[F]**
* oelint.tabs.notabs - No tabs allowed **[F]**
* oelint.task.addnotaskbody - Task added by addtask cannot be found
* oelint.task.customorder - order of custom tasks added via addtask
* oelint.task.docstrings - Custom tasks should have docstrings
* oelint.task.heredocs - Usage of heredocs should be avoided. Use files instead
* oelint.task.multifragments - Multiple fragments of the same function in the same file should be merged
* oelint.task.nocopy - No cp usage in do_install
* oelint.task.nomkdir - No mkdir usage in do_install
* oelint.task.nopythonprefix - Tasks containing shell code should NOT be prefixed with 'python' in function header
* oelint.task.order - Order of tasks **[S]**
* oelint.task.pythonprefix - Tasks containing python code should be prefixed with 'python' in function header
* oelint.var.bbclassextend - Use BBCLASSEXTEND when possible
* oelint.var.filesoverride - FILES_* variables should not be overriden
* oelint.var.improperinherit - Warn about improperly named inherits
* oelint.var.licenseremotefile - License shall be a file in remote source not a local file
* oelint.var.mandatoryvar - Check for mandatory variables **[S]**
* oelint.var.multiinclude - Warn on including the same file more than once
* oelint.var.multiinherit - Warn on inherit the same file more than once
* oelint.var.nativefilename - Native only recipes should be named -native
* oelint.var.order - Variable order **[S]**
* oelint.var.override - Check if include/append is overriding a variable
* oelint.var.rootfspostcmd - ROOTFS_POSTPROCESS_COMMAND should not have trailing blanks
* oelint.var.srcuriwildcard - 'SRC_URI' should not contain any wildcards
* oelint.var.suggestedvar - Notice on suggested variables **[S]**
* oelint.vars.appendop - Use '_append' instead of ' += '
* oelint.vars.autorev - The usage of 'AUTOREV' for SRCREV leads to not reproducible builds
* oelint.vars.bbvars - Variables that shouldn't be altered in recipe scope **[S]**
* oelint.vars.bugtrackerisurl - BUGTRACKER should be an URL
* oelint.vars.dependsappend - DEPENDS should only be appended, not overwritten
* oelint.vars.dependsordered - RDEPENDS entries should be ordered alphabetically
* oelint.vars.descriptionsame - 'DESCRIPTION' is the same a 'SUMMARY' - it can be removed then
* oelint.vars.descriptiontoobrief - 'DESCRIPTION' is the shorter than 'SUMMARY'
* oelint.vars.doublemodify - Multiple modifiers of append/prepend/remove/+= found in one operation
* oelint.vars.duplicate - No duplicates in DEPENDS and RDEPENDS
* oelint.vars.fileextrapaths - 'FILESEXTRAPATHS' shouldn't be used in a bb file
* oelint.vars.fileextrapathsop - 'FILESEXTRAPATHS' should only be used in combination with ' := '
* oelint.vars.filessetting - unnecessary FILES settings
* oelint.vars.homepageping - 'HOMEPAGE' isn't reachable
* oelint.vars.homepageprefix - HOMEPAGE should begin with https:// or http://
* oelint.vars.inconspaces - Inconsistent use of spaces on append operation
* oelint.vars.insaneskip - INSANE_SKIP should be avoided at any cost
* oelint.vars.licfileprefix - Unnecessary prefix to LIC_FILES_CHKSUM detected
* oelint.vars.listappend - Proper append/prepend to lists
* oelint.vars.mispell - Possible typo detected
* oelint.vars.multilineident - On a multiline assignment, line indent is desirable
* oelint.vars.notneededspace - Space at the beginning of the var is not needed **[F]**
* oelint.vars.notrailingslash - Variable shall not end on a slash
* oelint.vars.pathhardcode - Warn about the usage of hardcoded paths **[S]**
* oelint.vars.pbpusage - ${BP} should be used instead of ${P}
* oelint.vars.pkgspecific - Variable is package-specific, but isn't set in that way **[S]**
* oelint.vars.pnbpnusage - ${BPN} should be used instead of ${PN}
* oelint.vars.pnusagediscouraged - Variable shouldn't contain ${PN} or ${BPN}
* oelint.vars.sectionlowercase - SECTION should be lowercase only **[F]**
* oelint.vars.spacesassignment - ' = ' should be correct variable assignment
* oelint.vars.specific - Variable is specific to an unknown identifier
* oelint.vars.srcuriappend - Use SRC_URI_append otherwise this will override weak defaults by inherit
* oelint.vars.srcuridomains - Recipe is pulling from different domains, this will likely cause issues
* oelint.vars.srcurifile - First item of SRC_URI should not be a file:// fetcher, if multiple fetcher are used
* oelint.vars.srcurigittag - 'tag' in SRC_URI-options leads to not-reproducible builds
* oelint.vars.srcurioptions - Fetcher should only valid options
* oelint.vars.srcurisrcrevtag - 'tag' in SRC_URI and a SRCREV for the same component doesn't compute
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
  
### Writing your own additional rules

By passing `--customrules` via CLI you could add additional rules to be checked.
The argument should point to a directory - every class derived from `Rule` will be automatically loaded.
Please use the the following as a template for your own

```python
from oelint_adv.cls_rule import Rule


class FooMagicRule(Rule):
    def __init__(self):
        super().__init__(id="foocorp.foo.magic",
                         severity="error",
                         message="Too much foo happening here")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file)
        for i in items:
            if "Foo" in i.Raw:
                res += self.finding(i.Origin, i.InFileLine)
        return res
```

for more details please see the function docstrings of the API

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

### Adding additional constants

You can add e.g. known variable names, or known mirror replacements to the rulefile (or the constantfile).
Just add a key with the corresponding json type to the file.

| key                   | type | description                                                                          |
|-----------------------|------|--------------------------------------------------------------------------------------|
| known_machines        | list | Additional known machine identifiers                                                 |
| known_mirrors         | dict | Known mirror replacements. Key is the variable name surronded by ${}, value a string |
| known_vars            | list | Known variable name, to avoid false positives at `oelint.vars.mispell`               |
| mandatory_vars        | list | Additional mandatory variables that should be set in a recipe                        |
| protected_append_vars | list | Variables that shouldn't be set in a bbappend                                        |
| protected_vars        | list | Variables that shouldn't be set inside of a recipe                                   |
| suggested_vars        | list | Additional suggested variable that should be set in a recipe                         |

## vscode extension

Find the extension in the [marketplace](https://marketplace.visualstudio.com/items?itemName=kweihmann.oelint-vscode), or search for `oelint-vscode`

## Missing anything?

You think there's something missing, wrong, 'improveable'...
Just file an issue to get in contact.

## Contribute

Any sort of ideas, pull requests, bug reports, reports of false positives are welcome.
This project is open to anyone - no pitfalls or legal inconveniences
