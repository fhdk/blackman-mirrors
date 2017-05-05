#!/usr/bin/env python3

import collections
import io
import json
import re
import os
from urllib.request import urlopen
from http.client import HTTPException
from socket import timeout
from urllib.error import URLError

from setuptools import setup

from blackman_mirrors import bafn


def update_mirror_file():
    """update mirrors from github"""
    mirrorlist = None
    try:
        with urlopen("https://raw.githubusercontent.com/BlackArch/blackarch/master/mirror/mirror.lst") as response:
            mirrorlist = response.read().decode("utf8")
            mirrorlist = bafn.format_mirror(mirrorlist)
    except (HTTPException, json.JSONDecodeError, URLError, timeout):
        pass
    if mirrorlist:
        with open("share/blackman-mirrors.json", "w") as outfile:
            json.dump(mirrorlist, outfile, indent=4, sort_keys=True)


def read(*names, **kwargs):
    """read"""
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    """find version"""
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

with open('README.md') as readme_file:
    README = readme_file.read()

with open('CHANGELOG.md') as changelog_file:
    CHANGELOG = changelog_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

update_mirror_file()

setup(
    name='blackman-mirrors',
    version=find_version("blackman_mirrors", "__init__.py"),
    description="Package that provides all mirrors for BlackArch Linux.",
    long_description=README + '\n\n' + CHANGELOG,
    author="Roland Singer, Esclapion, philm, Ramon Buldó, Hugo Posnic, Frede Hundewadt",
    author_email='f@hundewadt.dk',
    url='https://github.com/fhdk/blackman-mirrors',
    packages=['blackman_mirrors'],
    package_dir={'blackman_mirrors': 'blackman_mirrors'},
    data_files=[('/etc', ['conf/blackman-mirrors.conf']),
                ('/etc/pacman.d', []),
                ('share/blackman-mirrors', ['share/blackman-mirrors.json']),
                ('share/locale/bg/LC_MESSAGES', ['locale/bg/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/ca/LC_MESSAGES', ['locale/ca/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/cs/LC_MESSAGES', ['locale/cs/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/cy/LC_MESSAGES', ['locale/cy/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/da/LC_MESSAGES', ['locale/da/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/de/LC_MESSAGES', ['locale/de/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/el/LC_MESSAGES', ['locale/el/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/es/LC_MESSAGES', ['locale/es/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/es_419/LC_MESSAGES', ['locale/es_419/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/fr/LC_MESSAGES', ['locale/fr/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/hr/LC_MESSAGES', ['locale/hr/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/is/LC_MESSAGES', ['locale/is/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/is_IS/LC_MESSAGES', ['locale/is_IS/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/it/LC_MESSAGES', ['locale/it/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/lt/LC_MESSAGES', ['locale/lt/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/pl/LC_MESSAGES', ['locale/pl/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/ru_RU/LC_MESSAGES', ['locale/ru_RU/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/sk/LC_MESSAGES', ['locale/sk/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/sv/LC_MESSAGES', ['locale/sv/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/tr/LC_MESSAGES', ['locale/tr/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/tr_TR/LC_MESSAGES', ['locale/tr_TR/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/uk/LC_MESSAGES', ['locale/uk/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/uk_UA/LC_MESSAGES', ['locale/uk_UA/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/zh_TW/LC_MESSAGES', ['locale/zh_TW/LC_MESSAGES/pacman_mirrors.mo']),
                ],
    scripts=["scripts/blackman-mirrors"],
    install_requires=requirements,
    license="GPL3",
    zip_safe=False,
    keywords='blackman-mirrors',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End User/Desktop',
        'License :: OSI Approved :: GPL3 License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Environment :: Console'
    ],
    test_suite='tests',
    tests_require=test_requirements
)
