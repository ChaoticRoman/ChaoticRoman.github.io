# Networking

## Apache

### iptables and network wide access

```
iptables -I INPUT 4 -p tcp -m state --state NEW -m tcp --dport 80 -j ACCEPT
```

### Basic HTTP access authentication

Create username and password to file, where apache main process has permitted
to read, but not to site or any other shared space!

```bash
htpasswd file username
```

Site configuration file in `/etc/apache2` or something you have should have
in appropriate directory section something like

```
AllowOverride AuthConfig
```

You need to load these modules:

```
LoadModule auth_basic_module /usr/lib/apache2/modules/mod_auth_basic.so
LoadModule authn_file_module /usr/lib/apache2/modules/mod_authn_file.so
LoadModule authz_user_module /usr/lib/apache2/modules/mod_authz_user.so
```

Create `.htaccess` in directory to be protected with content:

```
AuthType Basic
AuthUserFile full_path_to_htpasswd_file
AuthName "Some message to user."
Require user username
```

More advanced version to allow some ip address without authentication.

```
AuthType Basic
AuthUserFile full_path_to_htpasswd_file
AuthName "Hey, log in or get out!"
Require user username
Order allow,deny
Allow from ip_address_to_allow_without_authentication
satisfy any
```

Source: [http://httpd.apache.org/docs/2.2/howto/auth.html]

## SSH

### Key-based authentification

```bash
ssh-keygen -t rsa
cat ~/.ssh/id_rsa.pub | ssh user@host 'cat >> .ssh/authorized_keys'
```

### Host specific config

[https://linuxize.com/post/using-the-ssh-config-file/]

### Using ssh agent

[https://dev.to/levivm/how-to-use-ssh-and-ssh-agent-forwarding-more-secure-ssh-2c32]

### Port forwarding

Remote port forwarding serves to e.g. get on home computer behind NAT with help of public server,
i.e. "poor man's VPN".

Remote port forwarding means bringing client's port or any port in client's range
(here home's 22 port of ssh but it can be 80 of internal webpage etc...) **to listen** on remote
machine's port. Here is difference between local port forwarding.

In following instructions, remote machine is called public and machine whose port should listen
on public is called home. On public check if in `sshd_config` there is

```
AllowTcpForwarding yes
```

It should be yes as default, for details see [2].

For forwarding home's 22 to 11000 on public do in home

```bash
ssh -N -R 11000:localhost:22 publicuser@public
```

Then you can connect when logged in public by

```bash
ssh -l homeuser -p 11000 localhost
```

You can use `autossh` instead `ssh` to automatically restart session when it dies.

**If you can ensure there are no vulnerable SSH accounts on home**
(for example by setting home's `sshd_config` `AllowUsers` directive)
you can set on public in `sshd_config`

```
GatewayPorts yes
```

and then instead

`11000:localhost:22` do `\*:11000:localhost:22` to listen for all adresses on all
interfaces to allow from everywhere on the net `ssh -p 11000 homeuser@public`.

Sources:

```
[1] man ssh
[2] man sshd_config
```

## Nginx

[Installing nginx on CentOS 7 \[tested\]](https://uk.godaddy.com/help/build-a-lemp-stack-linux-nginx-mysql-php-centos-7-17349)

## Misc

### Hostname

TODO: how to set

Is nice to get name to machine i.e. to show it in prompt for your quick info. Show short and full hostname:

```bash
hostname
hostname -f
```

### netstat

Use `netstat` to write which programs (-p) are listening (-l) on TCP ports (-t) (to exclude unix sockets)

```bash
netstat -plt --numeric-ports
```

### traceroute

```bash
traceroute google.cz
```

### Show external IP address

```bash
dig +short myip.opendns.com @resolver1.opendns.com
```

From [http://unix.stackexchange.com/questions/22615/how-can-i-get-my-external-ip-address-in-bash]
