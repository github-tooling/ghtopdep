# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ghtopdep']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'cachecontrol>=0.12.5,<0.13.0',
 'click>=8.1.2,<9.0.0',
 'github3.py>=3.2.0,<4.0.0',
 'halo>=0.0.31,<0.0.32',
 'lockfile>=0.12.2,<0.13.0',
 'pipdate>=0.5.6,<0.6.0',
 'requests>=2.22,<3.0',
 'selectolax>=0.3.7,<0.4.0',
 'tabulate>=0.8.3,<0.9.0']

entry_points = \
{'console_scripts': ['ghtopdep = ghtopdep.ghtopdep:cli']}

setup_kwargs = {
    'name': 'ghtopdep',
    'version': '0.3.14',
    'description': 'CLI tool for sorting dependents repositories and packages by stars',
    'long_description': '# GHTOPDEP\n\n[![image](https://img.shields.io/pypi/v/ghtopdep.svg)](https://pypi.org/project/ghtopdep/)\n[![image](https://img.shields.io/pypi/l/ghtopdep.svg)](https://pypi.org/project/ghtopdep/)\n[![image](https://img.shields.io/pypi/pyversions/ghtopdep.svg)](https://pypi.org/project/ghtopdep/)\n\nCLI tool for sorting dependents repo by stars\n\n## Requirements\n\n- Python 3.5 and up\n- Python development libraries\n\n## Installation\n\nfrom PyPI\n\n```\n$ pip install ghtopdep\n```\n\nfrom git repository\n\n```\n$ pip install git+https://github.com/github-tooling/ghtopdep.git#egg=ghtopdep\n```\n\nfrom source\n\n```\n$ git clone https://github.com/github-tooling/ghtopdep\n$ cd ghtopdep\n$ python setup.py install\n```\n\n## Python development Installation\n\nUbuntu/Debian\n\n```\nsudo apt install python3-dev\n```\n\nCentOS/RHEL\n\n```\nsudo yum install python3-devel\n```\n\n## Version upgrade\n\n```\n➜ pip install --upgrade ghtopdep\n```\n\n## Usage\n\nIf you want retrieve packages or repositories description you need pass token.\nTo prevent rale limit being exceeded for unauthentIcated requests, ghtopdep needs an access token.\nFor public repositories, [create a token](https://github.com/settings/tokens/new?scopes=public_repo&description=ghtopdep)\nwith the public_repo permission.\n\nYou can use token as environment variable `GHTOPDEP_TOKEN` at `~/.bashrc` or `~/.zshrc`\n\nexport GHTOPDEP_TOKEN="**\\*\\*\\*\\***\\*\\***\\*\\*\\*\\***\\*\\*\\*\\***\\*\\*\\*\\***\\*\\***\\*\\*\\*\\***"\n\nor pass token as option --token\n\n```\n➜ ghtopdep --help\nUsage: ghtopdep [OPTIONS] URL\n\nOptions:\n  --repositories / --packages  Sort repositories or packages (default\n                               repositories)\n  --table / --json             View mode\n  --description                Show description of packages or repositories\n                               (performs additional request per repository)\n  --rows INTEGER               Number of showing repositories (default=10)\n  --minstar INTEGER            Minimum number of stars (default=5)\n  --search TEXT                search code at dependents\n                               (repositories/packages)\n  --token TEXT\n  --help                       Show this message and exit.\n```\n\nTable view (by default)\n\n```\n➜ ghtopdep https://github.com/dropbox/dropbox-sdk-js\n| url                                               | stars   |\n|---------------------------------------------------|---------|\n| https://github.com/transloadit/uppy               | 21K     |\n| https://github.com/codesandbox/codesandbox-client | 8.6K    |\n| https://github.com/joemccann/dillinger            | 6.5K    |\n| https://github.com/keplergl/kepler.gl             | 5.8K    |\n| https://github.com/jitsi/jitsi-meet               | 4.5K    |\n| https://github.com/jsbin/jsbin                    | 4.0K    |\n| https://github.com/NorthwoodsSoftware/GoJS        | 3.8K    |\n| https://github.com/buttercup/buttercup-desktop    | 3.1K    |\n| https://github.com/openstyles/stylus              | 2.3K    |\n| https://github.com/mickael-kerjean/filestash      | 2.0K    |\nfound 1660 repositories others repositories are private\nfound 443 repositories with more than zero star\n~ via ⬢ v12.5.0 via 🐘 v7.2.19 via 🐍 3.8.0 took 2m 57s\n```\n\nJSON view\n\n```\n➜ ghtopdep https://github.com/dropbox/dropbox-sdk-js --json\n[{"url": "https://github.com/transloadit/uppy", "stars": 21191}, {"url": "https://github.com/codesandbox/codesandbox-client", "stars": 8386}, {"url": "https://github.com/joemccann/dillinger", "stars": 6491}, {"url": "https://github.com/keplergl/kepler.gl", "stars": 5615}, {"url": "https://github.com/jitsi/jitsi-meet", "stars": 4303}, {"url": "https://github.com/jsbin/jsbin", "stars": 3947}, {"url": "https://github.com/NorthwoodsSoftware/GoJS", "stars": 3692}, {"url": "https://github.com/buttercup/buttercup-desktop", "stars": 3054}, {"url": "https://github.com/openstyles/stylus", "stars": 2219}, {"url": "https://github.com/mickael-kerjean/filestash", "stars": 1869}]\n```\n\nyou can sort packages and fetch their description\n\n```\n➜ ghtopdep https://github.com/dropbox/dropbox-sdk-js --description --packages\n| url                                            | stars   | description                                                  |\n|------------------------------------------------|---------|--------------------------------------------------------------|\n| https://github.com/jsbin/jsbin                 | 4.0K    | Collaborative JavaScript Debugging App                       |\n| https://github.com/jvilk/BrowserFS             | 1.9K    | BrowserFS is an in-browser filesystem that emulates the...   |\n| https://github.com/coderaiser/cloudcmd         | 1.1K    | ✨☁️📁✨ Cloud Commander file manager for the web with...       |\n| https://github.com/node-red/node-red-web-nodes | 153     | A collection of node-red nodes aimed at web services         |\n| https://github.com/robertknight/passcards      | 133     | A 1Password-compatible command-line and web-based...         |\n| https://github.com/enyojs/ares-project         | 125     | A browser-based code editor and UI designer for Enyo 2...    |\n| https://github.com/transloadit/uppy-server     | 114     | [DEPRECATED] \'Uppy Server\' was renamed to \'Companion\' and... |\n| https://github.com/bioimagesuiteweb/bisweb     | 34      | This is the repository for the BioImage Suite Web Project    |\n| https://github.com/sallar/dropbox-fs           | 30      | :package: Node FS wrapper for Dropbox                        |\n| https://github.com/filefog/filefog             | 26      | A thin cloud-service agnostic wrapper/interface to access... |\nfound 140 packages others packages are private\nfound 61 packages with more than zero star\n```\n\nalso ghtopdep support code searching at dependents (repositories/packages)\n\n```\n➜ ghtopdep https://github.com/rob-balfre/svelte-select --search=isMulti --minstar=0\nhttps://github.com/andriyor/linkorg-frontend/blob/7eed49c332f127c8541281b85def80e54c882920/src/App.svelte with 0 stars\nhttps://github.com/andriyor/linkorg-frontend/blob/7eed49c332f127c8541281b85def80e54c882920/src/providers/Post.svelte with 0 stars\nhttps://github.com/jdgaravito/bitagora_frontend/blob/776a23f5e848995d3eba90563d55c96429470c48/src/Events/AddEvent.svelte with 0 stars\nhttps://github.com/gopear/OlcsoSor/blob/b1fa1d877a59f7daf41a86fecb21137c91652d77/src/routes/index.svelte with 3 stars\nhttps://github.com/openstate/allmanak/blob/ff9ac0833e5e63f7c17f99c5c2355b4e46c48148/app/src/routes/index.svelte with 3 stars\nhttps://github.com/openstate/allmanak/blob/e6d7aa72a8878eefc6f63a27c983894de1cef294/app/src/components/ReportForm.svelte with 3 stars\nhttps://github.com/wolbodo/members/blob/d091f1e44b4e8cb8cc31f39ea6f6e9c36211d019/sapper/src/components/Member.html with 1 stars\n```\n\n## Development setup\n\nUsing [Poetry](https://poetry.eustace.io/docs/)\n\n```\n$ poetry install\n$ poetry run ghtopdep https://github.com/dropbox/dropbox-sdk-js\n$ dephell deps convert --from=pyproject.toml --to=setup.py\n$ poetry build\n$ poetry publish\n```\n\nor [Pipenv](https://docs.pipenv.org/)\n\n```\n$ pipenv install --dev -e .\n```\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n',
    'author': 'Andriy Orehov',
    'author_email': 'andriyorehov@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

