#!/usr/bin/python
import os
from os import listdir
from os.path import getsize
from os import remove
from os import system
import datetime as dt


top = '/home/pi/shots/2014-May_WL-RS-JD-HP-NL/'
target_dir = '/var/run/shm/'

output_video = target_dir + 'grow7.avi'
upload_url = '/var/www/temp/'

start_day = dt.datetime(2014, 9, 15)
bloom_day = dt.datetime(2014, 11, 25)
end_day   = dt.datetime(2015, 2, 1)

desc = 'Jamaican Dream, WL, RS, GP, NL, 50\% testing of 200W LED'


def get_date(fn):
    stripped_fn = fn.split('/')[-1].split('.')[0]
    if stripped_fn[:7] == 'Webcam-': # Camorama
        d = dt.datetime.utcfromtimestamp(int(stripped_fn[7:]))
        d = dt.datetime(d.year, d.month, d.day)
        return d

    if stripped_fn[:4] == 'shot':     # shot
        stripped_fn=stripped_fn[5:]

    if stripped_fn[:3] == '201':     # take pic script
        y, m, d = int(stripped_fn[:4]), int(stripped_fn[5:7]), int(stripped_fn[8:10])
        return dt.datetime(y,m,d)
    else:
        raise ValueError('unkown name ' + stripped_fn)

def date_repr(d):
    day = (d - start_day).days+1
    days_bloom = (d-bloom_day).days+1
    dstr = desc + ', day ' + str(day)
    if days_bloom>0:
      dstr += ' (day '+str(days_bloom)+' 12-12)'
    else:
      dstr += ', 18-6'
    return dstr

flist = sorted([f for f in listdir(top) if f[-4:]=='.jpg' or f[-5:]=='.jpeg'])
now = dt.datetime.now()
#flist = [top+f for f in flist if start_day <= get_date(f) <= end_day]
flist = [top+f for f in flist if now - dt.timedelta(days=3) <= get_date(f) <= now]

flist = sorted(flist, key=get_date)


fdates = map(get_date, flist)
fdates_repr = map(date_repr, fdates)

N=len(flist)
prefix='thumb'

left=170
params0 =   "-fill '#0008' -draw 'rectangle "+str(left)+",0,640,20' " +\
            "-fill white -font DejaVu-Sans-Book -annotate +"+str(left+5)+"+15"

if True:
    print 'Labeling...'
    for i in range(N):
        params=params0 + ' \'' + fdates_repr[i] + '\''
        output_path = target_dir+prefix+ ('%05d' % i) + '.jpg'
        cmd='convert ' + flist[i] +' '+ params +' '+ output_path
        system(cmd)
        #print
    
if True:
    print 'Converting...'
    cmd='mencoder mf://' + target_dir + '*.jpg -mf w=640:h=480:fps=8:type=jpg -ovc lavc -lavcopts vcodec=mpeg4:mbd=2:trell -oac copy -o ' + output_video
    #print cmd
    system(cmd)
    system('rm ' + target_dir + prefix + '*.jpg')
    
if False:
    print 'Uploading...'
    os.system('cp ' + output_video + ' ' + upload_url)
