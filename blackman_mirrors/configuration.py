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

"""blackman-mirrors Configuration"""

# # http constants
# URL_MIRROR_LIST = "https://raw.githubusercontent.com/BlackArch/blackarch/master/mirror/mirror.lst"
# # etc
# CONFIG_FILE = "/etc/blackman-mirrors.conf"
# MIRROR_LIST = "/etc/pacman.d/blackarch-mirrorlist"
# # blackman-mirrors
# MIRROR_DIR = "/var/lib/blackman-mirrors/"
# CUSTOM_FILE = "/var/lib/blackman-mirrors/custom-mirrors.json"
# MIRROR_FILE = "/var/lib/blackman-mirrors/blackman-mirrors.json"
# STATUS_FILE = "/var/lib/blackman-mirrors/status.json"
# # special cases
# FALLBACK = "/usr/share/blackman-mirrors/blackman-mirrors.json"
# # repo constants
# REPO_ARCH = "/$repo/os/$arch"

# blackman-mirrors is a fork of Manjaro pacman-mirrors
# http constants
URL_MIRROR_LIST = "https://raw.githubusercontent.com/BlackArch/blackarch/master/mirror/mirror.lst"
# URL_STATUS_JSON = "http://repo.manjaro.org/status.json"
# etc
CONFIG_FILE = "tests/mock/etc/blackman-mirrors.conf"
MIRROR_LIST = "tests/mock/etc/mirrorlist"
# blackman-mirrors
MIRROR_DIR = "tests/mock/var/"
CUSTOM_FILE = "tests/mock/var/custom-mirrors.json"
MIRROR_FILE = "tests/mock/var/blackman-mirrors.json"
STATUS_FILE = "tests/mock/var/blackman-status.json"
# special cases
FALLBACK = "tests/mock/usr/blackman-mirrors.json"
# repo constants
REPO_ARCH = "/$repo/os/$arch"
