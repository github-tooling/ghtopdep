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
$ pip install git+https://github.com/github-tooling/ghtopdep.git#egg=ghtopdep
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

If you want retrieve packages or repositories description you need pass token.
To prevent rale limit being exceeded for unauthentIcated requests, ghtopdep needs an access token.
For public repositories, [create a token](https://github.com/settings/tokens/new?scopes=public_repo&description=ghtopdep) 
with the public_repo permission.

You can use token as environment variable ``GHTOPDEP_TOKEN`` at ``~/.bashrc`` or ``~/.zshrc`` 

export GHTOPDEP_TOKEN="****************************************"

or pass token as option --token

```
➜ ghtopdep --help
Usage: ghtopdep [OPTIONS] URL

Options:
  --repositories / --packages  Sort repositories or packages (default
                               repositories)
  --description                Show description of packages or repositories
                               (performs additional request per repository)
  --rows INTEGER               Number of showing repositories (default=10)
  --minstar INTEGER            Minimum number of stars (default=5)
  --token TEXT
  --help                       Show this message and exit.
```


```
➜ ghtopdep https://github.com/dropbox/dropbox-sdk-js
+-------------------------------------------+---------+
| url                                       |   stars |
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

also you can sort packages and fetch their description 

```
➜ ghtopdep https://github.com/dropbox/dropbox-sdk-js --description --packages
+--------------------------------------------------------+---------+--------------------------------------------------------------+
| url                                                    |   stars | description                                                  |
+========================================================+=========+==============================================================+
| https://github.com/jsbin/jsbin                         |    3919 | Collaborative JavaScript Debugging App                       |
+--------------------------------------------------------+---------+--------------------------------------------------------------+
| https://github.com/jvilk/BrowserFS                     |    1494 | BrowserFS is an in-browser filesystem that emulates the...   |
+--------------------------------------------------------+---------+--------------------------------------------------------------+
| https://github.com/coderaiser/cloudcmd                 |    1042 | ✨☁️📁✨ Cloud Commander file manager for the web with...      |
+--------------------------------------------------------+---------+--------------------------------------------------------------+
| https://github.com/robertknight/passcards              |     130 | A 1Password-compatible command-line and web-based...         |
+--------------------------------------------------------+---------+--------------------------------------------------------------+
| https://github.com/transloadit/uppy-server             |     115 | [DEPRECATED] 'Uppy Server' was renamed to 'Companion' and... |
+--------------------------------------------------------+---------+--------------------------------------------------------------+
| https://github.com/bioimagesuiteweb/bisweb             |      31 | This is the repository for the BioImage Suite Web Project    |
+--------------------------------------------------------+---------+--------------------------------------------------------------+
| https://github.com/sallar/dropbox-fs                   |      29 | :package: Node FS wrapper for Dropbox                        |
+--------------------------------------------------------+---------+--------------------------------------------------------------+
| https://github.com/NickTikhonov/up                     |      13 | Painless, context-aware file uploads from the command line   |
+--------------------------------------------------------+---------+--------------------------------------------------------------+
| https://github.com/soixantecircuits/altruist           |       8 | 💌 Gateway micro service for sharing content with ease ✌️     |
+--------------------------------------------------------+---------+--------------------------------------------------------------+
| https://github.com/OpenMarshal/npm-WebDAV-Server-Types |       5 | Bundle of 'file systems' and 'serializers' for the...        |
+--------------------------------------------------------+---------+--------------------------------------------------------------+
found 130 packages others packages is private
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
