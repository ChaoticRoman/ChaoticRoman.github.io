#!/usr/bin/python

import datetime
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import os

dir = '/home/pi/care/'
data_file = dir + 'temperature'
plot_file = '/var/run/shm/temperature.png'


f = open(data_file)
data = f.read()
f.close()

data = data.split('\n')
data = [d.split(' ') for d in data if len(d)==49 and not ('\0' in d)]
strptime = datetime.datetime.strptime
format = r'%Y-%m-%dT%H:%M:%S'

times = [ strptime(d[0], format) for d in data ]

nan = float('nan')
tCPU, tGPU = [], []
for d in data:
  if len(d)==2:
    tCPU.append(nan)
    tGPU.append(float(d[1][5:9]))
  elif len(d)==3: 
    tCPU.append(float(d[1][8:12]))
    tGPU.append(float(d[2][8:12]))
  else:
    tGPU.append(nan)
    tCPU.append(nan)

#print [len(i) for i in (data, times, tCPU, tGPU)]
#print data[-15], times[-15], tCPU[-15], tGPU[-15]
#print data[-1], times[-1], tCPU[-1], tGPU[-1]





'''
Created on Nov 9, 2012

@author: roman
'''
import numpy as np

def triangle_moving_average(input_arr0, one_side_len):
    """ moving average, full length, over 2*one_side_len+1 points,
    maximal weight in center, returns numpy array of same length as data,
    one_side_len edge values are masked to nans"""

    input_arr = np.array(input_arr0)
    n = input_arr.shape[0]
    output = np.empty((n,))*np.NaN
    
    l=one_side_len
    
    mask = np.zeros( (2*l+1,) )
    max_weight = 1./(l+1)
    diff  = 1./(l+1)**2
    
    mask[l] = max_weight
    for i in range(l):
        mask[l + (i+1)] = (i+1) * diff
        mask[l - (i+1)] = mask[l + (i+1)]
        
    if n < 2*l+1:
        raise ValueError('mask bigger than data')
    
    # TRIANGLE AVERAGE
    output[:l] = np.NaN #left boundary
#    for i in range(l): #left boundary
##        print len(mask[l-i:]), len(input[:l+1+i])
#        valid = -np.isnan(input[:l+1+i])
#        if valid[i]:
#            output[i] = np.sum( mask[l-i:][valid]*input[:l+1+i][valid] ) / np.sum(mask[l-i:][valid])
#        else:
#            output[i] = np.NaN
    
    for i in range(n-2*l): # inner aread
        valid = -np.isnan(input_arr[i:i+2*l+1])
        if valid[l]:
            output[l+i] = np.sum( mask[:][valid]*input_arr[i:i+2*l+1][valid] ) / np.sum(mask[:][valid])
        else:
            output[l+i] = np.NaN
            
    output[-l:] = np.NaN       # right boundary
#    for i in range(l): # right boundary
##        print len(mask[:2*l-i]), len(input[n-2*l+i:])
#        valid = -np.isnan(input[n-2*l+i:])
#        if valid[l]:
#            output[n-l+i] = np.sum( mask[:2*l-i][valid]*input[n-2*l+i:][valid] ) / np.sum(mask[:2*l-i][valid])
#        else:
#            output[l+i] = np.NaN

    return output




#plt.ion()
plt.figure(figsize=(12,6))
plt.title('PiB temperatures\n'+str(data[0][0])+' - '+str(data[-1][0]))
plt.plot(times, tCPU, 'b.', label='CPU', ms=1.5)
plt.plot(times, triangle_moving_average(tCPU, 6), 'b-')
plt.plot(times, tGPU, 'r.', label='GPU', ms=1.5)
plt.plot(times, triangle_moving_average(tGPU, 12), 'r-')

plt.ylabel('temperature [C]')
plt.legend()
plt.grid()
plt.savefig(plot_file)
#raw_input()

os.system('scp %s root@romanpavelka.cz:/var/www/qv/' % plot_file)
