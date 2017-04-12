#!/usr/bin/env python3
#
# This file is part of pacman-mirrors.
# blackman-mirrors is a fork of Manjaro pacman-mirrors
#
# pacman-mirrors is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pacman-mirrors is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pacman-mirrors.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Frede Hundewadt <f@hundewadt.dk>

"""blackman-mirrors Niscellaneous Functions"""
import shutil

from . import txt


def blue(where, what, value):
    """Helper for printing debug messages"""
    print("{}In function{} {} -> '{} = {}'".format(txt.BS,
                                                   where,
                                                   txt.CE,
                                                   what,
                                                   value))


def green(where, what, value):
    """Helper for printing debug messages"""
    print("{}In function{} {} -> '{} = {}'".format(txt.GS,
                                                   where,
                                                   txt.CE,
                                                   what,
                                                   value))


def yellow(where, what, value):
    """Helper for printing debug messages"""
    print("{}In function{} {} -> '{} = {}'".format(txt.YS,
                                                   where,
                                                   txt.CE,
                                                   what,
                                                   value))


def internet_message():
    """Message when internet connection is down"""
    print(".: {} {}".format(txt.WRN_CLR, txt.INTERNET_DOWN))
    print(".: {} {}".format(txt.INF_CLR, txt.INTERNET_REQUIRED))
    print(".: {} {}".format(txt.INF_CLR, txt.MIRROR_RANKING_NA))
    print(".: {} {}".format(txt.INF_CLR, txt.INTERNET_ALTERNATIVE))


def terminal_size():
    """get terminal size"""
    # http://www.programcreek.com/python/example/85471/shutil.get_terminal_size
    cols = shutil.get_terminal_size().columns
    lines = shutil.get_terminal_size().lines
    result = (cols, lines)
    return result
