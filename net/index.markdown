<h1>Networking / <span lang='cs'>Síťování</span></h1>

<a href='..'>Home / <span lang='cs'>Domů</span></a>


<h2>Apache</h2>

<h3>iptables and network wide access</h3>
<pre>
iptables -I INPUT 4 -p tcp -m state --state NEW -m tcp --dport 80 -j ACCEPT
</pre>
<h3>Basic HTTP access authentication</h3>

Create username and password to file, where apache main process has permitted to read, but not to site or any other shared space!
<pre>
htpasswd file username
</pre>

Site configuration file in /etc/apache2 or something you have should have in appropriate directory section
something like
<pre>
AllowOverride AuthConfig
</pre>

You need to load these modules:

<pre>
LoadModule auth_basic_module /usr/lib/apache2/modules/mod_auth_basic.so
LoadModule authn_file_module /usr/lib/apache2/modules/mod_authn_file.so
LoadModule authz_user_module /usr/lib/apache2/modules/mod_authz_user.so
</pre>

Create .htaccess in directory to be protected with content:
<pre>
AuthType Basic
AuthUserFile full_path_to_htpasswd_file
AuthName "Some message to user."
Require user username
</pre>

More advanced version to allow some ip address without authentication.
<pre>
AuthType Basic
AuthUserFile full_path_to_htpasswd_file
AuthName "Hey, log in or get out!"
Require user username
Order allow,deny
Allow from ip_address_to_allow_without_authentication
satisfy any
</pre>
source: http://httpd.apache.org/docs/2.2/howto/auth.html

<h2>SSH</h2>


<h3>Key-based authentification</h3>
<pre>
ssh-keygen -t rsa
cat ~/.ssh/id_rsa.pub | ssh user@host 'cat >> .ssh/authorized_keys'
</pre>


<h3 id="port-forwarding">Remote port forwarding to get on home computer behind NAT with help of public server</h3>

Remote port forwarding means bringing client's port or any port in client's range
(here home's 22 port of ssh but it can be 80 of internal webpage etc...) *to listen* on remote
machine's  port. Here is difference between local port forwarding.
<p>

In following instructions, remote machine is called public and machine whose port should listen
on public is called home. On public check if in sshd_config there is
<pre>
AllowTcpForwarding yes
</pre>
It should be yes as default, for details see [2].

For forwarding home's 22 to 11000 on public do in home
<pre>
ssh -N -R 11000:localhost:22 publicuser@public
</pre>

Then you can connect when logged in public by
<pre>
ssh -l homeuser -p 11000 localhost
</pre>
<p>
You can use autossh instead ssh to automatically restart session when died.
<p>

<b>if you can ensure there are no vulnerable SSH accounts on home</b>
(for example by setting home's sshd_config AllowUsers directive)
you can change on public allow in sshd_config
<pre>
GatewayPorts yes
</pre>
and then instead
"11000:localhost:22" do "\*:11000:localhost:22"
to listen for all adresses on all interfaces to allow from everywhere on the net
<pre>ssh -p 11000 homeuser@public</pre>

<p>
Sources:
<pre>
[1] man ssh
[2] man sshd_config
</pre>

<h2>Nginx</h2>
<a href="https://uk.godaddy.com/help/build-a-lemp-stack-linux-nginx-mysql-php-centos-7-17349">
  Installing nginx on CentOS 7 [tested]
</a>

<h2>Misc / <span lang='cs'>Různé</span></h2>


<h3>Hostname</h3>
TODO: how to set<p>

Is nice to get name to machine i.e. to show it in prompt for your quick info. Show short and full hostname:
<pre>
hostname
hostname -f
</pre>


<h3>netstat</h3>
netstat to write which programs (-p) are listening (-l) on TCP ports (-t) (to exclude unix sockets)
<pre>
netstat -plt --numeric-ports
</pre>


<h3>traceroute</h3>
<pre>
traceroute google.cz
</pre>


<h3>Show external IP address</h3>
<pre>
dig +short myip.opendns.com @resolver1.opendns.com
</pre>
from http://unix.stackexchange.com/questions/22615/how-can-i-get-my-external-ip-address-in-bash


<h3>Postfix</h3>
Postfix configuration utility:
<pre>dpkg-reconfigure postfix</pre>




<p> <a href='..'>Home / <span lang='cs'>Domů</span></a>