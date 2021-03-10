#!/bin/bash

# terminate on ping google DNS success:
ping 8.8.8.8 -q -c 2 -w 10 > /dev/null && exit 0

# if not terminated, mark the problem's time
date >> /home/pi/care/net_fails

# and try to reset the wifi adapter
sudo ifdown wlan0
sleep 5
sudo ifup --force wlan0

# if needed restart autossh tunnel
AUTOSSH=`ps aux|grep autossh|grep '666:localhost:22'|wc -l`
if [ $AUTOSSH == 0 ]
then
   /usr/bin/autossh -f -N -R \*:666:localhost:22 root@romanpavelka.cz
fi

