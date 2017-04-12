# blackman-mirrors is a fork of Manjaro blackman-mirrors
#!/usr/bin/env bash
sudo blackman-mirrors --geoip -o geoip-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to geoip-mirrorlist.txt\e[m"
echo Verify checkpoint...
read -n 1
#
sudo blackman-mirrors -f 5 -o fasttrack-5-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to fasttrack-5-mirrorlist.txt\e[m"
echo Verify checkpoint...
read -n 1
sudo blackman-mirrors -i -o fasttrack-only_country_is_custom.txt
echo -e "\e[1m\e[41mResult was written to fasttrack-only_country_is_custom.txt\e[m"
echo Verify checkpoint...
read -n 1
sudo blackman-mirrors -f 5 -o fasttrack-only_country_is_custom.txt
echo -e "\e[1m\e[41mResult was written to fasttrack-only_country_is_custom.txt\e[m"
echo Verify checkpoint...
read -n 1
#
sudo blackman-mirrors -g -o default-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to default-stable-mirrorlist.txt\e[m"
echo Verify checkpoint...
read -n 1
#
sudo blackman-mirrors -c FR -o FR-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to FR-mirrorlist.txt\e[m"
echo Verify checkpoint...
read -n 1
#
sudo blackman-mirrors -c FR -m random -o FR-random-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to FR-random-mirrorlist.txt\e[m"
echo Verify checkpoint...
read -n 1
#
sudo blackman-mirrors -i -c FR -o FR-interactive-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to FR-interactive-mirrorlist.txt\e[m"
echo Verify checkpoint...
read -n 1
sudo blackman-mirrors -c all -m random -o interactive-reset-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to interactive-reset-mirrorlist.txt\e[m"
echo Verify checkpoint...
read -n 1
sudo blackman-mirrors -i -c all -m random -o check-interactive-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to check-len-interactive-mirrorlist.txt\e[m"
echo Verify checkpoint...
read -n 1

sudo chmod 0777 *-mirrorlist.txt

