<h1>Raspberry Pi</h1>

<h2>Deployment with Raspbian</h2>
<pre>
passwd
sudo su
passwd
raspi-config # enlarge card, set hostname and restart

sudo su
cp /usr/share/zoneinfo/Europe/Prague /etc/localtime
aptitude remove wolfram-engine # more than 450 MB freed...
aptitude install htop screen
screen
rpi-update
aptitude update
aptitude full-upgrade

aptitude install python-matplotlib image-magick autossh -y
ssh-keygen -t rsa
</pre>

<h2>Set wifi and dhcp on Raspbian</h2>
Your /etc/wpa_supplicant/wpa_supplicant.conf should look like this:

<pre>
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
  ssid="NETWORK_SSID"
  psk="NETWORK_PASSWORD"
  proto=RSN
  key_mgmt=WPA-PSK
  pairwise=CCMP
  auth_alg=OPEN
}
</pre>

and your /etc/network/interfaces
<pre>
auto lo

iface lo inet loopback
iface eth0 inet dhcp

auto wlan0
allow-hotplug wlan0
iface wlan0 inet dhcp
wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
wireless-power off

iface default inet dhcp
</pre>



Then I have little script for logging wifi status and restarting it when needed.
<p>
check_net.sh
<pre>
#!/bin/bash

DATE=`date +%Y-%m-%dT%H:%M:%S`
FAILS=/home/pi/care/fails

# terminate on ping success:
ping romanpavelka.cz -q -c 2 -w 10 > /dev/null && exit 0

# if not terminated, ping google DNS, mark romanpavelka problem on success and exit:
ping 8.8.8.8 -q -c 2 -w 10 > /dev/null && echo $DATE failed to reach rp >> $FAILS && exit 0

# if not terminated, ping router and mark on success
# external network problem, on unsuccess internal
ping 192.168.0.1 -q -c 2 -w 10 > /dev/null \
&& echo $DATE failed to reach google DNS >> $FAILS && exit 0\
|| echo $DATE failed to reach router >> $FAILS

# else try to reset the wifi adapter
sudo ifdown wlan0
sudo killall -q dhclient
sudo killall -q wpa_supplicant
sleep 5
sudo ifup --force wlan0
</pre>
I use cron calling it every five minutes.


<h2>Modules building</h2>
Firts you need headers of your kernel, the simplest way to get them is the rpi-source script.
<pre>
sudo wget https://raw.githubusercontent.com/notro/rpi-source/master/rpi-source -O /usr/bin/rpi-source
sudo chmod +x /usr/bin/rpi-source
/usr/bin/rpi-source -q --tag-update
</pre>

<h2>D-Link GO-USB-N150 Wireless N150 USB Adapter</h2>
This is nice cheap 802.11b/g/n, up to 150 Mbit/s, USB2.0 wifi adapter.
With 1A 5V supply I didn't get any problems supplying this stick and webcam directly from Pi.<p>

Install kernel headers as explained above and compile and install RTL8188EU driver from
<pre>
https://github.com/lwfinger/rtl8188eu
</pre>

<h2>Nginx instead of Apache</h2>

installation
<pre>
sudo su
aptitude install nginx -y && aptitude install php5-fpm -y
nano /etc/nginx/sites-enabled/default # I like to set document root to /var/www
nano /etc/php5/fpm/php.ini            # set cgi.fix_pathinfo=0
service php5-fpm restart
service nginx restart
</pre>
Source:http://elinux.org/RPi_Nginx_Webserver

<p>
To allow directory listings, set in site configuration file (that linked in /etc/nginx/sites-enabled):
<pre>
        location /somedir {
               autoindex on;
        }
</pre>
here the root / presents root directory of the webpage.
<p>
Source: https://www.digitalocean.com/community/tutorials/how-to-set-up-http-authentication-with-nginx-on-ubuntu-12-10
