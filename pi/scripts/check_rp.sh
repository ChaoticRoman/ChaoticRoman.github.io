#!/bin/bash

# terminate on ping success:
ping romanpavelka.cz -q -c 2 -w 10 > /dev/null && exit 0

# if not terminated, mark the problem's time
date >> /home/pi/care/rp_fails
