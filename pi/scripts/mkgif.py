#!/usr/bin/python
import os
top = '/home/pi/shots/M2015/'

LAST_N = 8

flist = sorted([f for f in os.listdir(top) if f[-4:]=='.jpg' or f[-5:]=='.jpeg'])
flist = [top+f for f in flist if f[:3]=='M20'][-LAST_N:]
#print flist
#for f in flist: print f
os.system('convert -resize 320x240 -delay 20 -loop 0 "' + '" "'.join(flist) + '" /run/shm/lqv.gif')
os.system('scp /run/shm/lqv.gif root@romanpavelka.cz:/var/www/qv/')
#os.system('du -sh "' + '" "'.join(flist) + '"')
