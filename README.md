# GHTOPDEP
[![image](https://img.shields.io/pypi/v/ghtopdep.svg)](https://pypi.org/project/ghtopdep/)
[![image](https://img.shields.io/pypi/l/ghtopdep.svg)](https://pypi.org/project/ghtopdep/)
[![image](https://img.shields.io/pypi/pyversions/ghtopdep.svg)](https://pypi.org/project/ghtopdep/)

CLI tool for sorting dependents repo by stars

## Requirements
* Python 3.5 and up

## Installation
from PyPI
```
$ pip install ghtopdep
```

from git repository
```
$ pip install git+https://github.com/github-tooling/ghtopdep
```

from source
```
$ git clone https://github.com/github-tooling/ghtopdep
$ cd ghtopdep
$ python setup.py install
```

## Usage

```
$ ghtopdep --help
Usage: ghtopdep [OPTIONS] URL

Options:
  --show INTEGER       Number of showing repositories (default=10).
  --more-than INTEGER  Number of stars (default=5).
  --help               Show this message and exit.
```


```
$ ghtopdep https://github.com/dropbox/dropbox-sdk-js     
+-------------------------------------------+---------+
| URL                                       |   Stars |
+===========================================+=========+
| https://github.com/LN-Zap/zap-desktop     |     978 |
+-------------------------------------------+---------+
| https://github.com/Cleod9/syncmarx-webext |      35 |
+-------------------------------------------+---------+
| https://github.com/Playork/StickyNotes    |      32 |
+-------------------------------------------+---------+
| https://github.com/WebAssemblyOS/wasmos   |      23 |
+-------------------------------------------+---------+
| https://github.com/Cleod9/syncmarx-api    |      19 |
+-------------------------------------------+---------+
| https://github.com/Bearer/templates       |      11 |
+-------------------------------------------+---------+
| https://github.com/nathsimpson/isobel     |       9 |
+-------------------------------------------+---------+
| https://github.com/sorentycho/blackmirror |       8 |
+-------------------------------------------+---------+
| https://github.com/easylogic/edy          |       6 |
+-------------------------------------------+---------+
| https://github.com/Kikugumo/imas765probot |       5 |
+-------------------------------------------+---------+
found 1203 repos others is private
found 289 repos with more than zero star
```


## Development setup
Using [Poetry](https://poetry.eustace.io/docs/)   
```
$ poetry install
```
or [Pipenv](https://docs.pipenv.org/)   
```
$ pipenv install --dev -e .
```

## License
[MIT](https://choosealicense.com/licenses/mit/)