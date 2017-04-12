#!/usr/bin/env python3
# blackman-mirrors is a fork of Manjaro pacman-mirrors
"""
test_blackman-mirrors
----------------------------------

Tests for `blackman-mirrors` module.
"""

import unittest
from unittest.mock import patch

from blackman_mirrors import httpfn
from blackman_mirrors.blackman_mirrors import PacmanMirrors
from blackman_mirrors import configfn
from . import mock_configuration as conf


class TestHttpFn(unittest.TestCase):
    """Pacman Mirrors Test suite"""
    def setUp(self):
        """Setup tests"""
        pass

    @patch("os.getuid")
    @patch.object(httpfn, "get_geoip_country")
    @patch.object(configfn, "build_config")
    def test_geoip_available(self, mock_build_config, mock_get_geoip_country, mock_os_getuid):
        """TEST: Geoip country IS avaiable"""
        mock_os_getuid.return_value = 0
        mock_get_geoip_country.return_value = "FR"
        mock_build_config.return_value = {
            "branch": "stable",
            "branches": conf.BRANCHES,
            "config_file": conf.CONFIG_FILE,
            "custom_file": conf.CUSTOM_FILE,
            "fallback_file": conf.FALLBACK,
            "method": "rank",
            "mirror_dir": conf.MIRROR_DIR,
            "mirror_file": conf.MIRROR_FILE,
            "mirror_list": conf.MIRROR_LIST,
            "no_update": False,
            "only_country": [],
            "repo_arch": conf.REPO_ARCH,
            "ssl": False,
            "status_file": conf.STATUS_FILE,
            "url_mirror_list": conf.URL_MIRROR_JSON,
            "url_status_json": conf.URL_STATUS_JSON
        }
        with unittest.mock.patch("sys.argv",
                                 ["blackman-mirrors",
                                  "--geoip"]):
            app = PacmanMirrors()
            app.config = configfn.build_config()
            app.command_line_parse()
            app.load_all_mirrors()
            assert app.selected_countries == "FR"

    @patch("os.getuid")
    @patch.object(httpfn, "get_geoip_country")
    @patch.object(configfn, "build_config")
    def test_geoip_not_available(self, mock_build_config, mock_get_geoip_country, mock_os_getuid):
        """TEST: Geoip country IS NOT available"""
        mock_os_getuid.return_value = 0
        mock_get_geoip_country.return_value = "Antarctica"
        mock_build_config.return_value = {
            "branch": "stable",
            "branches": conf.BRANCHES,
            "config_file": conf.CONFIG_FILE,
            "custom_file": conf.CUSTOM_FILE,
            "fallback_file": conf.FALLBACK,
            "method": "rank",
            "mirror_dir": conf.MIRROR_DIR,
            "mirror_file": conf.MIRROR_FILE,
            "mirror_list": conf.MIRROR_LIST,
            "no_update": False,
            "only_country": [],
            "repo_arch": conf.REPO_ARCH,
            "ssl": False,
            "status_file": conf.STATUS_FILE,
            "url_mirror_list": conf.URL_MIRROR_JSON,
            "url_status_json": conf.URL_STATUS_JSON
        }
        with unittest.mock.patch("sys.argv",
                                 ["blackman-mirrors",
                                  "-g",
                                  "--geoip"]):
            app = PacmanMirrors()
            app.config = configfn.build_config()
            app.command_line_parse()
            app.load_all_mirrors()
            assert app.selected_countries == app.mirrors.countrylist

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()
