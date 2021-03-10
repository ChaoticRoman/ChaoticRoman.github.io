#!/bin/bash


dir="/home/pi/shots/2015/cam2"
d=`date "+%Y-%m-%dT%H:%M:%S"`

fswebcam -d /dev/video1 -r 1280x720 -D 10 -S 30 --no-banner -q $dir/"$d"_cam2.jpg

#convert -rotate 180 $dir/"$d"_cam2.jpg $dir/"$d"_cam2.jpg


# Last picture upload
# pi:
ln -sf $dir/"$d"_cam2.jpg /var/www/last2.jpg

# rp:
rsync -a /home/pi/shots root@romanpavelka.cz:pibp/

scp /var/www/last2.jpg root@romanpavelka.cz:/var/www/qv/

# UPLOAD INFO
/home/pi/care/upload_info.sh
