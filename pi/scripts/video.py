#!/usr/bin/python
import os
from os import listdir
from os.path import getsize
from os import remove
from os import system
import datetime as dt


top = '/home/pi/shots/M2015/'
target_dir = '/run/shm/'

output_video = target_dir + '2015mothersA.ogg'

start_day = dt.datetime(2015, 1, 10)
bloom_day = dt.datetime(2015, 10, 1)
end_day   = dt.datetime(2015, 12, 31)

desc = 'CM CBD, JH, CJ, VK, LSD'
N = 120

def get_date(fn):
    stripped_fn = fn.split('/')[-1].split('.')[0]
    if stripped_fn[:7] == 'Webcam-': # Camorama
        d = dt.datetime.utcfromtimestamp(int(stripped_fn[7:]))
        d = dt.datetime(d.year, d.month, d.day)
        return d

    if stripped_fn[:4] == 'shot':     # shot
        stripped_fn=stripped_fn[5:]

    elif stripped_fn[:3] == '201':     # take pic script
        y, m, d,h,min,s = map(int, [stripped_fn[:4], stripped_fn[5:7], stripped_fn[8:10], \
                            stripped_fn[11:13], stripped_fn[14:16], stripped_fn[17:19]])
        return dt.datetime(y,m,d,h,min,s)
    elif stripped_fn[:4] == 'M201':     # take pic script
        stripped_fn = stripped_fn[1:]
        y, m, d,h,min,s = map(int, [stripped_fn[:4], stripped_fn[5:7], stripped_fn[8:10], \
                            stripped_fn[11:13], stripped_fn[14:16], stripped_fn[17:19]])
        return dt.datetime(y,m,d,h,min,s)
    else:
        raise ValueError('unkown name ' + stripped_fn)

def date_repr(d):
    day = (d - start_day).days+1
    days_bloom = (d-bloom_day).days+1
    dstr = desc + ', day ' + str(day)
    if days_bloom>0:
      dstr += ' (day '+str(days_bloom)+' 12-12) ['+d.strftime('%Y-%m-%dT%H:%M:%S')+']'
    else:
      dstr += ', 18-6 ['+d.strftime('%Y-%m-%dT%H:%M:%S')+']'
    return dstr

flist = sorted([f for f in listdir(top) if f[-4:]=='.jpg' or f[-5:]=='.jpeg'])


now = dt.datetime.now()
#flist = [top+f for f in flist if start_day <= get_date(f) <= end_day]

#flist = [top+f for f in flist[-N:]]

flist = sorted(flist, key=get_date)
#print flist

fdates = map(get_date, flist)
fdates_repr = map(date_repr, fdates)

N=len(flist)
prefix='thumb'

left=840
params0 =   "-fill '#0008' -draw 'rectangle "+str(left)+",0,1280,20' " +\
            "-fill white -font DejaVu-Sans-Book -annotate +"+str(left+5)+"+15"

if True:
    print 'Labeling...'
    for i in range(N):
        params=params0 + ' \'' + fdates_repr[i] + '\''
        output_path = target_dir+prefix+ ('%05d' % i) + '.jpg'
        cmd='convert ' + flist[i] +' '+ params +' '+ output_path
        #print cmd
        system(cmd)
        #print
    
if True:
    print 'Converting...'
    #cmd='mencoder mf://' + target_dir + '*.jpg -mf w=640:h=480:fps=8:type=jpg -ovc lavc -lavcopts vcodec=mpeg4:mbd=2:trell -oac copy -o ' + output_video
    cmd='avconv -r 8 -i ' + target_dir + 'thumb%05d.jpg -acodec libvorbis -vcodec libtheora -ac 2 -ab 96k -ar 44100 -b 819200 -s 1280x720 ' + output_video
    
    #print cmd
    system(cmd)
    system('rm ' + target_dir + prefix + '*.jpg')
