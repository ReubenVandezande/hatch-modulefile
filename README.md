# hatch_modulefile

[![PyPI - Version](https://img.shields.io/pypi/v/hatch-modulefile.svg)](https://pypi.org/project/hatch-modulefile)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hatch-modulefile.svg)](https://pypi.org/project/hatch-modulefile)

-----

**Table of Contents**

- [Installation](#installation)
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


## License

`hatch-modulefile` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
