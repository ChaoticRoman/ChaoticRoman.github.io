#!/bin/bash


dir="/home/pi/shots/2015/cam1"
d=`date "+%Y-%m-%dT%H:%M:%S"`
#echo $d

# capture, possible to specify banner, see man fswebcam:
fswebcam -r 640x480 -D 5 -S 20 --no-banner -q $dir/"$d"_cam1.jpg



# Last picture upload
# pi:
ln -sf $dir/"$d"_cam1.jpg /var/www/last1.jpg
# rp:
scp /var/www/last1.jpg root@romanpavelka.cz:/var/www/qv/


# UPLOAD INFO
/home/pi/care/upload_info.sh
