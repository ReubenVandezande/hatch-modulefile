# hatch_modulefile

[![PyPI - Version](https://img.shields.io/pypi/v/hatch-modulefile.svg)](https://pypi.org/project/hatch-modulefile)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hatch-modulefile.svg)](https://pypi.org/project/hatch-modulefile)

-----

This provides automatic modulefile generation for [EnvironmentModules](https://modules.readthedocs.io/en/latest/). Modulefiles are created with a basic template which:

1. Loads any modules listed in `requires`
2. Sources the activate script of the installed packages (assumes venv installation)
3. Sets extra environment variables defined in extra-paths

**Table of Contents**

- [Installation](#installation)
- [Example](#example)
- [License](#license)

## Installation

```console
pip install hatch-modulefile
```

## Example

Example use case. Note that requires is a list of modulefiles available on your system 
through environment modules. Extra paths defines modulefile environment manipulations.

[build.hooks.modulefile]
requires = [
  "module1/1.0.0",
  "module2/3.1.2",
  "module3/2.0.0",
]
extra-paths = [
  { type="setenv", variable="NUMEXPR_MAX_THREADS", value="8" },
  { type="prepend-path", variable="PATH", value="/custom/path" },
]

This would generate a modulefile which looks like this:

```
#%Module

# Gets the folder two folders up from this file
set              venv                    [file dirname [file dirname [file dirname [file normalize $ModulesCurrentModulefile/___]]]]
set              site_packages           [glob $venv/lib/python*/site-packages]

set     necessary       {
  module1/1.0.0
  module2/3.1.2
  module3/2.0.0
}

foreach mod $necessary {
    set splitList [split $mod "/"]
    set mod_name [lindex $splitList 0]
    if { [ is-loaded $mod_name ] } {
        module switch $mod
    } else {
        module load $mod
    }
}

if { [module-info mode load] || [module-info mode switch2] } {
    puts stdout "source $venv/bin/activate;"
} elseif { [module-info mode remove] && ![module-info mode switch3] } {
    puts stdout "deactivate;"
}

# Extra module path requirements
setenv          NUMEXPR_MAX_THREADS     8
prepend-path    PATH                    /custom/path
```

## License

`hatch-modulefile` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
