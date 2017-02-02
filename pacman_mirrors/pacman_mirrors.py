#!/usr/bin/env python
#
# This file is part of pacman-mirrors.
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
# Authors   : Esclapion
#             philm
#             Ramon Buldó <rbuldo@gmail.com>
#             Hugo Posnic <huluti@manjaro.org>
#             Frede Hundewadt <frede@hundewadt.dk>

"""
Pacman-Mirrors
Main Module
"""

import argparse
import datetime
import importlib.util
import json
import os
import sys
import tempfile
import time
from http.client import HTTPException
from operator import itemgetter
from random import shuffle
from socket import timeout
from urllib.error import URLError
from urllib.request import urlopen

from pacman_mirrors import __version__
from . import i18n
from . import txt

from .custom_help_formatter import CustomHelpFormatter

# The interactive argument will be only available if Gtk is installed
try:
    importlib.util.find_spec("gi.repository.Gtk")
except ImportError:
    GTK_AVAILABLE = False
else:
    GTK_AVAILABLE = True

_ = i18n.language.gettext


class PacmanMirrors:
    """
    Class PacmanMirrors
    """

    def __init__(self):
        """ Init """
        # Lists
        self.available_countries = []
        self.good_servers = []  # respond updated < 24h
        self.resp_servers = []  # respond updated > 24h
        self.bad_servers = []   # no response timeout > max_wait_time
        # Decisions
        self.geolocation = False
        self.interactive = False
        self.quiet = False
        self.no_display = False
        # Time out
        self.max_wait_time = 2
        # Files and dirs
        self.config_file = "/etc/pacman-mirrors.conf"
        self.default_mirror_dir = "/etc/pacman.d/mirrors"
        self.default_mirror_list = "/etc/pacman.d/mirrorlist"
        self.custom_mirror_dir = "/var/lib/pacman-mirrors"
        self.custom_mirror_file = "/var/lib/pacman-mirrors/Custom"
        # Get config from file
        self.config = self.config_init()

    def append_to_server_list(self, mirror, mirror_last_sync):
        """
        Append mirror to relevant list based on elapsed hours

        :param: mirror: object{}
        :param: response_time: mirror response time
        """
        elapsed_hours = int(mirror_last_sync[:-3])
        if elapsed_hours <= int(txt.LASTSYNC_OK[:-3]):
            self.good_servers.append(mirror)
        elif elapsed_hours <= int(txt.LASTSYNC_NA[:-3]):
            self.resp_servers.append(mirror)
        elif elapsed_hours == int(txt.SERVER_BAD[:-3]):
            self.bad_servers.append(mirror)

    def command_line_parse(self):
        """
        Read the arguments of the command line
        """
        parser = argparse.ArgumentParser(formatter_class=CustomHelpFormatter)
        parser.add_argument("-g", "--generate",
                            action="store_true",
                            help=txt.HLP_ARG_GENERATE)
        parser.add_argument("-m", "--method",
                            type=str,
                            choices=["rank", "random"],
                            help=txt.HLP_ARG_METHOD)
        parser.add_argument("-b", "--branch",
                            type=str,
                            choices=["stable", "testing", "unstable"],
                            help=txt.HLP_ARG_BRANCH)
        parser.add_argument("-c", "--country",
                            type=str,
                            help=txt.HLP_ARG_COUNTRY)
        parser.add_argument("--geoip",
                            action="store_true",
                            help=txt.HLP_ARG_GEOIP_P1 + txt.OPT_COUNTRY +
                            txt.HLP_ARG_GEOIP_P2)
        parser.add_argument("-d", "--mirror_dir",
                            type=str,
                            metavar=txt.PATH,
                            help=txt.HLP_ARG_PATH)
        parser.add_argument("-o", "--output",
                            type=str,
                            metavar=txt.FILE,
                            help=txt.HLP_ARG_FILE)
        parser.add_argument("-t", "--timeout",
                            type=int,
                            metavar=txt.SECONDS,
                            help=txt.HLP_ARG_TIMEOUT)
        parser.add_argument("--no-update",
                            action="store_true",
                            help=txt.HLP_ARG_NOUPDATE_P1 + txt.OPT_NOUPDATE +
                            txt.HLP_ARG_NOUPDATE_P2)
        parser.add_argument("-i", "--interactive",
                            action="store_true",
                            help=txt.HLP_ARG_INTERACTIVE)
        parser.add_argument("-v", "--version",
                            action="store_true",
                            help=txt.HLP_ARG_VERSION)
        parser.add_argument("-q", "--quiet",
                            action="store_true",
                            help=txt.HLP_ARG_QUIET)
        args = parser.parse_args()
        # start parsing
        if len(sys.argv) == 1:
            parser.print_help()
            exit(0)

        if args.version:
            print("pacman-mirrors {}".format(__version__))
            exit(0)

        if os.getuid() != 0:
            print(txt.ERROR + txt.SEP + txt.ERR_NOT_ROOT)
            exit(1)

        if args.no_update:
            if self.config["no_update"] == "True":
                exit(0)

        if args.method:
            self.config["method"] = args.method

        if args.branch:
            self.config["branch"] = args.branch

        if args.mirror_dir:
            self.config["mirror_dir"] = args.mirror_dir
            self.default_mirror_dir = self.config["mirror_dir"]

        self.available_countries = self.get_available_countries(
            self.config["mirror_dir"])

        if args.geoip:
            self.geolocation = True

        if args.country:
            country = args.country.split(",")
            if country == ["Custom"]:
                self.config["only_country"] = country
            elif country == ["all"]:
                self.config["only_country"] = []
            else:
                try:
                    self.validate_country_list(
                        country, self.available_countries)
                    self.config["only_country"] = country
                except argparse.ArgumentTypeError as err:
                    parser.error(err)

        if args.output:
            if args.output[0] == "/":
                self.config["mirror_list"] = args.output
            else:
                self.config["mirror_list"] = os.getcwd() + "/" + args.output
            self.default_mirror_list = self.config["mirror_list"]

        if GTK_AVAILABLE and (
                os.environ.get('DISPLAY') is not None) and args.interactive:
            self.interactive = True

        if args.interactive and (os.environ.get("DISPLAY") is None):
            self.interactive = True
            self.no_display = True

        if args.timeout:
            self.max_wait_time = args.timeout

        if args.quiet:
            self.quiet = True

    def config_init(self):
        """
        Get config informations
        """
        # initialising defaults
        # information which can differ from these defaults
        # is fetched from config file
        config = {
            "branch": "stable",
            "method": "rank",
            "only_country": [],
            "mirror_dir": "/etc/pacman.d/mirrors",
            "mirror_list": "/etc/pacman.d/mirrorlist",
            "no_update": False,
        }
        try:
            # read configuration from file
            with open(self.config_file) as conf:
                for line in conf:
                    line = line.strip()
                    if line.startswith("#") or "=" not in line:
                        continue
                    (key, value) = line.split("=", 1)
                    key = key.rstrip()
                    value = value.lstrip()
                    if key and value:
                        if value.startswith("\"") and value.endswith("\""):
                            value = value[1:-1]
                        if key == "Method":
                            config["method"] = value
                        elif key == "Branch":
                            config["branch"] = value
                        elif key == "OnlyCountry":
                            config["only_country"] = value.split(",")
                        elif key == "MirrorlistsDir":
                            config["mirror_dir"] = value
                        elif key == "OutputMirrorlist":
                            config["mirror_list"] = value
                        elif key == "NoUpdate":
                            config["no_update"] = value
        except (PermissionError, OSError) as err:
            print(txt.ERROR + txt.SEP + txt.ERR_FILE_READ + txt.SEP +
                  "{filename}" + txt.SEP +
                  "{error}".format(filename=err.filename,
                                   error=err.strerror))
        return config

    def generate_mirror_list_common(self):
        """
        Generate common mirrorlist
        """
        if len(self.good_servers) >= 3:  # Avoid an empty mirrorlist
            server_list = self.good_servers
        elif len(self.resp_servers) >= 3:
            server_list = (self.good_servers + self.resp_servers)
        else:
            server_list = (self.good_servers + self.resp_servers +
                           self.bad_servers)
        if not server_list:
            print(txt.NEWLINE +
                  txt.ERROR + txt.SEP + txt.ERR_SERVER_NOT_AVAILABLE +
                  txt.NEWLINE)
        else:
            # modify configuration to use default
            self.modify_config()  # function do self check
            self.output_mirror_list(server_list, write_file=True)

    def generate_mirror_list_interactive(self):
        """
        Prompt the user to select the mirrors with a gui.

        * Write the mirrorlist file,
        * Write "Custom" mirror file
        * Modify the configuration file to use the "Custom" file.
        """
        # concat good servers and responding servers
        server_list = self.good_servers + self.resp_servers + self.bad_servers
        server_list = sorted(server_list, key=itemgetter("response_time"))

        if self.no_display is True:
            from . import console_ui
            interactive = console_ui.run(server_list)
        else:
            from . import graphical_gui
            interactive = graphical_gui.run(server_list)

        server_list = interactive.custom_list

        if not interactive.is_done:
            return

        print(txt.NEWLINE +
              txt.DCS + txt.INF_INTERACTIVE_LIST)
        print("--------------------------")
        # restore self.config["only_country"] to "Custom"
        self.config["only_country"] = ["Custom"]
        self.output_custom_mirror_file(server_list)
        self.output_mirror_list(server_list, write_file=True)
        # modify configuration to use custom
        self.modify_config()  # function do self check
        print(txt.DCS + txt.INF_INTERACTIVE_LIST_SAVED + txt.SEP +
              "{path}".format(path=self.custom_mirror_file))

    def load_server_lists(self):
        """
        Generate a list of servers

        It will only use mirrors defined in only_country, and if empty will
        use all mirrors.
        """
        if self.config["only_country"]:
            if self.config["only_country"] == ["Custom"]:
                if os.path.isfile(self.custom_mirror_file):
                    self.config["only_country"] = [self.custom_mirror_file]
                else:
                    print(txt.WARN + txt.SEP + txt.INF_CUSTOM_MIRROR_FILE +
                          " '{path}' ".format(path=self.custom_mirror_file) +
                          txt.INF_DOES_NOT_EXIST)
                    print(txt.NEWLINE)
                    self.config["only_country"] = []
            elif self.config["only_country"] == ["all"]:
                self.config["only_country"] = []

        if not self.config["only_country"]:
            if self.geolocation:
                geoip_country = self.get_geoip_country()
                if geoip_country and geoip_country in self.available_countries:
                    self.config["only_country"] = [geoip_country]
                else:
                    self.config["only_country"] = self.available_countries
            else:
                self.config["only_country"] = self.available_countries

        if self.config["method"] == "rank":
            self.query_servers(self.config["only_country"])
        elif self.config["method"] == "random":
            self.random_servers(self.config["only_country"])

    def modify_config(self):
        """
        Modify configuration

        :param: custom: modify configuration based on custom
        """
        if self.config["only_country"] == self.available_countries:
            # default
            self.config_set_default(self.config_file)
            # remove obsolete custom mirror file
            if os.path.isfile(self.custom_mirror_file):
                os.remove(self.custom_mirror_file)
                os.rmdir(self.custom_mirror_dir)
        else:
            # custom
            self.config_set_custom(
                self.config_file, self.config["only_country"])

    def output_custom_mirror_file(self, servers):
        """
        Write a custom mirror file in custom mirror dir
        """
        mirror_file = self.custom_mirror_file

        os.makedirs(self.custom_mirror_dir, mode=0o755, exist_ok=True)
        try:
            with open(mirror_file, "w") as output:
                print(txt.DCS + txt.INF_OUTPUT_MIRROR_FILE)
                self.write_mirror_list_header(output, custom=True)
                for server in servers:
                    self.write_mirror_list_entry(output, server)

        except OSError as err:
            print(txt.ERROR + txt.SEP + txt.ERR_FILE_WRITE + txt.SEP +
                  "{filename}" + txt.SEP +
                  "{error}".format(filename=err.filename,
                                   error=err.strerror))
            exit(1)

    def output_mirror_list(self, servers, write_file=False):
        """
        Write servers to /etc/pacman.d/mirrorlist

        :param: servers: list of servers to write
        :param: write_file: if "True" the list is written to disk
        """
        mirror_list = self.config["mirror_list"]
        try:
            with open(mirror_list, "w") as outfile:
                if write_file:
                    print(txt.DCS + txt.INF_MIRROR_LIST_WRITE)
                    self.write_mirror_list_header(outfile)
                for server in servers:
                    if write_file:
                        # insert selected branch in url
                        server["url"] = server["url"].replace(
                            "$branch", self.config["branch"])
                        self.write_mirror_list_entry(outfile, server)
                        if not self.quiet:
                            print(txt.DAS + "{} : {}".format(
                                server["country"], server["url"]))
                print(txt.DCS + txt.INF_MIRROR_LIST_SAVED + txt.SEP +
                      "{output_file}".format(output_file=mirror_list))

        except OSError as err:
            print(txt.ERROR + txt.SEP + txt.ERR_FILE_WRITE + txt.SEP +
                  "{filename}" + txt.SEP +
                  "{error}".format(
                      filename=err.filename, error=err.strerror))
            exit(1)

    def query_servers(self, countries):
        """
        Query the servers and put them in good_server, resp_server and
        bad_server depending on quality, and sort them by response time.

        :param countries: list of country files to use
        """
        print(txt.DCS + txt.INF_QUERY_TIME_INFO)
        for country in countries:
            if "Custom" in country:
                custom = True
                print(txt.SAS + txt.INF_QUERY_CUSTOM)
            else:
                custom = False
                print(txt.SAS + txt.INF_QUERY_DEFAULT + " {}".format(country))
            # create a ref point for calculation
            ref_point_in_time = datetime.datetime.utcnow()
            try:
                with open(os.path.join(
                    self.default_mirror_dir, country), "r") as mirrorfile:

                    for line in mirrorfile:
                        mirror_country = self.get_mirror_country(line)
                        if mirror_country:
                            country = mirror_country
                            continue
                        server_url = self.get_mirror_url(line)
                        if not server_url:
                            continue
                        server = {"country": country,
                                  "response_time": txt.SERVER_RES,
                                  "last_sync": txt.SERVER_BAD,
                                  "url": server_url}
                        # create a probe start reference point
                        probe_start = time.time()
                        statefile_content = self.query_mirror_state(
                            server["url"], self.config["branch"],
                            self.max_wait_time, self.quiet)
                        # calculate response time
                        server_response_time = self.get_mirror_response_time(
                            probe_start, time.time())
                        if not self.quiet:
                            if custom:
                                print(
                                    txt.DAS +
                                    "{s_ctry} - {s_rt} - {s_url}".format(
                                        s_ctry=country,
                                        s_rt=server_response_time,
                                        s_url=server_url.replace(
                                            "$branch", self.config["branch"])))
                            else:
                                print(txt.DAS + "{s_rt} - {s_url}".format(
                                    s_rt=server_response_time,
                                    s_url=server_url.replace(
                                        "$branch", self.config["branch"])))
                        if not statefile_content:
                            self.append_to_server_list(
                                server, server["last_sync"])
                            continue
                        server["response_time"] = server_response_time
                        # extract timestamp from statefile
                        statefile_timestamp = self.get_mirror_branch_timestamp(
                            statefile_content)
                        try:
                            branch_timestamp = datetime.datetime.strptime(
                                statefile_timestamp, "%Y-%m-%dT%H:%M:%S")
                        except ValueError:
                            server["last_sync"] = txt.LASTSYNC_NA
                            self.append_to_server_list(
                                server, server["last_sync"])
                            if not self.quiet:
                                print(
                                    txt.NEWLINE +
                                    txt.WARN +
                                    txt.SEP +
                                    txt.INF_QUERY_WRONG_DATE_FORMAT)
                            continue
                        server["last_sync"] = self.get_mirror_branch_last_sync(
                            ref_point_in_time, branch_timestamp)
                        self.append_to_server_list(server, server["last_sync"])
            except OSError as err:
                print(txt.ERROR + txt.SEP + txt.ERR_FILE_READ + txt.SEP +
                      "{filename}" + txt.SEP +
                      "{error}".format(filename=err.filename,
                                       error=err.strerror))
                continue
        self.good_servers = sorted(self.good_servers,
                                   key=itemgetter("response_time"))
        self.resp_servers = sorted(self.resp_servers,
                                   key=itemgetter("response_time"))

    def random_servers(self, countries):
        """
        Add all servers to bad_servers and shuffle them randomly.

        :param countries: list of country files to use
        """
        print(txt.DCS + txt.INF_RANDOMIZE_SERVERS)
        for country in countries:
            try:
                with open(os.path.join(
                        self.default_mirror_dir, country), "r") as conf:

                    for line in conf:
                        m_country = self.get_mirror_country(line)
                        if m_country:
                            country = m_country
                            continue
                        m_url = self.get_mirror_url(line)
                        if not m_url:
                            continue
                        server = {"country": country,
                                  "response_time": txt.SERVER_RES,
                                  "last_sync": txt.SERVER_BAD,
                                  "url": m_url}
                        self.append_to_server_list(server, txt.SERVER_RES)
            except OSError as err:
                print(txt.ERROR + txt.SEP + txt.ERR_FILE_READ + txt.SEP +
                      "{filename}" + txt.SEP +
                      "{error}".format(filename=err.filename,
                                       error=err.strerror))
                continue
        shuffle(self.bad_servers)

    # ----------------------------------------------------------------
    # Begin static methods
    # ----------------------------------------------------------------
    @staticmethod
    def config_set_custom(config_file, config_only_country):
        """
        Use custom configuration
        """
        for country in config_only_country:
            if "Custom" in country:  # country is full path
                country = "Custom"  # must change to Custom
        country_list = ("OnlyCountry = {list}\n").format(
            list=",".join(config_only_country))
        try:
            with open(config_file) as cnf, tempfile.NamedTemporaryFile(
                    "w+t", dir=os.path.dirname(config_file),
                    delete=False) as tmp:

                replaced = False
                for line in cnf:
                    if "OnlyCountry" in line:
                        tmp.write(country_list)
                        replaced = True
                    else:
                        tmp.write("{}".format(line))
                if not replaced:
                    tmp.write(country_list)
            os.replace(tmp.name, config_file)
            os.chmod(config_file, 0o644)

        except OSError as err:
            print(txt.ERROR + txt.SEP + txt.ERR_FILE_UPDATE + txt.SEP +
                  "{filename}" + txt.SEP +
                  "{error}".format(filename=err.filename,
                                   error=err.strerror))
            exit(1)

    @staticmethod
    def config_set_default(config_file):
        """
        Use default configuration
        """
        with open(config_file) as cnf, tempfile.NamedTemporaryFile(
                "w+t", dir=os.path.dirname(config_file),
                delete=False) as tmp:

            for line in cnf:
                if "=" not in line:
                    tmp.write("{}".format(line))
                else:
                    key = [x.strip() for x in line.split("=", 1)[0]]
                    if key == "OnlyCountry":
                        tmp.write("# OnlyCountry = \n")
                    else:
                        tmp.write("{}".format(line))
        os.replace(tmp.name, config_file)
        os.chmod(config_file, 0o644)

    @staticmethod
    def get_available_countries(country_dir):
        """
        Returns a sorted list of countries.
        The name of mirror file is the country.

        :param country_dir: path with the mirror list
        :return: list of countries
        """
        return sorted(os.listdir(country_dir))

    @staticmethod
    def get_geoip_country():
        """
        Try to get the user country via GeoIP

        :return: return country name or empty list
        """
        country_name = None
        try:
            res = urlopen("http://freegeoip.net/json/", timeout=2)
            json_obj = json.loads(res.read().decode("utf8"))
        except (URLError, timeout, HTTPException, json.JSONDecodeError):
            pass
        else:
            if "country_name" in json_obj:
                country_name = json_obj["country_name"]
                country_fix = {
                    "Brazil": "Brasil",
                    "Costa Rica": "Costa_Rica",
                    "Czech Republic": "Czech",
                    "South Africa": "Africa",
                    "United Kingdom": "United_Kingdom",
                    "United States": "United_States",
                }
                if country_name in country_fix.keys():
                    country_name = country_fix[country_name]
        return country_name

    @staticmethod
    def get_mirror_branch_last_sync(point_in_time, timestamp):
        """
        Calculates elapsed time

        :param: point_in_time: reference point
        :param: timestamp: timestamp
        :return: elapsed_time
        """
        total_seconds = (point_in_time - timestamp).total_seconds()
        total_minutes = total_seconds // 60
        elapsed_hours = total_minutes // 60
        elapsed_minutes = total_minutes % 60
        elapsed_time = "{}:{}".format(
            str(int(elapsed_hours)).zfill(2),
            str(int(elapsed_minutes)).zfill(2))
        return elapsed_time

    @staticmethod
    def get_mirror_branch_timestamp(data):
        """
        Extract date from state file

        :param: data: contents of state file
        :return: string with timestamp from file
        """
        position = data.find(b"date=")
        timestamp = data[position + 5:position + 24].decode("utf-8")
        return timestamp

    @staticmethod
    def get_mirror_country(data):
        """
        Extract mirror country from data

        :param: data
        :return: country
        """
        line = data.strip()
        if line.startswith("[") and line.endswith("]"):
            return line[1:-1]
        elif line.startswith("## Country") or line.startswith("## Location"):
            return line[19:]

    @staticmethod
    def get_mirror_response_time(start_time, stop_time):
        """
        Calculate response time

        :param: start_time
        :param: stop_time
        :return: probe_time
        """
        probe_time = round((stop_time - start_time), 3)
        probe_time = format(probe_time, ".3f")
        return str(probe_time)

    @staticmethod
    def get_mirror_url(data):
        """
        Extract mirror url from data

        :param: data
        :return: url
        """
        line = data.strip()
        if line.startswith("Server"):
            return line[9:]

    @staticmethod
    def query_mirror_state(state_url, mirror_branch, request_timeout, quiet):
        """
        Get statefile

        :param: mirror_url
        :return: content
        """
        content = ""
        _state_url = state_url.replace("$branch", mirror_branch)
        position = _state_url.find(mirror_branch)
        req = _state_url[0:position] + "state"
        try:
            res = urlopen(req, timeout=request_timeout)
            content = res.read()
        except URLError as err:
            if hasattr(err, "reason"):
                if not quiet:
                    print(txt.NEWLINE +
                          txt.ERROR + txt.SEP +
                          txt.ERR_SERVER_NOT_REACHABLE + txt.SEP +
                          "{}".format(err.reason))
            elif hasattr(err, "code"):
                if not quiet:
                    print(txt.NEWLINE +
                          txt.ERROR + txt.SEP +
                          txt.ERR_SERVER_REQUEST + txt.SEP +
                          "{}".format(err.errno))
        except timeout:
            if not quiet:
                print(txt.NEWLINE +
                      txt.ERROR + txt.SEP +
                      txt.ERR_SERVER_NOT_AVAILABLE + txt.SEP +
                      txt.TIMEOUT)
        except HTTPException:
            if not quiet:
                print(txt.NEWLINE +
                      txt.ERROR + txt.SEP +
                      txt.ERR_SERVER_HTTP_EXCEPTION +
                      txt.SEP + txt.HTTP_EXCEPTION)

        return content

    @staticmethod
    def validate_country_list(countries, available_countries):
        """
        Check if the list of countries are valid.

        :param countries: list of countries to check
        :param available_countries: list of available countries
        :raise argparse.ArgumentTypeError: if it finds and invalid country.
        """
        for country in countries:
            if country not in available_countries:
                msg = (txt.INF_OPTION + txt.OPT_COUNTRY +
                       txt.INF_UNKNOWN_COUNTRY + txt.SEP +
                       "'{country}'.\n".format(country=country) +
                       txt.NEWLINE +
                       txt.INF_AVAILABLE_COUNTRIES + txt.SEP +
                       "{country_list}".format(
                           country_list=", ".join(available_countries)))
                raise argparse.ArgumentTypeError(msg)

    @staticmethod
    def write_mirror_list_header(handle, custom=False):
        """
        Write mirrorlist header

        :param: handle: handle to a file opened for writing
        """
        handle.write("##\n")
        handle.write("## Manjaro Linux repository mirrorlist\n")
        handle.write("## Generated on {}\n"
                     .format(datetime.datetime.now()
                             .strftime("%d %B %Y %H:%M")))
        handle.write("##\n")
        handle.write("## Use pacman-mirrors to modify\n")
        if custom:
            handle.write("## Custom mirrorlist\n")
            handle.write("## Use 'pacman-mirrors -c all' to reset\n")
        handle.write("##\n\n")

    @staticmethod
    def write_mirror_list_entry(handle, mirror):
        """
        Write mirror to mirrorlist

        :param: handle: handle to a file opened for writing
        :param: mirror: mirror object
        """
        handle.write("## Country       : {}\n"
                     .format(mirror["country"]))
        if not mirror["response_time"] == txt.SERVER_RES:  # 99.99
            handle.write("## Response time : {}\n"
                         .format(mirror["response_time"]))
        if not mirror["last_sync"] == txt.SERVER_BAD:  # 99:99
            if mirror["last_sync"] == txt.LASTSYNC_NA:  # 98:00 N/A
                handle.write("## Last sync     : {}\n"
                             .format("N/A"))
            else:
                handle.write("## Last sync     : {}h\n"  # 24:00
                             .format(mirror["last_sync"]))
        handle.write("Server = {}\n\n"
                     .format(mirror["url"]))

    # ----------------------------------------------------------------
    # End static methods
    # ----------------------------------------------------------------

    def run(self):
        """ Run """
        self.command_line_parse()
        self.load_server_lists()
        if self.interactive:
            self.generate_mirror_list_interactive()
        else:
            self.generate_mirror_list_common()


if __name__ == "__main__":
    pm = PacmanMirrors()
    pm.run()
