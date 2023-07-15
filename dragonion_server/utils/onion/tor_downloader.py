import os
import io
import tarfile
import requests
import re
import sys
from typing import Literal


def get_latest_version() -> str:
    """
    Gets latest non-alfa version name from dist.torproject.org
    :return:
    """
    r = requests.get('https://dist.torproject.org/torbrowser/').text

    results = re.findall(r'<a href=".+/">(.+)/</a>', r)
    for res in results:
        if 'a' not in res:
            return res


def get_build() -> Literal[
    'windows-x86_64',
    'linux-x86_64',
    'macos-x86_64',
    'macos-aarch64'
]:
    """
    Gets proper build name for your system
    :return:
    """
    if sys.platform == 'win32':
        return 'windows-x86_64'
    elif sys.platform == 'linux':
        return 'linux-x86_64'
    elif sys.platform == 'darwin':
        import platform
        if platform.uname().machine == 'arm64':
            return 'macos-aarch64'
        else:
            return 'macos-x86_64'
    else:
        raise 'System not supported'


def get_tor_expert_bundles(version: str = get_latest_version(),
                           platform: str = get_build()):
    """
    Returns a link for downloading tor expert bundle by version and platform
    :param version: Tor expert bundle version that exists in dist.torproject.org
    :param platform: Build type based on platform and arch, can be generated using
                     get_build()
    :return:
    """
    return f'https://dist.torproject.org/torbrowser/{version}/tor-expert-bundle-' \
           f'{version}-{platform}.tar.gz'


def download_tor(url: str = get_tor_expert_bundles(), dist: str = 'tor'):
    """
    Downloads tor from url and unpacks it to specified directory. Note, that
    it doesn't unpack only tor executable to dist folder, but creates there
    tor folder, where tor executable and libs are stored
    :param url: Direct link for downloading
    :param dist: Directory where to unpack archive (tor folder will appear there)
    :return:
    """
    if not os.path.exists(dist):
        os.makedirs(dist)

    (tar := tarfile.open(fileobj=io.BytesIO(requests.get(url).content),
                         mode='r:gz')).extractall(
        members=[
            tarinfo
            for tarinfo
            in tar.getmembers()
            if tarinfo.name.startswith("tor/")
        ], path=dist)


if __name__ == '__main__':
    download_tor()
