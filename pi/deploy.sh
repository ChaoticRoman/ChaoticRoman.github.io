#!/bin/bash

echo Do not forget to set your and root password. deploy2.sh script is for your help after reset.

ssh-keygen -t rsa
rp="root@romanpavelka.cz"
cat ~/.ssh/id_rsa.pub | ssh $rp 'cat >> ./ssh/authorized_keys'

scp -r $rp:pi/care $rp:pi/interfaces $rp:pi/wpa_supplicant.conf $rp:.crontab $rp:.bash_aliases $rp:/var/www/pi/deploy2.sh ./

sudo mv wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf
sudo mv interfaces /etc/network/interfaces

raspi-config

