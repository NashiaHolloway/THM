# Kenobi Walkthrough

> Nashia Holloway | April 30th, 2020

## Task 1 Deploy the Vulnerable Machine

**2. Scan the machine with nmap, how many ports are open?**

```
nmap -sC -sV -A $IP -oN initial.nmap
```

![](https://github.com/nashiaholloway/THM/learning_paths/oscp_prep/kenobi/initial.png?raw=true)

## Task 2 Enumerating Samba for Shares

1. How many shares have been found?

```
nmap -p 445 --script=smb-enum-shares.nse,smb-enum-users.nse $IP -oN shares.nmap
```

There are 3 shares. IPC$ and print$ are normal to see, however there is also an anonymous share.

![](shares.png)

2. Connect to the share and list the files. What file is seen?

```
smbclient //$IP/anonymous
```

Once connected, use the command `dir` to list the contents of the directory to find the file `log.txt`.

3. What port is FTP running on?

FTP usually runs on port 21, and we can see from the initial nmap scan that that port is open.

4. What mount can we see?

```
nmap -p 111 --script=nfs-ls,nfs-statfs,nfs-showmount $IP -oN nfs.nmap
```

`/var` is the mount seen.

## Task 3 Gain Initial Access with ProFtpd

1. Use netcat to connect to the FTP port. What is the version of ProFtpd?

```
nc $IP 21
```

`1.3.5` is the version of ProFtpd.

2. How many exploits for ProFtpd are there?

```
searchsploit ProFtpd 1.3.5
```
There are 3 exploits.

![](proftpd_exploits.png)
