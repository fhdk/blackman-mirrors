#!/usr/bin/env python3
#
# This file is part of blackman-mirrors.
# blackman-mirrors is a fork of Manjaro pacman-mirrors
#
# blackman-mirrors is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# blackman-mirrors is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with blackman-mirrors.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Frede Hundewadt <f@hundewadt.dk>

"""blackman-mirrors Mirrorlist Functions"""
from . import miscfn


def format_mirror(mirrorlist):
    """Format mirror from blackarch text file
    :param mirrorlist: sample FR|https://blackarch.org/blackarch/$repo/os/$arch|blackarch
    :return: server info in dictionary
    :rtype: dict
    """
    mirrors = []
    if not mirrorlist:
        return mirrors
    mirrordata = mirrorlist.split("|")
    for data in mirrordata:
        miscfn.blue("format_mirror", "data", mirrordata)
        exit()
        line = data.split("|")
        country = line[0]
        url = line[1]
        name = line[2]
        mirror = {
            "country": country,
            "name": name,
            "url": get_url(url),
            "protocols": [get_protocol(url)]
        }
        mirrors.append(mirror)

    return filter_doubles(mirrors)


def filter_doubles(mirrorlist):
    """Remove doubles - instead add protocol to protocols
    :param mirrorlist: the list to be checked
    :return: new list
    sample FR|http://blackarch.tamcore.eu/$repo/os/$arch|tamcore.eu
           FR|https://blackarch.tamcore.eu/$repo/os/$arch|tamcore.eu
    """
    mirrors = []
    for mirror in mirrorlist:
        if mirrors:
            for item in mirrors:
                if item["url"] == mirror["url"]:
                    for proto in enumerate(mirror["protocols"]):
                        item["protocols"].append(proto[1])
                    continue
            mirrors.append(mirror)
        else:
            mirrors.append(mirror)

    return mirrors


def get_protocol(url):
    """Extract protocol from url"""
    pos = url.find("://")
    return url[:pos]


def get_server(url):
    """Extract server from url"""
    pos = url.find("://")
    return url[pos + 3:]


def get_url(url):
    """Extract mirror url from data"""
    line = url.strip()
    pos = line.find("://")
    result = line[pos:]
    return "{}".format(result.replace("/$repo/os/$arch", ""))
