# oelint-adv

![Build status](https://github.com/priv-kweihmann/oelint-adv/workflows/Python%20package/badge.svg)
[![PyPI version](https://badge.fury.io/py/oelint-adv.svg)](https://badge.fury.io/py/oelint-adv)
[![Python version](https://img.shields.io/pypi/pyversions/oelint-adv)](https://img.shields.io/pypi/pyversions/oelint-adv)
[![Downloads](https://img.shields.io/pypi/dm/oelint-adv)](https://img.shields.io/pypi/dm/oelint-adv)

Advanced oelint

## Purpose

Based on the [OpenEmbedded Styleguide](https://www.openembedded.org/wiki/Styleguide) and work done by [oe-stylize-tool](https://github.com/openembedded/meta-openembedded/blob/master/contrib/oe-stylize.py) this module offers a (nearly) complete linter for bitbake-recipes.

The tool should help anyone working with YOCTO/OpenEmbedded to write more clean, less 'magical' recipes, without the need to know all the internals of your used poky/OpenEmbedded version.

It could also be used as part of a CI to avoid hard to debug issues slipping to your code base - be sure to checkout [rulefile](#defining-a-ruleset) for that use case.

As every linter this tool is sometimes extra picky, but for the good of it, not just to bug people.
Especially for novice users it might be a help to avoid the most common pitfalls of bitbake recipes.

The tool does handle includes/requires automatically, so you don't have to pass them via CLI.

**NOTE**: .bbappend-files have to be passed via CLI - these are NOT gathered automatically.

You can also pass ``distro``, ``machine`` and ``layer`` config files.
Those will be automatically handled in the correct order.

## Install

With pip (**recommended**)

```shell
pip3 install oelint_adv
```

from source

```shell
git clone https://github.com/priv-kweihmann/oelint-adv
cd oelint-adv
python3 setup.py install # might require sudo/root permissions
```

**NOTE** if you install from source, you'll have to provide all matching
required python libraries on your own. See [requirements.txt](requirements.txt) for details

## Usage

```shell
usage: oelint-adv [-h] [--suppress SUPPRESS] [--output OUTPUT] [--fix] [--nobackup] [--addrules ADDRULES [ADDRULES ...]]
                  [--customrules CUSTOMRULES [CUSTOMRULES ...]] [--rulefile RULEFILE] [--jobs JOBS] [--color] [--quiet]
                  [--hide {info,warning,error}]
                  [--mode {fast,all}] [--relpaths] [--messageformat MESSAGEFORMAT] [--constantmods CONSTANTMODS [CONSTANTMODS ...]] [--print-rulefile]
                  [--exit-zero]
                  [--release {...}]
                  [--cached] [--cachedir CACHEDIR] [--clear-caches] [--extra-layer [EXTRA_LAYER ...]]
                  [--version]
                  [files ...]

Advanced OELint - Check bitbake recipes against OECore styleguide

positional arguments:
  files                 File to parse

options:
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
  --jobs JOBS           Number of jobs to run (default all cores)
  --color               Add color to the output based on the severity
  --quiet               Print findings only
  --hide {info,warning,error}
                        Hide mesesages of specified severity
  --mode {fast,all}     Level of testing (default: fast)
  --relpaths            Show relative paths instead of absolute paths in results
  --messageformat MESSAGEFORMAT
                        Format of message output
  --constantmods CONSTANTMODS [CONSTANTMODS ...]
                        Modifications to the constant db. prefix with: + - to add to DB, - - to remove from DB, None - to override DB
  --print-rulefile      Print loaded rules as a rulefile and exit
  --exit-zero           Always return a 0 (non-error) status code, even if lint errors are found
  --release {...}
                        Run against a specific Yocto release
  --cached              Use caches (default: off)
  --cachedir CACHEDIR   Cache directory (default $HOME/.oelint/caches)
  --clear-caches        Clear cache directory and exit
  --extra-layer [EXTRA_LAYER ...]
                        Layer names of 3rd party layers to use
  --version             show program's version number and exit
```

## Output

Will be [file]:[line]:[severity]:[id]:[message].
To change the default message format, please see [Output message format](#output-message-format) section.

Example:

```shell
/disk/meta-some/cppcheck-native/cppcheck.inc:26:error:oelint.task.nomkdir:'mkdir' shall not be used in do_install. Use 'install' [branch:true]
/disk/meta-some/cppcheck-native/cppcheck-native_1.87.bb:0:error:oelint.var.mandatoryvar.SECTION:Variable 'SECTION' should be set [branch:true]
/disk/meta-some/cppcheck-native/cppcheck.inc:1:warning:oelint.vars.summary80chars:'SUMMARY' should not be longer than 80 characters [branch:true]
/disk/meta-some/cppcheck-native/cppcheck.inc:4:warning:oelint.vars.homepageprefix:'HOMEPAGE' should start with 'http://' or 'https://' [branch:true]
/disk/meta-some/cppcheck-native/cppcheck.inc:28:warning:oelint.spaces.lineend:Line shall not end with a space [branch:true]
/disk/meta-some/cppcheck-native/cppcheck-native_1.87.bb:0:error:oelint.var.mandatoryvar.AUTHOR:Variable 'AUTHOR' should be set [branch:true]
/disk/meta-some/cppcheck-native/cppcheck.inc:26:error:oelint.task.nocopy:'cp' shall not be used in do_install. Use 'install' [branch:true]
/disk/meta-some/cppcheck-native/cppcheck.inc:12:warning:oelint.var.order.DEPENDS:'DEPENDS' should be placed before 'inherit' [branch:true]
```

**NOTE**: as the tool checks against permutations of the input files, the used permutation matrix is appended to the rules message.
E.g.

- ``[branch:true]``, means the finding was found on the ``true`` branch of an expanded inline function block.
- ``[branch:false,mydistro.conf]``, means the finding occurs only when using ``mydistro.conf`` and on the ``false`` branch of an expanded inline function block.

This should help to better spot the issue found by the linter.

## Apply automatic fixing

Some of the rules are capable of fixing the issues found automatically.
This will be done if you pass **--fix** as a startup parameter.

As long as you don't pass **--nobackup** a backup copy (filename + .bak) will be created for all files fixed.

## Available rules

Rules marked with **[F]** are able to perform automatic fixing
Rules marked with **[S]** can have multiple sub-IDs
Rules marked with **[I]** need to be activated through [a rule file](#defining-a-ruleset) first

* [oelint.append.protvars](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.append.protvars.md) - Variables that shouldn't be set in a bbappend **[S]**
* [oelint.bbclass.underscores](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.bbclass.underscores.md) - bbclass filenames shall not contain dashes
* [oelint.exportfunction.dash](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.exportfunction.dash.md) - EXPORT_FUNCTIONS shall not contain dashes
* [oelint.file.inactiveupstreamdetails](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.file.inactiveupstreamdetails.md) - Patches with Upstream-Status: Inactive-Upstream require more details
* [oelint.file.inappropriatemsg](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.file.inappropriatemsg.md) - Patches with Upstream-Status: Inappropriate should provide a valid reasoning
* [oelint.file.includenotfound](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.file.includenotfound.md) - File to be included not found
* [oelint.file.includerelpath](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.file.includerelpath.md) - Require should be used instead of include
* [oelint.file.inlinesuppress_na](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.file.inlinesuppress_na.md) - A not applicable inline suppression has been found
* [oelint.file.nospaces](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.file.nospaces.md) - Path to file should not contain spaces
* [oelint.file.patchsignedoff](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.file.patchsignedoff.md) - Patches should contain a Signed-Of-By entry
* [oelint.file.requireinclude](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.file.requireinclude.md) - Require should be used instead of include
* [oelint.file.requirenotfound](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.file.requirenotfound.md) - File to be required not found
* [oelint.file.underscores](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.file.underscores.md) - Checks the correct usage of underscores in filename
* [oelint.file.upstreamstatus](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.file.upstreamstatus.md) - Patches should contain a Upstream-Status entry
* [oelint.file.upstreamstatus_occurance](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.file.upstreamstatus_occurance.md) - Certain Upstream-Status classifier found **[S]** **[I]**
* [oelint.func.specific](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.func.specific.md) - Function is specific to an unknown identifier
* [oelint.newline.consecutive](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.newline.consecutive.md) - Consecutive blank lines should be avoided
* [oelint.newline.eof](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.newline.eof.md) - File shall end on a newline **[F]**
* [oelint.spaces.emptyline](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.spaces.emptyline.md) - Empty line should not contain spaces or tabs **[F]**
* [oelint.spaces.linebeginning](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.spaces.linebeginning.md) - No space at a line beginning **[F]**
* [oelint.spaces.linecont](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.spaces.linecont.md) - Safe line continuation **[F]**
* [oelint.spaces.lineend](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.spaces.lineend.md) - No spaces at line end **[F]**
* [oelint.tabs.notabs](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.tabs.notabs.md) - No tabs allowed **[F]**
* [oelint.task.addnotaskbody](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.task.addnotaskbody.md) - Task added by addtask cannot be found
* [oelint.task.customorder](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.task.customorder.md) - order of custom tasks added via addtask
* [oelint.task.dash](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.task.dash.md) - Functions and related statements shall not contain dashes
* [oelint.task.docstrings](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.task.docstrings.md) - Custom tasks should have docstrings
* [oelint.task.heredocs](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.task.heredocs.md) - Usage of heredocs should be avoided. Use files instead
* [oelint.task.multifragments](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.task.multifragments.md) - Multiple fragments of the same function in the same file should be merged
* [oelint.task.network](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.task.network.md) - Warn about potential network access of tasks
* [oelint.task.noanonpython](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.task.noanonpython.md) - Avoid anonymous python functions
* [oelint.task.nocopy](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.task.nocopy.md) - No cp usage in do_install
* [oelint.task.nomkdir](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.task.nomkdir.md) - No mkdir usage in do_install
* [oelint.task.nopythonprefix](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.task.nopythonprefix.md) - Tasks containing shell code should NOT be prefixed with 'python' in function header
* [oelint.task.order](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.task.order.md) - Order of tasks **[S]**
* [oelint.task.pythonprefix](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.task.pythonprefix.md) - Tasks containing python code should be prefixed with 'python' in function header
* [oelint.var.addpylib](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.var.addpylib.md) - addpylib is only valid in .conf files
* [oelint.var.badimagefeature](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.var.badimagefeature.md) - Warn about "bad" IMAGE_FEATURES
* [oelint.var.bbclassextend](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.var.bbclassextend.md) - Use BBCLASSEXTEND when possible
* [oelint.var.filesoverride](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.var.filesoverride.md) - FILES:*(FILES_*) variables should not be overridden
* [oelint.var.improperinherit](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.var.improperinherit.md) - Warn about improperly named inherits
* [oelint.var.inherit](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.var.inherit.md) - Check the correct usage of inherit and inherit_defer (scarthgap+)
* [oelint.var.inheritdevtool](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.var.inheritdevtool.md) - inherit_defer is recommended for native and nativesdk class **[S]** (scarthgap+)
* [oelint.var.inheritlast](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.var.inheritlast.md) - Target specific classes need to be inherited last **[S]**
* [oelint.var.licenseremotefile](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.var.licenseremotefile.md) - License shall be a file in remote source not a local file
* [oelint.var.mandatoryvar](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.var.mandatoryvar.md) - Check for mandatory variables **[S]**
* [oelint.var.multiinclude](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.var.multiinclude.md) - Warn on including the same file more than once
* [oelint.var.multiinherit](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.var.multiinherit.md) - Warn on inherit the same file more than once
* [oelint.var.nativefilename](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.var.nativefilename.md) - Native only recipes should be named.md -native
* [oelint.var.nativesdkfilename](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.var.nativesdkfilename.md) - NativeSDK only recipes should be named nativesdk-
* [oelint.var.order](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.var.order.md) - Variable order **[S]**
* [oelint.var.override](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.var.override.md) - Check if include/append is overriding a variable
* [oelint.var.rootfspostcmd](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.var.rootfspostcmd.md) - ROOTFS_POSTPROCESS_COMMAND should not have trailing blanks
* [oelint.var.srcuriwildcard](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.var.srcuriwildcard.md) - 'SRC_URI' should not contain any wildcards
* [oelint.var.suggestedvar](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.var.suggestedvar.md) - Notice on suggested variables **[S]**
* [oelint.vars.appendop](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.appendop.md) - Use ':append(_append)' instead of ' += '
* [oelint.vars.autorev](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.autorev.md) - The usage of 'AUTOREV' for SRCREV leads to not reproducible builds
* [oelint.vars.bbvars](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.bbvars.md) - Variables that shouldn't be altered in recipe scope **[S]**
* [oelint.vars.bugtrackerisurl](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.bugtrackerisurl.md) - BUGTRACKER should be an URL
* [oelint.vars.dependsappend](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.dependsappend.md) - DEPENDS should only be appended, not overwritten
* [oelint.vars.dependsclass](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.dependsclass.md) - DEPENDS should use the correct class variants
* [oelint.vars.dependsordered](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.dependsordered.md) - RDEPENDS entries should be ordered alphabetically
* [oelint.vars.descriptionsame](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.descriptionsame.md) - 'DESCRIPTION' is the same a 'SUMMARY'.md) - it can be removed then
* [oelint.vars.descriptiontoobrief](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.descriptiontoobrief.md) - 'DESCRIPTION' is the shorter than 'SUMMARY'
* [oelint.vars.distroconf](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.distroconf.md) - Machine and image variables should not be set as part of a distro config **[S]**
* [oelint.vars.doublemodify](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.doublemodify.md) - Multiple modifiers of append/prepend/remove/+= found in one operation
* [oelint.vars.doublesemicolon](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.doublesemicolon.md) - pointless double semicolons detected in variable value **[F]**
* [oelint.vars.downloadfilename](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.downloadfilename.md) - Fetcher does create a download artifact without 'PV' in the filename
* [oelint.vars.duplicate](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.duplicate.md) - No duplicates in DEPENDS and RDEPENDS
* [oelint.vars.dusageinpkgfuncs](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.dusageinpkgfuncs.md) - use \$D instead of \$\{D\} in pkg functions **[F]**
* [oelint.vars.fileextrapaths](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.fileextrapaths.md) - 'FILESEXTRAPATHS' shouldn't be used in a bb file
* [oelint.vars.fileextrapathsop](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.fileextrapathsop.md) - 'FILESEXTRAPATHS' should only be used in combination with ' := '
* [oelint.vars.filessetting](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.filessetting.md) - unnecessary FILES settings
* [oelint.vars.homepageping](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.homepageping.md) - 'HOMEPAGE' isn't reachable
* [oelint.vars.homepageprefix](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.homepageprefix.md) - HOMEPAGE should begin with https:// or http://
* [oelint.vars.inappclassoverride](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.inappclassoverride.md) - warn about inapplicable class specific overrides
* [oelint.vars.inconspaces](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.inconspaces.md) - Inconsistent use of spaces on append operation
* [oelint.vars.insaneskip](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.insaneskip.md) - INSANE_SKIP should be avoided at any cost
* [oelint.vars.layerconf](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.layerconf.md) - Only selected variables should be set as part of a layer.conf
* [oelint.vars.licensesdpx](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.licensesdpx.md) - Check for correct SPDX syntax in licenses
* [oelint.vars.licfileprefix](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.licfileprefix.md) - Unnecessary prefix to LIC_FILES_CHKSUM detected **[F]**
* [oelint.vars.listappend](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.listappend.md) - Proper append/prepend to lists **[F]**
* [oelint.vars.machineconf](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.machineconf.md) - Distro and image variables should not be set as part of a machine config **[S]**
* [oelint.vars.mispell.unknown](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.mispell.unknown.md) - Variable is not known from CONSTANTS, typo is unlikely
* [oelint.vars.mispell](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.mispell.md) - Possible typo detected
* [oelint.vars.multilineident](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.multilineident.md) - On a multiline assignment, line indent is desirable **[F]**
* [oelint.vars.notneededspace](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.notneededspace.md) - Space at the beginning of the var is not needed **[F]**
* [oelint.vars.notrailingslash](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.notrailingslash.md) - Variable shall not end on a slash
* [oelint.vars.outofcontext](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.outofcontext.md) - variables are used in the wrong context
* [oelint.vars.overrideappend](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.overrideappend.md) - Check correct order of append/prepend on variables with override syntax
* [oelint.vars.pathhardcode](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.pathhardcode.md) - Warn about the usage of hardcoded paths **[S]**
* [oelint.vars.pbpusage](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.pbpusage.md) - \$\{BP\} should be used instead of \$\{P\} **[F]**
* [oelint.vars.pkgspecific](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.pkgspecific.md) - Variable is package-specific, but isn't set in that way **[S]**
* [oelint.vars.pnbpnusage](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.pnbpnusage.md) - \$\{BPN\} should be used instead of \$\{PN\} **[F]**
* [oelint.vars.pnusagediscouraged](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.pnusagediscouraged.md) - Variable shouldn't contain \$\{PN\} or \$\{BPN\}
* [oelint.vars.pythonpnusage](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.pythonpnusage.md) - python3 should be used instead of \$\{PYTHON_PN\} **[F]** (scarthgap+)
* [oelint.vars.renamed](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.renamed.md) - Warn about renamed or deprecated variables **[F]**
* [oelint.vars.sectionlowercase](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.sectionlowercase.md) - SECTION should be lowercase only **[F]**
* [oelint.vars.spacesassignment](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.spacesassignment.md) - ' = ' should be correct variable assignment
* [oelint.vars.specific](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.specific.md) - Variable is specific to an unknown identifier
* [oelint.vars.srcuriappend](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.srcuriappend.md) - Use SRC_URI:append(SRC_URI_append) otherwise this will override weak defaults by inherit
* [oelint.vars.srcurichecksum](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.srcurichecksum.md) - If SRC_URI has URLs pointing single file that is not from VCS, then checksusm is required
* [oelint.vars.srcuridomains](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.srcuridomains.md) - Recipe is pulling from different domains, this will likely cause issues
* [oelint.vars.srcurifile](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.srcurifile.md) - First item of SRC_URI should not be a file:// fetcher, if multiple fetcher are used
* [oelint.vars.srcurigittag](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.srcurigittag.md) - 'tag' in SRC_URI-options leads to not-reproducible builds
* [oelint.vars.srcurioptions](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.srcurioptions.md) - Unsupported fetcher or invalid options detected
* [oelint.vars.srcurisrcrevtag](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.srcurisrcrevtag.md) - 'tag' in SRC_URI and a SRCREV for the same component doesn't compute
* [oelint.vars.summary80chars](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.summary80chars.md) - SUMMARY should max. be 80 characters long
* [oelint.vars.summarylinebreaks](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.summarylinebreaks.md) - No line breaks in SUMMARY
* [oelint.vars.unpackdir](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.unpackdir.md) - \$\{UNPACKDIR\} should be used instead of \$\{WORKDIR\} in S and B
* [oelint.vars.valuequoted](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.valuequoted.md) - Variable values should be properly quoted
* [oelint.vars.virtual](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.vars.virtual.md) - no virtual/ items in RDEPENDS/RPROVIDES

### Non-default rulesets

To enable rulesets that are not part of the standard ruleset pass
**--addrules \<ruleset-name\>** to CLI.

These rules are sometimes contrary to OE-style-guide, so use them with caution.

#### jetm ruleset

To enable pass **--addrules jetm** to CLI.

Rules marked with **[F]** are able to perform automatic fixing.

* [oelint.jetm.vars.dependssingleline](https://github.com/priv-kweihmann/oelint-adv/blob/master/docs/wiki/oelint.jetm.vars.dependssingleline.md) - Each [R]DEPENDS entry should be put into a single line
  
### Writing your own additional rules

By passing `--customrules` via CLI you could add additional rules to be checked.
The argument should point to a directory - every class derived from `Rule` will be automatically loaded.
Please use the following as a template for your own:

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

    # To provide automatic fixing capability
    # add the following optional function
    def fix(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file)
        for i in items:
            if 'Foo' in i.Raw:
                # you have to replace the content of `RealRaw` and `Raw`
                # with the fixed content
                # `Raw` is the raw block with expanded inlines blocks
                # `RealRaw` is the raw block without any modifications
                #           this is what will be actually written to the file
                i.RealRaw = i.RealRaw.replace('Foo', 'Bar')
                i.Raw = i.Raw.replace('Foo', 'Bar')
                # Return the file name to signalize that fixes have been
                # applied
                res.append(_file)
        return res
```

For more details please see the function docstrings of the API.

You can find this example also in the development [source tree](https://github.com/priv-kweihmann/oelint-adv/tree/master/docs)

Additional real-life examples can be found in e.g. [meta-rubygems](https://github.com/priv-kweihmann/meta-rubygems/tree/master/files/lint/oelint-custom)

### Release constrained rules

Rules can be also configured to work on specific releases of YP only, if determined not to be applicable, the rules will
be skipped during the loading process and therefore won't show up if e.g. `--print-rulefile` is used

#### Rules working up to a certain release

```python
from oelint_adv.cls_rule import Rule


class FooMagicRule(Rule):
    def __init__(self):
        super().__init__(id="foocorp.foo.magic",
                         severity="error",
                         message="Too much foo happening here",
                         valid_till_release="kirkstone")
```

Would enable the rule, but only if `--release` is set to a YP release earlier than `kirkstone`

#### Rules working from a certain release

```python
from oelint_adv.cls_rule import Rule


class FooMagicRule(Rule):
    def __init__(self):
        super().__init__(id="foocorp.foo.magic",
                         severity="error",
                         message="Too much foo happening here",
                         valid_from_release="kirkstone")
```

Would enable the rule, but only if `--release` is set to a YP release later than `kirkstone` (including `kirkstone`)

#### Enable special settings per release

```python
from oelint_adv.cls_rule import Rule


class FooMagicRule(Rule):
    def __init__(self):
        super().__init__(id="foocorp.foo.magic",
                         severity="error",
                         message="Too much foo happening here")

    def check_release_range(self, release_range: List[str]) -> bool:
        if 'kirkstone' in release_range:
            self._we_are_running_on_kirkstone = True
            self.Appendix.append('kirkstone')
        return super().check_release_range(release_range)
```

Enables the special `Appendix` `kirkstone`, if `kirkstone` is part of the calculated `--release` list.

It also sets the variable `self._we_are_running_on_kirkstone`, which can be used as part of `check()` to
code special code paths.

## File type constrained rules

Rule can be limited in on what kind of files they are run on

e.g.

```python
from oelint_adv.cls_rule import Rule, Classification


class FooMagicRule(Rule):
    def __init__(self):
        super().__init__(id="foocorp.foo.magic",
                         severity="error",
                         run_on=[Classification.RECIPE]
                         message="Too much foo happening here")
```

would only apply to recipe files (.bb).

Valid ``Classification`` are

- ``Classification.BBAPPEND`` : for bbappends
- ``Classification.BBCLASS`` : for bbclasses
- ``Classification.DISTROCONF`` : for distro configurations
- ``Classification.LAYERCONF`` : for layer configurations
- ``Classification.MACHINECONF`` : for machine configurations
- ``Classification.RECIPE`` : for recipes

## Defining a ruleset

If you pass the option `--rulefile` you could define the rules to be checked and their severity via a simple json file.

The rule file could look like this:

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
The severity of `oelint.file.includenotfound` will be the default of the tool, while `oelint.file.requirenotfound` will report `warning` instead of the original suggested severity.

### Adding additional constants

Please see [oelint-parser](https://github.com/priv-kweihmann/oelint-parser) for further details, how to add your own constants to the parser.

## Output message format

You can freely define a custom output format.
The following placeholder symbols will be automatically replaced

| name       | replaced by                  |
| ---------- | ---------------------------- |
| {path}     | path of the file             |
| {line}     | line of the finding          |
| {severity} | severity of the finding      |
| {id}       | error-ID of the finding      |
| {msg}      | description of the finding   |
| {wikiurl}  | a link to the online wiki    |
| {rungroup} | files being checked together |

## Configuration file

You can define your own global or project wide defaults for all CLI parameters with an ini-style configuration file.

In the following order files are probed

* file pointed to by environment variable `OELINT_CONFIG`
* file `.oelint.cfg` in current work directory
* file `.oelint.cfg` in your `HOME` directory

Explicitly passed options to CLI are always chosen over the defaults defined by the configuration file.

To skip the loading of any configuration file, set `OELINT_SKIP_CONFIG` to a non empty value in your environment.

### File format

```ini
[oelint]
# this will set the --hide warning parameter automatically
hide = warning
# this will set A + B as suppress item
# use indent (tab) and line breaks for multiple items
suppress = 
  A
  B
# this will set messageformat parameter
messageformat = {severity}:{id}:{msg}
# will configure --release to dunfell
release=dunfell
```

You can find an example file [here](docs/.oelint.cfg.example)

## Inline suppression

You can suppress one or more checks on a line by line basis

```bitbake
# nooelint: <id>[,<id>,...][ comment]
```

suppresses all the specified IDs for the next line.
Multiple IDs can be separated by commas.
You can add a comment after the ids and separated by at least a single space.

### Example

```bitbake
# nooelint: oelint.vars.insaneskip - this is an acceptable risk here
INSANE_SKIP:${PN} = "foo"
```

will not warn about the usage of `INSANE_SKIP`.

## picking the right constants for your checks

See our [guide](https://github.com/priv-kweihmann/oelint-adv/tree/master/docs/constants.md) for everything you need to know about constants

## cached mode

When run with ``--cached`` the tool will store resuls into a local caching directory and reuse the results, if
nothing has changed in the input tree and configuration.

By default caches are stored to ``OELINT_CACHE_DIR`` environment variable (or `~/.oelint/caches` if not set).

To clear the local caches run ``--clear-caches``

## vscode extension

Find the extension in the [marketplace](https://marketplace.visualstudio.com/items?itemName=kweihmann.oelint-vscode), or search for `oelint-vscode`.

## Vim / NeoVim integration

Integration for Vim / NeoVim is provided by [ale](https://github.com/dense-analysis/ale) or [nvim-lint](https://github.com/mfussenegger/nvim-lint).

## Jenkins integration

Jenkins integration is provided by [warnings-ng](https://plugins.jenkins.io/warnings-ng/).

## Use as a library

To use the linter as part of calling application do

```python
from oelint_adv.core import create_lib_arguments, run

args = create_lib_arguments(['file to check', 'another file to check']])

# check the docstring of create_lib_arguments for more options

results = run(args)

# the results will be a List[Tuple[Tuple[str, int], str]]
# each item is
#  [0] - 'path to the finding', 'line of the finding'
#  [1] - 'message'
```

The caller is responsible for appropriate exception handling

## Missing anything?

You think there's something missing, wrong, 'improvable'...
Just file an issue to get in contact.

## Contribute

Any sort of ideas, pull requests, bug reports, reports of false positives are welcome.
This project is open to anyone - no pitfalls or legal inconveniences.
