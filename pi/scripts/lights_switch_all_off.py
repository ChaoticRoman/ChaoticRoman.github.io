#!/usr/bin/python
import os


write = lambda s: os.system('echo %s > /dev/ttyUSB0' % (s,))
write('d')

pins=[11,25]
val=1
for pin in pins:
  gpio_dir = '/sys/class/gpio/gpio%d/' % pin
  f = open(gpio_dir + 'value','w')
  f.write('%d'%val)
  f.close()
