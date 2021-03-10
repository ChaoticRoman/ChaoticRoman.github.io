#!/usr/bin/python
from datetime import datetime as dt

pin = 23
# 24-hours:
start, end = 7, 1

cross_the_day = start>end
now = dt.now()
hours = now.hour
on = False
if cross_the_day:
  if (hours < end) or (hours >= start):
     on = True 
else:
  if (hours >= start) and (hours < end):
     on = True

gpio_dir = '/sys/class/gpio/gpio%d/' % pin

# TODO if is dir export... 

if on:
  val=0
else:
  val=1

f = open(gpio_dir + 'value','w')
f.write('%d'%val)
f.close()
