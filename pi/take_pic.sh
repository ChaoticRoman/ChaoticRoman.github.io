#!/bin/bash


dir="/home/pi/shots/M2015/"
d=`date "+%Y-%m-%dT%H:%M:%S"`
#echo $d

# capture, possible to specify banner, see man fswebcam:
fswebcam -r 1280x720 -D 5 -S 20 --no-banner -q $dir/M$d.jpg
convert -rotate 180 $dir/M$d.jpg $dir/M$d.jpg
# Last picture upload
# pi:
ln -sf "$dir/"M"$d.jpg" /var/www/last.jpg

# rp:
rsync -a /home/pi/shots root@romanpavelka.cz:pib/

#former rp:
#scp "$dir/$d.jpg" root@romanpavelka.cz:pi/shots/2014-May_WL-RS-JD-HP-NL/


scp /var/www/last.jpg root@romanpavelka.cz:/var/www/qv/
# UPLOAD INFO
/home/pi/care/upload_info.sh


# AVI creation
python /home/pi/care/last_days_video_cam1.py
scp /run/shm/2015mothers.ogg root@romanpavelka.cz:/var/www/qv/pib/
mv /run/shm/2015mothers.ogg /run/shm/2015mothersL.ogg
#rm /run/shm/2015mothers.ogg



# GIF creation
#/home/pi/care/mkgif.py


