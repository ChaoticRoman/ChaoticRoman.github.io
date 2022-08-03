<h1>Bash tricks</h1>

In all php files look for string "We are currently" and print filename and line number for every match:
<pre>
find . -iname "*php" -exec grep -Hn "We are currently" "{}" \;
</pre>

Inkscape can convert files from bash!
<pre>
inkscape -z -D --file=input.svg --export-pdf=output.pdf
</pre>

Very useful to know: http://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard

<h2>Nice aliases</h2>
<pre>
export LANG=cs_CZ.utf8

# user@hostname path $: 
PS1='\[\e[00;32m\]\u@\h\[\e[m\] \[\e[1;34m\]\w \$ \[\e[m\]\[\e[00m\]'

# root@hostname path $: 
PS1='\[\e[1;31m\]\u@\h\[\e[m\] \[\e[1;34m\]\w\[\e[m\] \[\e[1;31m\]\$ \[\e[m\]\[\e[0;00m\]'

alias a='nano ~/.bash_aliases && . ~/.bash_aliases'

alias ..='cd ..'
alias l='ls -a --color'
alias ll='ls -alh --color'

alias sdr='screen -dr'
alias sr='screen -r'

alias work='cd ~/work'

# love this
alias matplotlib='python3 -i -c "from datetime import datetime as dt;from datetime import timedelta as td;import matplotlib.pyplot as plt;plt.ion()"'

# sometimes useful for webservers, modify according to your needs
alias wgr='chmod -R g+r /var/www; chgrp -R www-data /var/www'
alias www='cd /var/www'

# network troubleshooting
alias pingg='ping 8.8.8.8'
alias pinggg='ping google.com'

# gcc include stuff
alias printIncludePath='echo | gcc -E -Wp,-v - 2>&1 | grep "^ "'

# docker (docker ps and docker container ls are same commands)
alias listRunningContainers='docker container ls -s'
alias listAllContainers='docker container ls -as'
alias killAllContainers='docker kill $(docker ps -q)'
alias removeAllContainers='docker rm $(docker ps -a -q)'
</pre>

## Git aware prompt

Download official script

```
wget https://raw.githubusercontent.com/git/git/master/contrib/completion/git-prompt.sh -O ~/.git-prompt.sh
```

and replace your prompt setting code in `.bashrc` with

```
GIT_PS1_SHOWDIRTYSTATE=1
GIT_PS1_SHOWSTASHSTATE=1
GIT_PS1_SHOWCOLORHINTS=1
GIT_PS1_SHOWUNTRACKEDFILES=1
GIT_PS1_SHOWUPSTREAM="verbose"
source ~/.git-prompt.sh
if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]$(__git_ps1 " (%s)")\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w$(__git_ps1 " (%s)")\$ '
fi
```
