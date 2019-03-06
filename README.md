# oelint-adv
Advanced oelint

## Purpose

Based on the [OpenEmbedded Styleguide](https://www.openembedded.org/wiki/Styleguide) and work done by [oe-stylize-tool](https://github.com/openembedded/meta-openembedded/blob/master/contrib/oe-stylize.py) this module offers a (nearly) complete linter for bitbake-recipes.

The tool does handle includes/requires automatically so you don't have to pass them via CLI.

## Usage

```
python3 oelint_adv -h
usage: oelint_adv [-h] [--suppress SUPPRESS] [--output OUTPUT]
                  files [files ...]

Advanced OELint - Check bitbake recipes against OECore styleguide

positional arguments:
  files                File to parse

optional arguments:
  -h, --help           show this help message and exit
  --suppress SUPPRESS  Rules to suppress
  --output OUTPUT      Where to flush the findings (default: stderr)
```

## Output

Will be [file]:[line]:[severity]:[message].

Example:
```
/disk/meta-some/cppcheck-native/cppcheck.inc:26:error:oelint.task.nomkdir:'mkdir' shall not be used in do_install. Use 'install'
/disk/meta-some/cppcheck-native/cppcheck-native_1.87.bb:0:error:oelint.var.mandatoryvar:Variable 'SECTION' should be set
/disk/meta-some/cppcheck-native/cppcheck.inc:1:warning:oelint.vars.summary80chars:'SUMMARY' should not be longer than 80 characters
/disk/meta-some/cppcheck-native/cppcheck.inc:4:warning:oelint.vars.homepageprefix:'HOMEPAGE' should start with 'http://' or 'https://'
/disk/meta-some/cppcheck-native/cppcheck.inc:28:warning:oelint.spaces.lineend:Line shall not end with a space
/disk/meta-some/cppcheck-native/cppcheck-native_1.87.bb:0:error:oelint.var.mandatoryvar:Variable 'AUTHOR' should be set
/disk/meta-some/cppcheck-native/cppcheck.inc:26:error:oelint.task.nocopy:'cp' shall not be used in do_install. Use 'install'
/disk/meta-some/cppcheck-native/cppcheck.inc:12:warning:oelint.var.order:'DEPENDS' should be placed before 'inherit'
```

## Available rules

 * oelint.comments.notrailing - No traling comments allowed, comments should be on a single line
 * oelint.spaces.emptyline - Empty line should not contain spaces or tabs
 * oelint.spaces.linebeginning - No space at a line beginning
 * oelint.spaces.linecont - Safe line continuation 
 * oelint.spaces.lineend - No spaces at line end
 * oelint.tabs.notabs - No tabs allowed
 * oelint.task.nocopy - No cp usage in do_install
 * oelint.task.nomkdir - No mkdir usage in do_install
 * oelint.task.order - Order of tasks
 * oelint.var.bbclassextend - Use BBCLASSEXTEND when possible
 * oelint.var.mandatoryvar - Check for mandatory variables
 * oelint.var.nativefilename - Native only recipes should be named -native
 * oelint.var.order - Variable order
 * oelint.var.override - Check if include/append is overriding a variable
 * oelint.var.suggestedvar - Notice on suggeste variables
 * oelint.vars.bugtrackerisurl - BUGTRACKER should be an URL
 * oelint.vars.homepageprefix - HOMEPAGE should begin with https:// or http://
 * oelint.vars.spacesassignment - ' = ' should be correct variable assigment
 * oelint.vars.summary80chars - SUMMARY should max. be 80 characters long
 * oelint.vars.summarylinebreaks - No line breaks in SUMMARY
 * oelint.vars.valuequoted - Variable values should be properly quoteds