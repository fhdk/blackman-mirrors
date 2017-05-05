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
    servers = []
    if not mirrorlist:
        return mirrors
    mirrordata = mirrorlist.split("\n")
    for data in mirrordata:
        if not data:
            continue
        line = data.split("|")
        country = line[0]
        url = line[1]
        name = line[2]
        mirror = {
            "country": country,
            "name": name,
            "url": url,
            "server": get_server(url),
            "protocols": [get_protocol(url)]
        }
        if not mirror["server"] in servers:
            servers.append(mirror["server"])
        mirrors.append(mirror)

    return condensed_list(mirrors, servers)


def condensed_list(mirrorlist, serverlist):
    """Filter mirrors offering several protocols - add to protocols
    :param mirrorlist: the list to be checked
    :return: new list
    sample FR|http://blackarch.tamcore.eu/$repo/os/$arch|tamcore.eu
           FR|https://blackarch.tamcore.eu/$repo/os/$arch|tamcore.eu
    """
    mirrors = []

    for mirror in mirrorlist:
        if mirror["server"] in serverlist:
            try:
                idx = next(index for (index, d) in enumerate(mirrorlist) if d["server"] == mirror["server"])
                mirrors[idx]["protocols"] = mirrors[idx]["protocols"] + mirror["protocols"]
                mirrors[idx]["protocols"] = sorted(mirrors[idx]["protocols"], reverse=True)
            except:
                mirrors.append(mirror)
    return mirrors


def get_protocol(url):
    """Extract protocol from url"""
    pos = url.find("://")
    return url[:pos]


def get_server(url):
    """Extract server from url"""
    pos1 = url.find("://")
    server = url[pos1 + 3:]
    pos2 = server.find("/")
    server = server[:pos2]
    return server


def get_url(url):
    """Extract mirror url from data"""
    line = url.strip()
    pos = line.find("://")
    result = line[:pos + 3]
    return "{}".format(result.replace("/$repo/os/$arch", ""))

