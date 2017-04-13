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

"""Manjaro-Mirrors HTTP Functions"""

import collections
import json
import time
import ssl
from http.client import HTTPException
from os import system as system_call
from socket import timeout
from urllib.error import URLError
from urllib.request import urlopen

from . import configuration as conf
from . import filefn
from . import jsonfn
from . import bafn
from . import txt


def download_mirrors(config):
    """Retrieve mirrors from manjaro.org
    :param config:
    :returns: bool with success
    :rtype: bool
    """
    fetchmirrors = False
    try:
        with urlopen(config["url_mirror_list"]) as response:
            mirrorlist = response.read().decode("utf8")
            mirrorlist = bafn.format_mirror(mirrorlist)
        fetchmirrors = True
        jsonfn.write_json_file(mirrorlist, config["mirror_file"])
    except (HTTPException, json.JSONDecodeError, URLError):
        pass

    return fetchmirrors


def get_geoip_country():
    """Try to get the user country via GeoIP
    :return: country name or nothing
    """
    country_code = None
    try:
        res = urlopen("http://freegeoip.net/json/")
        json_obj = json.loads(res.read().decode("utf8"))
    except (URLError, HTTPException, json.JSONDecodeError):
        pass
    else:
        if "country_code" in json_obj:
            country_code = json_obj["country_code"]
    return country_code


def get_mirror_response(url, maxwait=2, count=1, quiet=False, ssl_verify=True):
    """Query mirrors availability
    :param ssl_verify: 
    :param ssl_verify: 
    :param url:
    :param maxwait:
    :param count:
    :param quiet:
    :returns string with response time
    """

    # ssl.verify_mode = ssl.CERT_NONE
    context = None
    if not ssl_verify:
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.verify_mode = ssl.CERT_NONE

    probe_start = time.time()
    response_time = txt.SERVER_RES
    probe_stop = None
    message = ""
    try:
        for _ in range(count):
            urlopen(url, timeout=maxwait, context=context)
        probe_stop = time.time()
    except URLError as err:
        if hasattr(err, "reason"):
            message = "\n.: {} {} '{}'".format(txt.ERR_CLR,
                                               err.reason,
                                               url)
        elif hasattr(err, "code"):
            message = "\n.: {} {} '{}'".format(txt.ERR_CLR,
                                               err.reason,
                                               url)
    except timeout:
        message = "\n.: {} {} '{}'".format(txt.ERR_CLR,
                                           txt.TIMEOUT,
                                           url)
    except HTTPException:
        message = "\n.: {} {} '{}'".format(txt.ERR_CLR,
                                           txt.HTTP_EXCEPTION,
                                           url)
    if message and not quiet:
        print(message)
    if probe_stop:
        calc = round((probe_stop - probe_start), 3)
        response_time = str(format(calc, ".3f"))
    return response_time


def is_connected(remote_host, maxwait=2):
    """Check for internet connection"""
    data = None
    # noinspection PyBroadException
    try:
        data = urlopen(remote_host, timeout=maxwait)
    except:
        pass
    return bool(data)


def ping_host(host, count=1):
    """Check a hosts availability
    :param host:
    :param count:
    :rtype: boolean
    """
    print(".: {} ping {} x {}".format(txt.INF_CLR, host, count))
    return system_call("ping -c{} {} > /dev/null".format(count, host)) == 0


def update_mirrors(config):
    """Download updates from repo.manjaro.org
    :param config:
    :returns: tuple with result for mirrors.json and status.json
    :rtype: tuple
    """
    result = None
    connected = is_connected("https://blackarch.org")
    if connected:
        print(".: {} {} {}".format(txt.INF_CLR,
                                   txt.DOWNLOADING_MIRROR_FILE,
                                   txt.REPO_SERVER))
        result = download_mirrors(config)
    else:
        if not filefn.check_file(config["mirror_file"]):
            print(".: {} {} {} {}".format(txt.WRN_CLR,
                                          txt.MIRROR_FILE,
                                          config["mirror_file"],
                                          txt.IS_MISSING))
            print(".: {} {} {}".format(txt.WRN_CLR,
                                       txt.FALLING_BACK,
                                       conf.FALLBACK))
            result = (True, False)
        if not filefn.check_file(config["fallback_file"]):
            print(".: {} {}".format(txt.ERR_CLR, txt.HOUSTON))
            result = (False, False)
    return result
