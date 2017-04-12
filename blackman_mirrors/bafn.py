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


def format_mirror(data):
    """Format mirror from blackarch text file
    :param data: sample 'FR|https://blackarch.org/blackarch/$repo/os/$arch|blackarch'
    :return: server info in dictionary
    :rtype: dict
    """
    lines = data.split()
    mirrors = []
    for line in lines:
        server = line.split("|")
        mirror = {
            "country": "{}".format(server[0]),
            "name": "{}".format(server[2]),
            "url": "{}".format(get_url(server[1])),
            "protocols": ["{}".format(get_protocol(server[1]))]
        }
        mirrors.append(mirror)
    return filter_doubles(mirrors)


def filter_doubles(mirrorlist):
    """Remove doubles - instead add protocol to protocols
    :param mirrorlist: the list to be checked
    :return: new list
    sample data FR|http://blackarch.tamcore.eu/$repo/os/$arch|tamcore.eu
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


def get_server(url):
    """return servername from url"""
    pos = url.find(":")
    result = url[pos + 3:]
    pos = result.find("/")
    return result[:pos]


def get_protocol(data):
    """Extract protocol from url"""
    pos = data.find(":")
    return data[:pos]


def get_country(data):
    """Extract mirror country from data"""
    line = data.strip()
    if line.startswith("[") and line.endswith("]"):
        return line[1:-1]
    elif line.startswith("## Country") or line.startswith("## Location"):
        return line[19:]


def get_url(url):
    """Extract mirror url from data"""
    line = url.strip()
    pos = line.find(":")
    result = line[pos + 3:]
    return "{}".format(result.replace("$repo/os/$arch", ""))
