# oelint-adv
Advanced oelint

## Purpose

Based on the [OpenEmbedded Styleguide](https://www.openembedded.org/wiki/Styleguide) and work done by [oe-stylize-tool](https://github.com/openembedded/meta-openembedded/blob/master/contrib/oe-stylize.py) this module offers a (nearly) complete linter for bitbake-recipes.

The tool does handle includes/requires automatically so you don't have to pass them via CLI.

**NOTE**: .bbappend-files have to be passed via CLI - these are NOT gathered automatically

## Usage

```
oelint-adv
usage: oelint-adv [-h] [--suppress SUPPRESS] [--output OUTPUT]
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

 * oelint.comments.notrailing - No trailing comments allowed, comments should be on a single line
 * oelint.file.patchsignedoff - Patches should contain a Signed-Of-By entry
 * oelint.file.upstreamstatus - Patches should contain a Upstream-Status entry
 * oelint.spaces.emptyline - Empty line should not contain spaces or tabs
 * oelint.spaces.linebeginning - No space at a line beginning
 * oelint.spaces.linecont - Safe line continuation 
 * oelint.spaces.lineend - No spaces at line end
 * oelint.tabs.notabs - No tabs allowed
 * oelint.task.addnotaskbody - Task added by addtask cannot be found
 * oelint.task.customorder - order of custom tasks added via addtask
 * oelint.task.docstrings - Custom tasks should have docstrings
 * oelint.task.multiappends - Multiple appends to the same function in the same file won't work in bitbake
 * oelint.task.nocopy - No cp usage in do_install
 * oelint.task.nomkdir - No mkdir usage in do_install
 * oelint.task.order - Order of tasks
 * oelint.var.bbclassextend - Use BBCLASSEXTEND when possible
 * oelint.var.licenseremotefile - License shall be a file in remote source not a local file
 * oelint.var.mandatoryvar - Check for mandatory variables
 * oelint.var.multiinclude - Warn on including the same file more than once
 * oelint.var.multiinherit - Warn on inherit the same file more than once
 * oelint.var.nativefilename - Native only recipes should be named -native
 * oelint.var.order - Variable order
 * oelint.var.override - Check if include/append is overriding a variable
 * oelint.var.suggestedvar - Notice on suggeste variables
 * oelint.vars.bugtrackerisurl - BUGTRACKER should be an URL
 * oelint.vars.homepageprefix - HOMEPAGE should begin with https:// or http://
 * oelint.vars.multilineident - On a multiline assignment, line indent is desirable
 * oelint.vars.sectionlowercase - SECTION should be lowercase only
 * oelint.vars.spacesassignment - ' = ' should be correct variable assigment
 * oelint.vars.summary80chars - SUMMARY should max. be 80 characters long
 * oelint.vars.summarylinebreaks - No line breaks in SUMMARY
 * oelint.vars.valuequoted - Variable values should be properly quoteds