#!/usr/bin/python
from datetime import datetime as dt

f = open('/home/pi/care/temperature')
lines = f.read().split('\n')
f.close()

lines = [l.split(' ')[0] for l in lines if len(l)>0]

print 'Sorted?',
srt = sorted(lines)
if srt == lines:
  print 'Yes.'
  srt = True
else:
  print 'No.'
  lines=srt
  srt = False


format='%Y-%m-%dT%H:%M:%S'
lines = [dt.strptime(l, format) for l in lines]
N=len(lines)
print N, 'items from', min(lines).strftime(format), 'to', max(lines).strftime(format)


deltas = [lines[i+1]-lines[i] for i in range(N-1)]
deltas = [D.total_seconds()/60. for D in deltas]
print 'Max delta is %.1f minutes.' % (max(deltas), )

for i, d in enumerate(deltas):
  if d>6:
    print 'No data from', lines[i], 'to', lines[i+1], ('(%d minutes)'%int(d))
