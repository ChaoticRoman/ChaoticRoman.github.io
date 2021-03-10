#!/usr/bin/python
from datetime import datetime as dt
import os

# 24-hours:
start, end = 6, 18


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


# TODO if is dir export... 

write = lambda s: os.system('echo %s > /dev/ttyUSB0' % (s,))

if on:
  #print 'u'
  write('u')
else:
  #print 'd'
  write('d')
