#!/bin/bash
cpuTemp0=$(cat /sys/class/thermal/thermal_zone0/temp)
cpuTemp1=$(($cpuTemp0/1000))
cpuTemp2=$(($cpuTemp0/100))
cpuTempM=$(($cpuTemp2 % $cpuTemp1))

echo -n `date +%Y-%m-%dT%H:%M:%S` >> /home/pi/care/temperature
echo -n " " >> /home/pi/care/temperature
echo -n CPUtemp"="$cpuTemp1"."$cpuTempM"'C" >> /home/pi/care/temperature
echo -n " GPU" >> /home/pi/care/temperature
/opt/vc/bin/vcgencmd measure_temp >> /home/pi/care/temperature



