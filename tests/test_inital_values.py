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


class TestInitialValues(unittest.TestCase):
    """Pacman Mirrors Test suite"""
    def setUp(self):
        """Setup tests"""
        pass

    @patch("os.getuid")
    def test_initial_custom(self, mock_os_getuid):
        """TEST: self.custom is False"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["blackman-mirrors",
                                  "-g"]):
            app = PacmanMirrors()
            assert app.custom is False

    @patch("os.getuid")
    def test_initial_fasttrack(self, mock_os_getuid):
        """TEST: self.fasttrack is False"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["blackman-mirrors",
                                  "-g"]):
            app = PacmanMirrors()
            assert app.fasttrack is None

    @patch("os.getuid")
    def test_initial_geoip(self, mock_os_getuid):
        """TEST: self.geoip is False"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["blackman-mirrors",
                                  "-g"]):
            app = PacmanMirrors()
            assert app.geoip is False

    @patch("os.getuid")
    def test_initial_interactive(self, mock_os_getuid):
        """TEST: self.interactive is False"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["blackman-mirrors",
                                  "-g"]):
            app = PacmanMirrors()
            assert app.interactive is False

    @patch("os.getuid")
    def test_initial_max_wait_time(self, mock_os_getuid):
        """TEST: self.max_wait_time = 2"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["blackman-mirrors",
                                  "-g"]):
            app = PacmanMirrors()
            assert app.max_wait_time == 2

    @patch("os.getuid")
    def test_initial_network(self, mock_os_getuid):
        """TEST: self.network is True"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["blackman-mirrors",
                                  "-g"]):
            app = PacmanMirrors()
            assert app.network is True

    @patch("os.getuid")
    def test_initial_nodisplay(self, mock_os_getuid):
        """TEST: self.no_display is False"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["blackman-mirrors",
                                  "-g"]):
            app = PacmanMirrors()
            assert app.no_display is False

    @patch("os.getuid")
    def test_initial_quiet(self, mock_os_getuid):
        """TEST: self.quiet is False"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["blackman-mirrors",
                                  "-g"]):
            app = PacmanMirrors()
            assert app.quiet is False

    @patch("os.getuid")
    def test_initial_selected_countries(self, mock_os_getuid):
        """TEST: self.selected_countries = []"""
        mock_os_getuid.return_value = 0
        with unittest.mock.patch("sys.argv",
                                 ["blackman-mirrors",
                                  "-g"]):
            app = PacmanMirrors()
            assert app.selected_countries == []

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()
