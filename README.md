# GHTOPDEP

[![image](https://img.shields.io/pypi/v/ghtopdep.svg)](https://pypi.org/project/ghtopdep/)
[![image](https://img.shields.io/pypi/l/ghtopdep.svg)](https://pypi.org/project/ghtopdep/)
[![image](https://img.shields.io/pypi/pyversions/ghtopdep.svg)](https://pypi.org/project/ghtopdep/)

CLI tool for sorting dependents repo by stars

## Requirements

- Python 3.5 and up
- Python development libraries

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
sudo yum install python3-devel
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

You can use token as environment variable `GHTOPDEP_TOKEN` at `~/.bashrc` or `~/.zshrc`

export GHTOPDEP_TOKEN="**\*\*\*\***\*\***\*\*\*\***\*\*\*\***\*\*\*\***\*\***\*\*\*\***"

or pass token as option --token

```
➜ ghtopdep --help
Usage: ghtopdep [OPTIONS] URL

Options:
  --repositories / --packages  Sort repositories or packages (default
                               repositories)
  --table / --json             View mode
  --description                Show description of packages or repositories
                               (performs additional request per repository)
  --rows INTEGER               Number of showing repositories (default=10)
  --minstar INTEGER            Minimum number of stars (default=5)
  --search TEXT                search code at dependents
                               (repositories/packages)
  --token TEXT
  --help                       Show this message and exit.
```

Table view (by default)

```
➜ ghtopdep https://github.com/dropbox/dropbox-sdk-js
| url                                               | stars   |
|---------------------------------------------------|---------|
| https://github.com/transloadit/uppy               | 21K     |
| https://github.com/codesandbox/codesandbox-client | 8.6K    |
| https://github.com/joemccann/dillinger            | 6.5K    |
| https://github.com/keplergl/kepler.gl             | 5.8K    |
| https://github.com/jitsi/jitsi-meet               | 4.5K    |
| https://github.com/jsbin/jsbin                    | 4.0K    |
| https://github.com/NorthwoodsSoftware/GoJS        | 3.8K    |
| https://github.com/buttercup/buttercup-desktop    | 3.1K    |
| https://github.com/openstyles/stylus              | 2.3K    |
| https://github.com/mickael-kerjean/filestash      | 2.0K    |
found 1660 repositories others repositories are private
found 443 repositories with more than zero star
~ via ⬢ v12.5.0 via 🐘 v7.2.19 via 🐍 3.8.0 took 2m 57s
```

JSON view

```
➜ ghtopdep https://github.com/dropbox/dropbox-sdk-js --json
[{"url": "https://github.com/transloadit/uppy", "stars": 21191}, {"url": "https://github.com/codesandbox/codesandbox-client", "stars": 8386}, {"url": "https://github.com/joemccann/dillinger", "stars": 6491}, {"url": "https://github.com/keplergl/kepler.gl", "stars": 5615}, {"url": "https://github.com/jitsi/jitsi-meet", "stars": 4303}, {"url": "https://github.com/jsbin/jsbin", "stars": 3947}, {"url": "https://github.com/NorthwoodsSoftware/GoJS", "stars": 3692}, {"url": "https://github.com/buttercup/buttercup-desktop", "stars": 3054}, {"url": "https://github.com/openstyles/stylus", "stars": 2219}, {"url": "https://github.com/mickael-kerjean/filestash", "stars": 1869}]
```

you can sort packages and fetch their description

```
➜ ghtopdep https://github.com/dropbox/dropbox-sdk-js --description --packages
| url                                            | stars   | description                                                  |
|------------------------------------------------|---------|--------------------------------------------------------------|
| https://github.com/jsbin/jsbin                 | 4.0K    | Collaborative JavaScript Debugging App                       |
| https://github.com/jvilk/BrowserFS             | 1.9K    | BrowserFS is an in-browser filesystem that emulates the...   |
| https://github.com/coderaiser/cloudcmd         | 1.1K    | ✨☁️📁✨ Cloud Commander file manager for the web with...       |
| https://github.com/node-red/node-red-web-nodes | 153     | A collection of node-red nodes aimed at web services         |
| https://github.com/robertknight/passcards      | 133     | A 1Password-compatible command-line and web-based...         |
| https://github.com/enyojs/ares-project         | 125     | A browser-based code editor and UI designer for Enyo 2...    |
| https://github.com/transloadit/uppy-server     | 114     | [DEPRECATED] 'Uppy Server' was renamed to 'Companion' and... |
| https://github.com/bioimagesuiteweb/bisweb     | 34      | This is the repository for the BioImage Suite Web Project    |
| https://github.com/sallar/dropbox-fs           | 30      | :package: Node FS wrapper for Dropbox                        |
| https://github.com/filefog/filefog             | 26      | A thin cloud-service agnostic wrapper/interface to access... |
found 140 packages others packages are private
found 61 packages with more than zero star
```

also ghtopdep support code searching at dependents (repositories/packages)

```
➜ ghtopdep https://github.com/rob-balfre/svelte-select --search=isMulti --minstar=0
https://github.com/andriyor/linkorg-frontend/blob/7eed49c332f127c8541281b85def80e54c882920/src/App.svelte with 0 stars
https://github.com/andriyor/linkorg-frontend/blob/7eed49c332f127c8541281b85def80e54c882920/src/providers/Post.svelte with 0 stars
https://github.com/jdgaravito/bitagora_frontend/blob/776a23f5e848995d3eba90563d55c96429470c48/src/Events/AddEvent.svelte with 0 stars
https://github.com/gopear/OlcsoSor/blob/b1fa1d877a59f7daf41a86fecb21137c91652d77/src/routes/index.svelte with 3 stars
https://github.com/openstate/allmanak/blob/ff9ac0833e5e63f7c17f99c5c2355b4e46c48148/app/src/routes/index.svelte with 3 stars
https://github.com/openstate/allmanak/blob/e6d7aa72a8878eefc6f63a27c983894de1cef294/app/src/components/ReportForm.svelte with 3 stars
https://github.com/wolbodo/members/blob/d091f1e44b4e8cb8cc31f39ea6f6e9c36211d019/sapper/src/components/Member.html with 1 stars
```

## Development setup

Using [Poetry](https://poetry.eustace.io/docs/)

```
$ poetry install
$ poetry run ghtopdep https://github.com/dropbox/dropbox-sdk-js
$ dephell deps convert --from=pyproject.toml --to=setup.py
$ poetry build
$ poetry publish
```

or [Pipenv](https://docs.pipenv.org/)

```
$ pipenv install --dev -e .
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
