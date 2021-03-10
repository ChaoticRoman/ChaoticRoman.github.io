#!/bin/bash

python /home/pi/care/last_days_video_cam1.py
scp /run/shm/grow7.ogg root@romanpavelka.cz:/var/www/qv/pibp/
rm /run/shm/grow7.ogg

python /home/pi/care/last_days_video_cam2.py
scp /run/shm/case.ogg root@romanpavelka.cz:/var/www/qv/pibp/
rm /run/shm/case.ogg

