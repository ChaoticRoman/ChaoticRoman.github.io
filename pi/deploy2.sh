#!/bin/bash
sudo aptitude remove wolfram-engine -y
sudo aptitude update -y
sudo aptitude upgrade -y
sudo aptitude install htop screen python-matplotlib -y
cd /usr/src/
sudo rpi-update
