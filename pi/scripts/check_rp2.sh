#!/bin/bash

# terminate on ping success:
ping romanpavelka.cz -q -c 2 -w 10 > /dev/null && exit 0

# if not terminated, ping google DNS, mark romanpavelka problem on success and exit:
ping 8.8.8.8 -q -c 2 -w 10 > /dev/null && date >> /home/pi/care/rp_fails && exit 0

# if not terminated, ping router and mark on success
# external network problem, on unsuccess internal
ping 192.168.0.1 -q -c 2 -w 10 > /dev/null \
&& date >> /home/pi/care/ext_fails && exit 0\
|| date >> /home/pi/care/net_fails

# else try to reset the wifi adapter
sudo ifdown wlan0
sudo killall -q dhclient
sudo killall -q wpa_supplicant
sleep 5
sudo ifup --force wlan0

# if needed restart autossh tunnel
AUTOSSH=`ps aux|grep autossh|grep '666:localhost:22'|wc -l`
if [ $AUTOSSH == 0 ]
then
   /usr/bin/autossh -f -N -R \*:666:localhost:22 root@romanpavelka.cz
fi

