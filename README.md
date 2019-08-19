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

## Version upgrade
```
➜ pip install --upgrade ghtopdep   
```

## Usage

```
➜ ghtopdep --help                                              
Usage: ghtopdep [OPTIONS] URL

Options:
  --repositories / --packages  Sort repositories or packages (default
                               repositories)
  --show INTEGER               Number of showing repositories (default=10)
  --more-than INTEGER          Minimum number of stars (default=5)
  --help                       Show this message and exit.
```


```
➜ ghtopdep https://github.com/dropbox/dropbox-sdk-js
+-------------------------------------------+---------+
| URL                                       |   Stars |
+===========================================+=========+
| https://github.com/LN-Zap/zap-desktop     |     979 |
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
found 1173 repos others repos is private
found 281 repos with more than zero star
~ via ⬢ v12.5.0 via 🐘 v7.2.19 via 🐍 3.5.7 took 36s 
```

also you can sort packages

```
➜ ghtopdep https://github.com/dropbox/dropbox-sdk-js --packages
+--------------------------------------------------------+---------+
| URL                                                    |   Stars |
+========================================================+=========+
| https://github.com/jsbin/jsbin                         |    3917 |
+--------------------------------------------------------+---------+
| https://github.com/jvilk/BrowserFS                     |    1489 |
+--------------------------------------------------------+---------+
| https://github.com/coderaiser/cloudcmd                 |    1033 |
+--------------------------------------------------------+---------+
| https://github.com/robertknight/passcards              |     130 |
+--------------------------------------------------------+---------+
| https://github.com/transloadit/uppy-server             |     115 |
+--------------------------------------------------------+---------+
| https://github.com/bioimagesuiteweb/bisweb             |      31 |
+--------------------------------------------------------+---------+
| https://github.com/sallar/dropbox-fs                   |      29 |
+--------------------------------------------------------+---------+
| https://github.com/NickTikhonov/up                     |      13 |
+--------------------------------------------------------+---------+
| https://github.com/soixantecircuits/altruist           |       8 |
+--------------------------------------------------------+---------+
| https://github.com/OpenMarshal/npm-WebDAV-Server-Types |       5 |
+--------------------------------------------------------+---------+
found 129 packages others packages is private
found 57 packages with more than zero star
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
