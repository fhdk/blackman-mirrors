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


def format_mirror(data):
    """Format mirror from blackarch text file
    :param data: sample FR|https://blackarch.org/blackarch/$repo/os/$arch|blackarch
    :return: server info in dictionary
    :rtype: dict
    """
    works = data.split("|")
    proto = get_protocol(works[1])
    url = get_url(works[1])
    server = {
        "country": "{} - {}".format(works[0], works[2]),
        "url": "{}".format(url),
        "protocols": "{}".format(proto)
    }
    return server


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


def get_url(data):
    """Extract mirror url from data"""
    line = data.strip()
    if line.startswith("Server"):
        return line[9:].replace("$branch/$repo/$arch", "")
