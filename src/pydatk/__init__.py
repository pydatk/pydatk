# use this for importing modules (see example import below)
# do not include dev - it should be called separately so dev features
# are not accessed accidentally
# from pydatk.module import *

# from pydatk import dev as dtkdev
# import pydatk as dtk

# TODO: fn for checking installed version against latest
# Download (from MAIN): https://github.com/pydatk/pydatk/blob/main/pyproject.toml
# Parse: https://docs.python.org/3/library/tomllib.html

_versions = [
    {
        'version': '0.0.0',
        'dt_utc': '2025-04-12',
        'pypi': {
            'dt_utc': '2025-04-12T06:53:03+0000',
            'url': 'https://pypi.org/project/pydatk/0.0.0/'
        },
        'github': {
            'dt_utc': '2025-04-18T02:53:00Z',
            'url': 'https://github.com/pydatk/pydatk/releases/tag/0.0.0',
            'is_prerelease': True
        }
    },
    {
        'version': '0.0.1',
        'dt_utc': 'TBC',
        'pypi': {
            'dt_utc': 'TBC',
            'url': 'TBC'
        },
        'github': {
            'dt_utc': 'TBC',
            'url': 'TBC',
            'is_prerelease': True
        }
    }
]

_version_int = len(_versions) - 1

version = _versions[_version_int]['version']