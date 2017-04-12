#  Documentation of blackman-mirrors

Enhanced blackman-mirrors for Blackarch Linux

## Commands

`-h`, `--help`
Show the help message.

`-g`, `--generate`
Generate a new mirrorlist.

`-m [method]`, `--method [method]`
Choose the generation method:

- rank
- random

`-c [country]`, `--country [country]`
Choose the country to use:

- all
- FR
- FR,DE,AT

`--geoip`
Detect country by using geolocation.

`-d`, `--mirror_dir`
Change directory of mirrors to use.

`-f [n]`, `--fasttrack [n]`
Generates an updated and responsive mirrorlist of [n] mirrors.

`-l`, `--list`
Lists available mirror countries.

`-o`, `--output`
Change path of the output file.

`-t`, `--timeout`
Change the server maximum waiting time.

`--no-update`
Don't generate mirrorlist.

`-i`, `--interactive`
Launch a graphical tool to select mirrors to generate a custom mirrorlist.

`--default`
Used in conjunction with `-i/--interactive` ignores custom mirrorfile,  
loading the default mirrorfile and executes the ranking/randomizing process  
after the selection of mirrors.

`-v`, `--version`
Show the version of blackman-mirrors.

`--quiet`
Make blackman-mirrors silent.

`-a`, `--api` [--prefix] [{--get-branch | --set-branch}]

- `--prefix` for blackman-mirrors file-handling eg. /mnt/install or $mnt
- `--get-branch` returns branch from config in prefix`config_file`.   
   Don't use with `--branch` it defeats the purpose og `--getbranch`.
- `--set-branch` writes branch from `--branch` to prefix`config_file`

## blackman-mirrors.conf
```
## Generation method
## 1) rank   - rank mirrors depending on their access time
## 2) random - randomly generate the output mirrorlist
# Method = rank

## Specify to use only mirrors from specific a country.
## Can add multiple countries separated by a comma (ex: Germany,France)
## Empty means all
# OnlyCountry =

## Mirrors directory
# MirrorlistsDir = /var/lib/blackman-mirrors

## Output file
# OutputMirrorlist = /etc/pacman.d/blackman-mirrorlist

## When set to True prevents the regeneration of the mirrorlist if
## blackman-mirrors is invoked with the --no-update argument.
## Useful if you don't want the mirrorlist regenerated after a
## blackman-mirrors package upgrade.
# NoUpdate = False

# SSL = False
```
