#!/bin/bash

DATE=`date +%Y-%m-%dT%H:%M:%S`
FAILS=/home/pi/care/fails

# terminate on ping success:
ping romanpavelka.cz -q -c 2 -w 10 > /dev/null && exit 0

# if not terminated, ping google DNS, mark romanpavelka problem on success and exit:
ping 8.8.8.8 -q -c 2 -w 10 > /dev/null && echo $DATE failed to reach rp >> $FAILS && exit 0

# if not terminated, ping router and mark on success
# external network problem, on unsuccess internal
ping 192.168.0.1 -q -c 2 -w 10 > /dev/null \
&& echo $DATE failed to reach google DNS >> $FAILS && exit 0\
|| echo $DATE failed to reach router >> $FAILS

# if needed restart autossh tunnel
#AUTOSSH=`ps aux|grep autossh|grep '666:localhost:22'|wc -l`
#if [ $AUTOSSH == 0 ]
#then
#   /usr/bin/autossh -f -N -R \*:666:localhost:22 root@romanpavelka.cz
#fi

