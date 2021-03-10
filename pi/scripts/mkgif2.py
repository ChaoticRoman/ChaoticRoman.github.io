#!/usr/bin/python
import os
top = '/home/pi/shots/2015/cam2/'

LAST_N = 10

flist = sorted([f for f in os.listdir(top) if f[-4:]=='.jpg' or f[-5:]=='.jpeg'])
flist = [top+f for f in flist if f[:2]=='20'][-LAST_N:]

#for f in flist: print f
os.system('convert -resize 320x180 -delay 20 -loop 0 "' + '" "'.join(flist) + '" /run/shm/lqv2.gif')
os.system('scp /run/shm/lqv2.gif root@romanpavelka.cz:/var/www/qv/')
#os.system('du -sh "' + '" "'.join(flist) + '"')
