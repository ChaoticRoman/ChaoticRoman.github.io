#!/bin/bash

rsync -a /home/pi/care /home/pi/shots \
         /home/pi/.bash* \
         /home/pi/.crontab \
         /etc/network/interfaces \
         /etc/rc.local \
         root@romanpavelka.cz:pibp/
