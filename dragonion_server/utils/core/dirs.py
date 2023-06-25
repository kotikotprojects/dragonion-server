import os
import sys
import platform

from . import const


def dir_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size


def get_resource_path(filename):
    application_path = 'resources'

    return os.path.join(application_path, filename)


def get_tor_paths():
    from ..onion.tor_downloader import download_tor
    if platform.system() in ["Linux", "Darwin"]:
        tor_path = os.path.join(build_data_dir(), 'tor/tor')
    elif platform.system() == "Windows":
        tor_path = os.path.join(build_data_dir(), 'tor/tor.exe')
    else:
        raise "Platform not supported"

    if not os.path.isfile(tor_path):
        download_tor(dist=build_data_dir())

    return tor_path


def build_data_dir():
    dragonion_data_dir = 'data'

    os.makedirs(dragonion_data_dir, exist_ok=True)
    return dragonion_data_dir


def build_tmp_dir():
    tmp_dir = os.path.join(build_data_dir(), "tmp")
    os.makedirs(tmp_dir, exist_ok=True)
    return tmp_dir


def build_persistent_dir():
    persistent_dir = os.path.join(build_data_dir(), "persistent")
    os.makedirs(persistent_dir, exist_ok=True)
    return persistent_dir


def build_tor_data_dir():
    tor_dir = os.path.join(build_data_dir(), "tor_data")
    os.makedirs(tor_dir, exist_ok=True)
    return tor_dir
