# do not include __pydatk_dev - it should be called separately
from pydatk import new_module


def __get_versions():
    versions = (
        {
            'version': '0.0.0',
            'dt_utc': '2025-04-12'
        },
        {
            'version': '0.0.1-dev.1',
            'dt_utc': '2025-04-22'
        },
        {
            'version': '0.0.1-dev.2',
            'dt_utc': '2025-04-23'
        }
    )
    return versions

def __get_version_int():
    versions = __get_versions()
    version_int = len(versions) - 1
    return version_int

def get_version():
    versions = __get_versions()
    version_int = __get_version_int()
    version = versions[version_int]['version']
    return version