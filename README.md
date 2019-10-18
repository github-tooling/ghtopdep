# GHTOPDEP
[![image](https://img.shields.io/pypi/v/ghtopdep.svg)](https://pypi.org/project/ghtopdep/)
[![image](https://img.shields.io/pypi/l/ghtopdep.svg)](https://pypi.org/project/ghtopdep/)
[![image](https://img.shields.io/pypi/pyversions/ghtopdep.svg)](https://pypi.org/project/ghtopdep/)

CLI tool for sorting dependents repo by stars

## Requirements
* Python 3.5 and up
* Python development libraries

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

## Python development Installation

Ubuntu/Debian
```
sudo apt install python3-dev
```

CentOS/RHEL
```
sudo yum install python3-dev
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
+---------------------------------------------------+---------+
| url                                               |   stars |
+===================================================+=========+
| https://github.com/transloadit/uppy               |   20726 |
+---------------------------------------------------+---------+
| https://github.com/codesandbox/codesandbox-client |    7924 |
+---------------------------------------------------+---------+
| https://github.com/joemccann/dillinger            |    6452 |
+---------------------------------------------------+---------+
| https://github.com/keplergl/kepler.gl             |    5306 |
+---------------------------------------------------+---------+
| https://github.com/jitsi/jitsi-meet               |    4114 |
+---------------------------------------------------+---------+
| https://github.com/jsbin/jsbin                    |    3919 |
+---------------------------------------------------+---------+
| https://github.com/NorthwoodsSoftware/GoJS        |    3543 |
+---------------------------------------------------+---------+
| https://github.com/buttercup/buttercup-desktop    |    3004 |
+---------------------------------------------------+---------+
| https://github.com/openstyles/stylus              |    2101 |
+---------------------------------------------------+---------+
| https://github.com/mickael-kerjean/filestash      |    1610 |
+---------------------------------------------------+---------+
found 1583 repositories others repositories is private
found 419 repositories with more than zero star
~ via ⬢ v12.5.0 via 🐘 v7.2.19 via 🐍 3.5.7 took 36s 
```

also you can sort packages and fetch their description 

```
➜ ghtopdep https://github.com/dropbox/dropbox-sdk-js --description --packages
+------------------------------------------------+---------+--------------------------------------------------------------+
| url                                            |   stars | description                                                  |
+================================================+=========+==============================================================+
| https://github.com/jsbin/jsbin                 |    3919 | Collaborative JavaScript Debugging App                       |
+------------------------------------------------+---------+--------------------------------------------------------------+
| https://github.com/jvilk/BrowserFS             |    1497 | BrowserFS is an in-browser filesystem that emulates the...   |
+------------------------------------------------+---------+--------------------------------------------------------------+
| https://github.com/coderaiser/cloudcmd         |    1043 | ✨☁️📁✨ Cloud Commander file manager for the web with...       |
+------------------------------------------------+---------+--------------------------------------------------------------+
| https://github.com/node-red/node-red-web-nodes |     144 | A collection of node-red nodes aimed at web services         |
+------------------------------------------------+---------+--------------------------------------------------------------+
| https://github.com/robertknight/passcards      |     130 | A 1Password-compatible command-line and web-based...         |
+------------------------------------------------+---------+--------------------------------------------------------------+
| https://github.com/enyojs/ares-project         |     125 | A browser-based code editor and UI designer for Enyo 2...    |
+------------------------------------------------+---------+--------------------------------------------------------------+
| https://github.com/transloadit/uppy-server     |     115 | [DEPRECATED] 'Uppy Server' was renamed to 'Companion' and... |
+------------------------------------------------+---------+--------------------------------------------------------------+
| https://github.com/bioimagesuiteweb/bisweb     |      31 | This is the repository for the BioImage Suite Web Project    |
+------------------------------------------------+---------+--------------------------------------------------------------+
| https://github.com/sallar/dropbox-fs           |      29 | :package: Node FS wrapper for Dropbox                        |
+------------------------------------------------+---------+--------------------------------------------------------------+
| https://github.com/filefog/filefog             |      26 | A thin cloud-service agnostic wrapper/interface to access... |
+------------------------------------------------+---------+--------------------------------------------------------------+
found 130 packages others packages are private
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
