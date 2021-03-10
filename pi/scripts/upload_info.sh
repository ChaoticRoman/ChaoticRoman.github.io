#!/bin/bash

outf=/run/shm/qvi
plot=/run/shm/temperature.png
destination=root@romanpavelka.cz:/var/www/qv/pibp/

echo -n > $outf # Clear file, not remove to be still with us :]

echo -n "Last shot cam1: " >> $outf
lastshot=`ls /home/pi/shots/2015/cam1/*jpg|tail -n 1`
ls $lastshot >> $outf
echo -n "Last shot cam2: " >> $outf
lastshot=`ls /home/pi/shots/2015/cam2/*jpg|tail -n 1`
ls $lastshot >> $outf
echo >> $outf

echo -n "Updated: " >> $outf
date >> $outf
echo -n "Last boot: " >> $outf
tail -n 1 /home/pi/care/boots >> $outf
echo -n "Uptime: " >> $outf
uptime|head -c 26 >> $outf
echo >> $outf


echo "$ df -h /dev/root" >> $outf
df -h /dev/root >> $outf
echo >> $outf


echo Networking fails monitoring: >> $outf
tail -n 5 /home/pi/care/fails >> $outf
echo >> $outf


echo Temperature logs:>> $outf
tail -n 5 /home/pi/care/temperature >> $outf
echo >> $outf

echo Temperature log analysis:>> $outf
/home/pi/care/extract_gap_in_temperature.py >> $outf
echo >> $outf

echo TODO:>> $outf
cat /home/pi/TODO >> $outf
echo >> $outf

scp $outf $destination
scp $plot $destination
#rm $outf

