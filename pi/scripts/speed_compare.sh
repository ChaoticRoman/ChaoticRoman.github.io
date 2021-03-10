#!/bin/bash

FILES0='/home/pi/shots/2014-May_WL-RS-JD-HP-NL/2014-10-23T23:00:01.jpg /home/pi/shots/2014-May_WL-RS-JD-HP-NL/2014-10-23T23:15:02.jpg /home/pi/shots/2014-May_WL-RS-JD-HP-NL/2014-10-23T23:30:01.jpg /home/pi/shots/2014-May_WL-RS-JD-HP-NL/2014-10-23T23:45:01.jpg'
FILE1='/home/pi/shots/2014-May_WL-RS-JD-HP-NL/2014-10-23T23:45:01.jpg'
OUT=/var/run/shm/testout.gif

echo $OUT
echo

CMD="convert -resize 400x300 -delay 20 -loop 0 $FILES0 $OUT"
echo $CMD
time $CMD

CMD="convert -resize 400x300 -delay 20 -loop 0 $OUT $FILE1 $OUT"
echo $CMD
time $CMD

CMD="convert -delay 20 -loop 0 $FILES0 $OUT"
echo $CMD
time $CMD

CMD="convert -delay 20 -loop 0 $OUT $FILE1 $OUT"
echo $CMD
time $CMD

