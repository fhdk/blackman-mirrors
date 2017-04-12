## blackman-mirrors testpoints
### Geoip

* `--geoip -o geoip-mirrorlist.txt`
  - check `geoip-mirrorlist.txt` Should contain mirrors from geoip country
  - check `/etc/pacman-mirrors.conf` OnlyCountry should equal nothing
  
### Fasttrack

* `-f 5 -o fasttrack-5-mirrorlist.txt`
  - check `fasttrack-5-mirrorlist.txt` Should contain 5 mirrors - some hosts have several protocols
  - check `/etc/pacman-mirrors.conf` OnlyCountry should equal nothing
  
* `-i -o fasttrack-only_country_is_custom.txt`
  - select 2 mirrors and save
  - check `pacman-mirrors.conf` should have `OnlyCountry = Custom`
  - run `-f 5 -o fasttrack-only_country_is_custom.txt`
  - check `fasttrack-only_country_is_custom.txt` should countain 5 mirrors
  - check `pacman-mirrors.con` should have `OnlyCountry = Custom`

### Default generation method = rank

* `-g -b stable -o default-mirrorlist.txt`
  * `default-mirrorlist.txt` Should contain mirrors ranked by response time
   
### Single country

* `-c FR -o FR-mirrorlist.txt`
  - check `/etc/pacman-mirrors.conf` OnlyCountry should equal FR
  - check `FR-mirrorlist.txt` Should contain only mirrors from FR
  
### Single country method = random  
  
* `-c FR -m random -o FR-randommirrorlist.txt`
  - check `/etc/pacman-mirrors.conf` OnlyCountry should equal FR
  - check `FR-mirrorlist.txt` Should contain only, in random order, mirrors FR
  
### Single country interactive

* `-c FR -i -o FR-interactive-mirrorlist.txt`
  - action: select all mirrors from the list
  - check `/var/lib/pacman-mirrors/custom-mirrors.json` Should be created
  - check `FR-interactive-mirrorlist.txt` Should contain mirrors from FR
  - check `/etc/pacman-mirrors.conf` OnlyCountry should equal Custom
  
* `-c all -m random -o interactive-reset-mirrorlist.txt`
  - check `/var/lib/pacman-mirrors/custom-mirrors.json` Should be deleted
  - check `interactive-reset-mirrorlist` Should contain mirrors in random order
  - check `/etc/pacman-mirrors.conf` OnlyCountry should equal nothing

### Single mirror interactive

* `-c all -m random -o check-interactive-mirrorlist.txt`
  - action: select ONE mirror on the list 
  - check `/var/lib/pacman-mirrors/custom-mirrors.json` Should be created
  - check `/var/lib/pacman-mirrors/custom-mirrors.json` Should contain one mirror
  - check `check-interactive-mirrorlist` Should contain exactly one mirror - maybe several protocols
  - check `/etc/pacman-mirrors.conf` OnlyCountry should equal Custom
