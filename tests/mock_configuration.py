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
MIRROR_FILE = "tests/mock/var/mirrors.json"
STATUS_FILE = "tests/mock/var/status.json"
# special cases
O_CUST_FILE = "tests/mock/var/Custom"
FALLBACK = "tests/mock/usr/mirrors.json"
# repo constants
REPO_ARCH = "/$repo/os/$arch"
