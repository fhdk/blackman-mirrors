#!/usr/bin/env python3
# blackman-mirrors is a fork of Manjaro pacman-mirrors
"""
test_blackman-mirrors
----------------------------------

Tests for `blackman-mirrors` module.
"""

import unittest
from unittest.mock import patch

from blackman_mirrors.blackman_mirrors import PacmanMirrors
from blackman_mirrors import configfn
from . import mock_configuration as conf


class TestDefaultConfig(unittest.TestCase):
    """Pacman Mirrors Test suite"""
    def setUp(self):
        """Setup tests"""
        pass

    @patch("os.getuid")
    @patch.object(configfn, "build_config")
    def test_default_method(self, mock_build_config, mock_os_getuid):
        """TEST: config[method] = rank"""
        mock_os_getuid.return_value = 0
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
                                  "-g"]):
            app = PacmanMirrors()
            app.config["config_file"] = conf.CONFIG_FILE
            app.config = configfn.build_config()
            assert app.config["method"] == "rank"

    @patch("os.getuid")
    @patch.object(configfn, "build_config")
    def test_default_mirrordir(self, mock_build_config, mock_os_getuid):
        """TEST: config[mirror_dir] = tests/mock/var/"""
        mock_os_getuid.return_value = 0
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
                                  "-g"]):
            app = PacmanMirrors()
            app.config = configfn.build_config()
            assert app.config["mirror_dir"] == "tests/mock/var/"

    @patch("os.getuid")
    @patch.object(configfn, "build_config")
    def test_default_mirrorfile(self, mock_build_config, mock_os_getuid):
        """TEST: config[mirror_file] = tests/mock/var/mirrors.json"""
        mock_os_getuid.return_value = 0
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
                                  "-g"]):
            app = PacmanMirrors()
            app.config = configfn.build_config()
            assert app.config["mirror_file"] == "tests/mock/var/mirrors.json"

    @patch("os.getuid")
    @patch.object(configfn, "build_config")
    def test_default_mirrorlist(self, mock_build_config, mock_os_getuid):
        """TEST: config[mirror_list] = tests/mock/etc/mirrorlist"""
        mock_os_getuid.return_value = 0
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
                                  "-g"]):
            app = PacmanMirrors()
            app.config = configfn.build_config()
            assert app.config["mirror_list"] == "tests/mock/etc/mirrorlist"

    @patch("os.getuid")
    @patch.object(configfn, "build_config")
    def test_default_noupdate(self, mock_build_config, mock_os_getuid):
        """TEST: config[no_update] = False"""
        mock_os_getuid.return_value = 0
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
                                  "-g"]):
            app = PacmanMirrors()
            app.config = configfn.build_config()
            assert app.config["no_update"] is False

    @patch("os.getuid")
    @patch.object(configfn, "build_config")
    def test_default_onlycountry(self, mock_build_config, mock_os_getuid):
        """TEST: config[only_country] = []"""
        mock_os_getuid.return_value = 0
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
                                  "-g"]):
            app = PacmanMirrors()
            app.config["config_file"] = conf.CONFIG_FILE
            app.config = configfn.build_config()
            assert app.config["only_country"] == []

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()
