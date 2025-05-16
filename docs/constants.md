# use of constants

By default the linter will load the known variables, machines and distro settings for
the chosen release of ``poky/meta``.
More 3rd party layer settings can be added by using ``--extra-layer`` CLI argument.

e.g. to load in addition to ``core`` layer the information of ``meta-openembedded/meta-webserver``,
``--extra-layer=webserver`` can be used.

## currently available information

For all releases starting from ``kirkstone`` the following 3rd party layer configurations are
available

| name                     | layer                                   |
| ------------------------ | --------------------------------------- |
| ``clang-layer``          | meta-clang                              |
| ``core``                 | meta from poky                          |
| ``filesystems-layer``    | meta-filesystems from meta-openembedded |
| ``flutter-layer``        | meta-flutter                            |
| ``freescale-distro``     | meta-freescale-distro                   |
| ``freescale-layer``      | meta-freescale                          |
| ``gnome-layer``          | meta-gnome from meta-openembedded       |
| ``intel``                | meta-intel                              |
| ``meta-initramfs``       | meta-initramfs from meta-openembedded   |
| ``meta-python``          | meta-python from meta-openembedded      |
| ``meta-sca``             | meta-sca                                |
| ``multimedia-layer``     | meta-multimedia from meta-openembedded  |
| ``networking-layer``     | meta-networking from meta-openembedded  |
| ``openembedded-layer``   | meta-oe from meta-openembedded          |
| ``perl-layer``           | meta-perl from meta-openembedded        |
| ``qt6-layer``            | meta-qt6                                |
| ``rubygems``             | meta-rubygems                           |
| ``virtualization-layer`` | meta-virtualization                     |
| ``webkit``               | meta-webkit                             |
| ``webserver``            | meta-webserver from meta-openembedded   |
| ``xfce-layer``           | meta-xfce from meta-openembedded        |
| ``yocto``                | meta-poky from poky                     |
| ``yoctobsp``             | meta-yocto-bsp from poky                |

## layer specific constants

You can create a layer specific constants file, which is automatically loaded by the linter, if any recipe from that
layer is checked.

Those files contain information about the found machines, distros and class variables, in addition to dependencies
on other 3rd party layer.

Use the ``scripts/generate-layer-variables`` tool for that.

### step by step guide

- checkout the master of the ``oelint-data`` repository.
- create a virtual python environment (e.g. ``python3 -m venv env``)
- active the virtual python environment (e.g. ``. env/bin/activate``)
- install the needed dependencies (e.g. ``pip3 install -r requirements.txt -r requirements-dev.txt``) from the ``oelint-adv`` checkout
- checkout your custom layer and all of the dependencies
- run ``generate-layer-variables --layer_filter <name of your layer> --local <path to the poky checkout> <path to the build directory> <name of the release> <path to your layer checkout>/oelint.constants.json <name(s) of other layers to exclude>``
  - e.g. your layer is called ``my-project-layer`` and does required ``core``, ``meta-poky`` and ``meta-oe`` for a ``scarthgap`` release the command
    line would look like
    ``generate-layer-variables --layer_filter my-project-layer --local <path to the poky checkout> <path to the build directory> scarthgap <path to your layer checkout>/oelint.constants.json core yocto openembedded-layer``

In case your layer supports multiple different sets of information for different releases you can create a ``oelint.constants.<release name>.json``
file in your layer root.

## Constants to add

| key                        | type | description                                | getter for information                                     |
| -------------------------- | ---- | ------------------------------------------ | ---------------------------------------------------------- |
| functions/known            | list | known functions                            | `oelint_parse.constants.CONSTANT.FunctionsKnown`           |
| functions/order            | list | preferred order of core functions          | `oelint_parse.constants.CONSTANT.FunctionsOrder`           |
| images/known-classes       | list | bbclasses to be known to be used in images | `oelint_parse.constants.CONSTANT.ImagesClasses`            |
| images/known-variables     | list | variables known to be used in images       | `oelint_parse.constants.CONSTANT.ImagesVariables`          |
| replacements/distros       | list | known distro overrides                     | `oelint_parse.constants.CONSTANT.DistrosKnown`             |
| replacements/machines      | list | known machine overrides                    | `oelint_parse.constants.CONSTANT.MachinesKnown`            |
| replacements/mirrors       | dict | known mirrors                              | `oelint_parse.constants.CONSTANT.MirrorsKnown`             |
| variables/known            | list | known variables                            | `oelint_parse.constants.CONSTANT.VariablesKnown`           |
| variables/mandatory        | list | variables mandatory to a recipe            | `oelint_parse.constants.CONSTANT.VariablesMandatory`       |
| variables/order            | list | preferred order of variables               | `oelint_parse.constants.CONSTANT.VariablesOrder`           |
| variables/protected        | list | variables not to be used in recipes        | `oelint_parse.constants.CONSTANT.VariablesProtected`       |
| variables/protected-append | list | variables not to be used in bbappends      | `oelint_parse.constants.CONSTANT.VariablesProtectedAppend` |
| variables/suggested        | list | suggested variable in a recipe             | `oelint_parse.constants.CONSTANT.VariablesSuggested`       |

## Q&A

## why only class and configuration related variables?

By default only variables defined by files under ``conf/``, ``lib/``, ``classes``, ``classes-global`` and ``classes-recipe``
are available.

Variables defined in recipes are deliberately ignored.

Those recipe defined variables should not be used outside of the recipe, as they are subject to change without any warning.

## the variable 'xyz' is not listed, even if it's part of oe-core

Sadly oe-core still uses variables without default values and/or documentation.
To have a variable listed, the variable needs to be used (at least the default value loaded)
by any recipe and/or configuration file.

You can check that by running

```shell
$ bitbake-getvar XYZ
# or
$ bitbake-getvar -r <recipe that uses the variable> XYZ
```

if both return

```shell
The variable 'XYZ' is not defined
```

then an upstream patch needs to be posted adding a sane default value and documentation
to it.

## the variable 'xyz' is part of the latest, but missing in an older release branch

Please check if all patches have been properly backported upstream.

## I need those settings for releases earlier than kirkstone

Sadly the needed tooling to extract the information is only available from kirkstone on.
And with ``honister`` release being now EOL since May 2022, it's maybe time to move away
from using those branches all together.
Manually gathering the data is an error prone process, so the only valid option is to
set those to your layer specific constant file (a file that you will need to manually
create and maintain).

## How can I add more layers to the default data?

More data can be requested via an issue, but only for layer that are publicly accessible
and support *ALL* the currently in support releases.

## How can I add data from my extra private layer?

Currently there is no support for that planned, as the tool doesn't know anything
about layers or the way they are assembled.
So the only option will be to merge all information from that layer into the
layer specific constant file of the consuming layer.

## A variable added/changed upstream is not reflected in the data yet

The variables are bumped once a week, so please give the automation some time
till the update will be available.
